# Bounty preparation skill

A Codex skill for preparing a supervised Caido workbench session. It initializes an absent private deny-all program, optionally starts Docker Desktop and prepares a pinned toolbox image, and reports setup blockers. Preparation sends no target requests and does not grant testing permission.

## Prerequisites

- A separately installed, trusted `bbworkbench` checkout with its existing `AGENTS.md`, `init.md`, `IMPLEMENTATION_STATUS.md`, `uv.lock`, `image.lock.json` and `src/bbworkbench` implementation. The Python CLI and workbench dependencies are not included here.
- Python 3.12+ from that workbench's bootstrapped environment.
- Windows Docker Desktop with the local `desktop-linux` context and Linux amd64 engine for optional Docker preparation. Other Docker platforms are not validated by this helper.
- Either the existing verified local `bbworkbench-toolbox:0.1.0` image or access to an operator-selected, immutable registry image compatible with the workbench lock. No registry account, image digest, credentials or image contents are distributed here.

## Install in a project

Copy `skills/bounty-prep` into the chosen project's `.agents/skills/bounty-prep`. Set `BB_WORKBENCH_ROOT` in your local session to the absolute trusted workbench path, then invoke:

```text
$bounty-prep initialize program acme
```

If needed, restart Codex to discover the new skill. Follow the project's existing instructions and filesystem permissions. Installation does not require changing global skills.

For a shell invocation, replace the example paths with your local installation and copied skill directory:

```powershell
$env:BB_WORKBENCH_ROOT = 'C:\path\to\trusted-workbench'
$skillRoot = 'C:\path\to\project\.agents\skills\bounty-prep'
& (Join-Path $env:BB_WORKBENCH_ROOT '.venv\Scripts\python.exe') (Join-Path $skillRoot 'scripts\prepare.py') --program acme --init-draft --start-docker --pull-image
```

Omit the three mutation switches for inspection only. Initialization preserves an existing program's policy and stop state. A registry pull requires `BB_TOOLBOX_IMAGE` or `--registry-image` in the form `<registry>/<namespace>/<image>@sha256:<64-hex-digest>`; supply your own verified reference privately. Mutable tags are refused. The helper reuses an existing matching local toolbox without requiring a registry setting. It never logs in, reads credential stores or changes the image lock.

`DATA_ROOT` and `SECRET_ROOT` are separate private directories outside the workbench and target project. On Windows the defaults are under `LOCALAPPDATA\BBWorkbench`. Keep the same roots for subsequent CLI calls and the operator's approval terminal. Optional `--data-root` and `--secret-root` arguments affect only that helper process. `--synthetic-fixture` is for explicit offline synthetic validation and prohibits startup/pulls.

## Publishing and local configuration

This package contains the skill, this README and `.gitignore`. It excludes `workbench.json`, private data, evidence, credentials, caches and host-specific verification reports. An optional locally generated `workbench.json` is supported for convenience but must remain untracked. Do not add actual machine paths, registry account details or engagement content to public instructions. Environment-variable names and generic example paths in this package are configuration interfaces, not stored values.

This skill depends on the separate workbench; it is not a standalone scanner or execution sandbox. Live Caido validation, policy/data-sharing review, operator approval and existing native-tool refusals remain prerequisites for later work. Docker startup/pull handling has been mock-tested; this distribution makes no new live integration claim. It does not change Caido projects/listeners, token stores, host trust or firewall settings, execute response content, resume stopped work or launch reconnaissance automatically.
