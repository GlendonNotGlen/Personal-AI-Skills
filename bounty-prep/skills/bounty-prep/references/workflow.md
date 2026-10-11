# Workbench session context

One reusable toolbox image serves separate private program workspaces. Manual browsing through Caido supplies captured traffic. The supervised loop is: review selected traffic, record a specific hypothesis, prepare a bounded plan, let the operator approve its displayed hash, compare baseline/candidate/control, preserve evidence with Caido request IDs, and checkpoint/stop. Preparation ends before testing.

Use `bb doctor` for local inspection. Invoke subsequent CLI calls with the same roots and installed workbench, for example:

```powershell
$env:DATA_ROOT = 'PRIVATE-DATA-ROOT-FROM-PREPARATION'
$env:SECRET_ROOT = 'PRIVATE-SECRET-ROOT-FROM-PREPARATION'
uv run --offline --frozen --no-sync --directory $env:BB_WORKBENCH_ROOT bb doctor
```

These placeholders represent paths, never secret values. Set `BB_WORKBENCH_ROOT` privately to the trusted installation's absolute path. Do not silently change policy or resume controls while reusing a program. Existing data-sharing consent is required before reading engagement content into Codex; synthetic fixture content is distinct.

There is no default registry account, image reference or image digest. When a registry pull is needed, set `BB_TOOLBOX_IMAGE` privately or pass `--registry-image` with an operator-verified immutable reference: `<registry>/<namespace>/<image>@sha256:<64-hex-digest>`. Mutable tags are refused. A missing setting blocks pulls; it does not select an account or repository automatically.

The local Compose tag remains `bbworkbench-toolbox:0.1.0`. The registry manifest digest and local image ID are different concepts. The helper verifies the installation's `image.lock.json` and refuses a new-host identity mismatch. Follow the workbench's `README.md` new-host verification before changing pins or creating plans. It does not build, execute or update tool binaries.

Caido configuration roles are separate: `CAIDO_API_URL` is management, `CAIDO_PROXY_URL` is target forwarding, `CAIDO_PROJECT_ID` is the expected project, and `CAIDO_CA_FILE` is the public interception certificate. Reuse the audited integration via `CAIDO_BRIDGE_CONFIG`; never migrate its tokens or install a competing proxy. Operator setup/audit is in the workbench's `docs/caido-integration.md` and `docs/skill-audit.md`. Browser identities A/B/anonymous require isolated profiles and evidence of identity; labels alone do not establish them.

As recorded on 11 October 2026, live Caido integration remains blocked, native bounty dispatch remains disabled, and all managed Katana execution refuses because version 1.7.0 attempted an excluded proxy-detection destination. A successful Docker start/pull does not resolve these blockers. Use the installation's current status over this dated summary if it has changed. Bootstrap tests use controlled local fixtures; no external target/provider calls.

This is cooperative supervised tooling. A skill, policy file or wrapper is not an execution sandbox. Preserve actual runtime gates and operator approval boundaries.
