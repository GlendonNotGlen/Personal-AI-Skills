"""Local preparation only: private drafts and optional pinned Docker readiness."""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
LOCAL_IMAGE = "bbworkbench-toolbox:0.1.0"
LOCAL_ENDPOINT = "npipe:////./pipe/dockerDesktopLinuxEngine"
IMAGE_FORMAT = (
    '{"id":{{json .Id}},"os":{{json .Os}},"architecture":{{json .Architecture}},'
    '"digests":{{json .RepoDigests}}}'
)


class PreparationError(Exception):
    pass


def resolve_workbench(explicit=None):
    configured = explicit or os.environ.get("BB_WORKBENCH_ROOT")
    config = SKILL / "workbench.json"
    if not configured and config.exists():
        value = json.loads(config.read_text(encoding="utf-8"))
        if value.get("schema_version") != 1 or set(value) != {"schema_version", "workbench_root"}:
            raise PreparationError("unsupported workbench.json")
        configured = value["workbench_root"]
    candidates = [Path(configured)] if configured else list(SKILL.parents)
    for candidate in candidates:
        if not candidate.is_absolute():
            raise PreparationError("workbench path must be absolute")
        root = candidate.resolve()
        required = (
            "src/bbworkbench/cli.py",
            "pyproject.toml",
            "uv.lock",
            "image.lock.json",
            "AGENTS.md",
            "init.md",
            "IMPLEMENTATION_STATUS.md",
        )
        if all((root / name).is_file() for name in required):
            return root
    raise PreparationError("set BB_WORKBENCH_ROOT to the trusted bootstrapped workbench")


def overlaps(left, right):
    return left == right or left.is_relative_to(right) or right.is_relative_to(left)


def registry_reference(value):
    if value is None:
        return None
    if not re.fullmatch(r"[a-z0-9][a-z0-9./:_-]*@sha256:[0-9a-f]{64}", value):
        raise PreparationError("registry image must be an immutable image@sha256:64-hex reference")
    return value


