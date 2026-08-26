---
name: handover
description: Transfer the active project, working state, and reproducible setup to a configured remote home server when the user asks to hand over, move, or continue work remotely.
---

# Home Server Handover

Move the current work to the server described in `server.json` and leave it ready to resume.

## Connection

Read `server.json` before any network action. Treat blank `host` or `username` fields as unconfigured and ask the user to fill them; never guess connection details. Use the configured SSH port and the caller's existing SSH agent or identity. Do not store passwords, private keys, tokens, or passphrases in this skill.

Stop and report the problem if the SSH host key changes, authentication fails, or the resolved destination is unsafe. Do not bypass host-key verification.

## Workflow

1. Identify the current project root, active branch or revision, uncommitted changes, and the files needed to reproduce the work. Inspect setup manifests such as lockfiles, container definitions, tool-version files, and environment examples.
2. Use `remote_root` from `server.json`. Unless the user names an existing destination, create a new child directory based on the project name and timestamp; never overwrite or delete an existing remote project implicitly.
3. Preflight the connection with Tailscale when available, then use non-interactive SSH to verify the remote user, host, free space, and destination permissions.
4. Transfer the working tree with SSH/SCP, SFTP, rsync, or a streamed archive, choosing the method available on both systems. Preserve dotfiles, executable bits, Git state when appropriate, and files that describe the setup.
5. Exclude regenerable dependency/build directories and sensitive material by default, including `.env` files other than examples, private keys, credential stores, `.ssh`, `node_modules`, virtual environments, caches, and build output. If excluded material is required, list it and ask the user how it should be provisioned securely.
6. Add a `HANDOVER.md` inside the remote destination that records the objective, current status, source path, revision and dirty state, important commands, setup requirements, verification performed, and the next concrete action. Do not add this file to the local project unless requested.
7. Recreate only project-scoped setup that can be inferred reliably from the project's own manifests. Ask immediately before using `sudo`, changing services, firewall or system configuration, installing system-wide packages, replacing remote configuration, or exposing ports.
8. Verify transferred file integrity, run a proportionate project check when practical, and remove only temporary transfer archives created by this handover.

Do not delete or modify the local source as part of a handover. Do not start a remote Codex process, background service, or long-running job unless the user asks for it.

Finish with the remote destination, transferred and excluded items, setup actions, verification result, and the exact SSH/resume command.