def docker_command(args, timeout=10):
    executable = shutil.which("docker")
    if not executable:
        raise PreparationError("Docker CLI missing; install Docker Desktop locally")
    env = os.environ.copy()
    for key in ("DOCKER_HOST", "DOCKER_CONTEXT", "DOCKER_TLS_VERIFY", "DOCKER_CERT_PATH"):
        env.pop(key, None)
    try:
        return subprocess.run(
            [executable, "--context", "desktop-linux", *args],
            capture_output=True,
            text=True,
            env=env,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise PreparationError(
            "Docker command timed out; no restart or fallback attempted"
        ) from exc


def inspect_image(reference):
    result = docker_command(["image", "inspect", reference, "--format", IMAGE_FORMAT])
    if result.returncode:
        return None
    return json.loads(result.stdout)


def ensure_toolbox(expected_id, start=False, pull=False, registry_image=None):
    result = {"state": "blocked", "started": False, "pulled": False, "tagged": False}
    try:
        registry_image = registry_reference(registry_image)
        if sys.platform != "win32":
            raise PreparationError("Docker preparation is validated only for Windows Desktop")
        context = docker_command(
            ["context", "inspect", "desktop-linux", "--format", "{{.Endpoints.docker.Host}}"]
        )
        if context.returncode or context.stdout.strip() != LOCAL_ENDPOINT:
            raise PreparationError("desktop-linux must point to the local Desktop Linux pipe")
        info_args = ["info", "--format", "{{.OSType}}/{{.Architecture}}"]
        info = docker_command(info_args)
        if info.returncode and start:
            started = docker_command(["desktop", "start", "--detach"], timeout=15)
            if started.returncode:
                raise PreparationError("Docker Desktop start failed; use a local operator terminal")
            result["started"] = True
            deadline = time.monotonic() + 60
            while info.returncode and time.monotonic() < deadline:
                time.sleep(2)
                info = docker_command(info_args, timeout=5)
        if info.returncode:
            raise PreparationError("Docker Linux engine unavailable; startup/access is required")
        if info.stdout.strip() not in {"linux/x86_64", "linux/amd64"}:
            raise PreparationError("only the tested Linux amd64 engine is supported")
        local = inspect_image(LOCAL_IMAGE)
        if local and local["id"] != expected_id:
            raise PreparationError(
                "local toolbox tag conflicts with image.lock.json; not overwritten"
            )
        image = inspect_image(registry_image) if registry_image else None
        if image is None and local is not None:
            image = local
        if image is None and pull:
            if not registry_image:
                raise PreparationError(
                    "set BB_TOOLBOX_IMAGE or --registry-image to allow a pinned pull"
                )
            result["pull_attempted"] = True
            fetched = docker_command(
                ["pull", "--platform", "linux/amd64", registry_image], timeout=180
            )
            if fetched.returncode:
                raise PreparationError(
                    "pinned pull failed; check local Docker login and repository access"
                )
            result["pulled"] = True
            image = inspect_image(registry_image)
            if image and registry_image not in (image.get("digests") or []):
                raise PreparationError("pulled image does not record the expected registry digest")
        if image is None:
            raise PreparationError("pinned toolbox missing; allow its immutable registry pull")
        if image["os"] != "linux" or image["architecture"] != "amd64":
            raise PreparationError("toolbox platform differs from the tested linux/amd64")
        if image["id"] != expected_id:
            raise PreparationError(
                "local image identity differs from lock; new-host verification required"
            )
        result["image_id"] = image["id"]
        if local is None:
            if not pull:
                raise PreparationError("local Compose tag missing; allow preparation to create it")
            tagged = docker_command(["tag", registry_image, LOCAL_IMAGE])
            if tagged.returncode:
                raise PreparationError("could not create the absent local Compose tag")
            result["tagged"] = True
        result["state"] = "ready"
    except (PreparationError, ValueError, KeyError, OSError) as exc:
        # Never echo daemon/registry diagnostics or credential helper output.
        result["blocker"] = (
            str(exc) if isinstance(exc, PreparationError) else "Docker metadata invalid"
        )
    return result


def prepare(
    workbench,
    program,
    initialize=False,
    start=False,
    pull=False,
    synthetic=False,
    registry_image=None,
):
    # Only a trusted operator-selected installation supplies executable Python.
    sys.path.insert(0, str(workbench / "src"))
    from bbworkbench import state
    from bbworkbench.config import data_root, secret_root

    state.safe_id(program)
    registry_image = registry_reference(
        registry_image if registry_image is not None else os.environ.get("BB_TOOLBOX_IMAGE")
    )
    data, secrets = data_root(), secret_root()
    for path in (data, secrets):
        state.reject_links(path)
    data, secrets = data.resolve(), secrets.resolve()
    if overlaps(data, secrets):
        raise PreparationError("DATA_ROOT and SECRET_ROOT must be disjoint")
    if synthetic and (start or pull):
        raise PreparationError("synthetic-fixture mode is offline only")
    if not synthetic:
        for path in (data, secrets):
            if overlaps(path, workbench) or overlaps(path, Path.cwd().resolve()):
                raise PreparationError(
                    "private roots must be outside workbench and current project"
                )
    lock = json.loads((workbench / "image.lock.json").read_text(encoding="utf-8"))
    if (
        lock.get("schema_version") != 1
        or lock.get("platform") != "linux/amd64"
        or not re.fullmatch(r"sha256:[0-9a-f]{64}", lock.get("image", ""))
    ):
        raise PreparationError("unsupported workbench image lock")
    root = state.program_dir(program)
    created = False
    if root.exists():
        manifest = state.load_program(program)
        control = state.control(root)
    elif initialize:
        state.init_program(program)
        created = True
        manifest, control = state.load_program(program), state.control(root)
    else:
        manifest, control = None, None
    docker = (
        {"state": "not checked", "reason": "synthetic offline fixture"}
        if synthetic
        else ensure_toolbox(lock["image"], start=start, pull=pull, registry_image=registry_image)
    )
    return {
        "schema_version": 1,
        "workbench_root": str(workbench),
        "program": program,
        "data_root": str(data),
        "secret_root": str(secrets),
        "program_directory": str(root),
        "created_draft": created,
        "program_exists": manifest is not None,
        "program_stopped": control["stopped"] if control else None,
        "policy_approved": manifest.policy.approved_by_operator if manifest else False,
        "target_requests": 0,
        "docker": docker,
        "caido_configuration_present": {
            key: bool(os.environ.get(key))
            for key in (
                "CAIDO_BRIDGE_CONFIG",
                "CAIDO_API_URL",
                "CAIDO_PROXY_URL",
                "CAIDO_PROJECT_ID",
                "CAIDO_CA_FILE",
            )
        },
        "live_integration": "not checked; audited runtime/project/HTTPS capture required",
        "next_action": (
            "operator reviews private policy, scope, data-sharing and expected Caido project"
            if manifest
            else "initialize a private deny-all draft"
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workbench")
    parser.add_argument("--program", required=True)
    parser.add_argument("--data-root")
    parser.add_argument("--secret-root")
    parser.add_argument("--registry-image")
    parser.add_argument("--init-draft", action="store_true")
    parser.add_argument("--start-docker", action="store_true")
    parser.add_argument("--pull-image", action="store_true")
    parser.add_argument("--synthetic-fixture", action="store_true")
    args = parser.parse_args()
    try:
        workbench = resolve_workbench(args.workbench)
        for key, value in (("DATA_ROOT", args.data_root), ("SECRET_ROOT", args.secret_root)):
            if value:
                if not Path(value).is_absolute():
                    raise PreparationError("private root overrides must be absolute")
                os.environ[key] = value
        result = prepare(
            workbench,
            args.program,
            args.init_draft,
            args.start_docker,
            args.pull_image,
            args.synthetic_fixture,
            args.registry_image,
        )
        print(json.dumps(result, indent=2))
        return 2 if result["docker"]["state"] == "blocked" else 0
    except Exception as exc:
        workbench_error = getattr(
            sys.modules.get("bbworkbench.errors"), "WorkbenchError", PreparationError
        )
        message = (
            str(exc)
            if isinstance(exc, (PreparationError, workbench_error))
            else "preparation failed; verify installation and private path permissions"
        )
        print(json.dumps({"error": message, "target_requests": 0}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
