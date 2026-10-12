# Canonical repository transfer

Use this contract when saving or connecting the managed website to the user's GitHub, returning it to Manus, or continuing/canceling an in-progress switch. Ordinary Git branches and commits do not themselves change the managed repository. Keep a repository command separate from ordinary configuration writes.

Describe the Manus storage destination as a **Manus-managed repository** (the UI label is **Managed by Manus**). Keep infrastructure provider names out of user-facing explanations.

Saving the project to the user's GitHub uses this connection workflow unless the user requests
only a separate backup. A backup does not switch the project's active repository.

Use `webdev.config`, not a GitHub connector or `gh repo create`. The platform confirmation creates the authorized target and grants temporary transport access; another tool cannot perform the managed switch.

## 1. Prepare and obtain owner confirmation

Read the current configuration, then send `PUT <config-plane>/config/git` with one command:

```json
{"git":{"canonical":{"provider":"github"}}}
```

To return to Manus:

```json
{"git":{"canonical":{"provider":"manus"}}}
```

`git.canonical` is request-only, not stored configuration. The current provider comes from the sibling `git_repository` in `GET config`. Omitting `git` never disconnects. An already active provider without an in-progress change is a no-op.

For GitHub, optional `owner` and `name` are confirmation prefills, not authorization. They are trimmed 1–100-character slugs with alphanumeric endpoints and alphanumerics, `.`, `_`, or `-` internally. The owner confirms a **new private repository**; existing-repository adoption, rebind, `visibility`, `branch`, and `mode` are unsupported. A Manus command has no owner/name. Use the confirmed target, not an earlier prefill.

`409 confirmation_required` returns the existing repository/Disconnect confirmation card. Do not resubmit the command, request a token, or confirm on the owner's behalf. The registered tool controls waiting and notification resumption.

The card is already displayed by `webdev.config`. Yield to its `agent_pause`; do not repeat the card link, ask the user to fill it out or send a follow-up message, or call a separate ask/wait tool. Saving the card emits `git_transfer_ready` and wakes Manus automatically. Resume at step 2 without another confirmation. On `git_transfer_cancelled`, acknowledge the cancellation and do not reopen the card.

**Confirmation only prepares the target. The original repository remains canonical until complete succeeds.** A ready card, a nonempty GitHub repository, or a successful push does not mean the website has switched.

For an adopted Cloud website that still uses its original repository, `webdev.manus_git` accepts `{"action":"fetch"}` or `{"action":"push"}`. Fetch updates `origin/main` without merging or resetting files; push sends the already-created HEAD and uses the usual checkpoint/logo/card processing. Make an intended commit separately. This Cloud tool is not available for ordinary Cloud/Game projects, which retain their terminal Git workflow. Local uses the separate `{command}` interface below.

## 2. Read the transfer and synchronize the workspace

After the confirmation notification, read `GET <config-plane>/config/git/transfer`; do not repeat Prepare. The response is `{ok:true,data:{transfer:...}}`, with operation ID, direction, status, expected revision, source/target, latest project checkpoint, and any required base commit in the Manus-managed repository.

In Cloud, for a ready operation, this `webdev.config` call safely prepares the temporary remote in the bound workspace and returns its actual `remoteName` and `workspaceReady`. Use that returned name only after preparation succeeds. Keep `origin` on the source; do not overwrite remotes, install another helper, or copy credentials. Native Git obtains short-lived, repository-scoped credentials through the existing helper.

In Local, a ready response reports `remoteName: "manus"`; this alias exists only inside each authorized `webdev.manus_git` command. Fetch the canonical source with `{"command":"git fetch manus"}`. Fetch or push the operation target using `{"transfer_operation_id":"<operationId>","command":"git fetch manus"}` or an explicit push refspec. Each call uses the same separate Managed Git object store but distinct tracking refs returned as `remote_refs`; save the source SHA before selecting the target. The server resolves the target from the confirmed operation; never pass a repository URL or credential. Transfer-target calls do not record checkpoints or publish. Existing separate user Git and its remotes/index remain independent. When the website's root gitfile points to Managed Git, ordinary terminal Git shares that Managed repository and index; file changes are always visible to both workflows. Do not install Cloud helper files locally.

Inspect current work and fetch the source before choosing what to push. **The latest accepted checkpoint is project-wide, not the current session's HEAD.** If another session advanced main from C to D, the transfer must include D even when this workspace was opened at C. Fetching is not permission to reset, clean, stash, or overwrite uncommitted work. Inspect conflicts and preserve both sides; never force-push to make completion pass.

A reminder means the operation is still pending. Prioritize its remaining work and call complete or explain the blocker; it is not permission to skip checks. Re-read state after recovery instead of trusting cached remote metadata.

If preparation needs attention and no ready target is returned, do not push or repeat repository creation. A network/DB failure may have happened after GitHub created the repository. Explain the uncertainty and abort the operation if it cannot continue; keep the source active and never delete that repository automatically. Any new attempt needs its own owner confirmation.

## 3a. Connect to GitHub

Push an explicit source commit/ref to the temporary remote's `refs/heads/main`, using a normal push. The source main must contain the latest checkpoint reported by the server. When working on a feature branch, source main and that branch are separate refs: **do not merge the feature into main merely to copy it**.

Preserve other branches and tags requested by the user, including relevant locally created branches as well as source-remote branches. Fetch the source refs you need; one session cannot discover another session's unshared local-only branch. Push explicit refspecs without `--mirror`, deleting refs, or uploading internal refs. Check the requested branches' push outcomes before saying they were transferred. Uncommitted/ignored files, secrets, unrelated directories, LFS objects and submodule repositories are not covered by blindly pushing Git refs.

The platform completion check covers main, not all branches/tags. If requested branch transfers fail, explain that remaining work rather than claiming everything is done.

## 3b. Return to Manus: snapshot recovery, not GitHub-history import

Obtain the **current latest accepted checkpoint D** from the source GitHub repository and fetch the expected main commit in the Manus-managed repository through the temporary remote. Preserve the user's worktree/index and branches.

Create a new commit R using D's tree and the expected main commit in the Manus-managed repository as its sole parent. `git commit-tree` can create this commit without checking out or rewriting the working tree. If the Manus-managed repository is explicitly reported empty, R has no parent. **Do not use GitHub's D as a parent, merge the two histories, or push all GitHub branches/tags into the Manus-managed repository.** Push only R to main in the Manus-managed repository without force.

GitHub changes not yet accepted as a checkpoint must first go through ordinary checkpoint recording if the user wants them included. Complete verifies the exact tree and permitted parent, so it cannot be satisfied by substituting an older snapshot or importing history. A concurrent new checkpoint or change to main in the Manus-managed repository requires refreshed state and recovery from the new boundary.

## 4. Complete or abort

After the required transfer succeeds, send `POST <config-plane>/config/git/complete` with:

```json
{"operationId":"<returned operation ID>","expectedRevision":42}
```

Use the returned revision, not the example value. For snapshot recovery, also pass `targetSha` with the full recovery commit R SHA.

For GitHub, the server freshly verifies that target main **equals or descends from the latest accepted checkpoint**. A checkpoint present only on another branch does not qualify. For Manus, it verifies main in the Manus-managed repository equals R, R's tree matches D and its parent matches the expected base commit in the Manus-managed repository. The final transaction rejects changed checkpoint/revision or an aborted operation. Complete does not silently record extra GitHub commits as checkpoints.

Only a successful complete response with `transfer.status: "completed"` establishes the switch. Read back configuration when needed; subsequent ordinary Git/checkpoint work uses the newly canonical repository. Cloud runtime synchronization aligns its managed origin. Local resolves the current canonical target on every ordinary `manus_git` call, without changing user remotes. After snapshot recovery, fetch R and inspect Managed Git history before saving again: new Manus checkpoints must descend from R. Preserve working files and ordinary Git; do not push the old GitHub HEAD back to Manus or force-push.

If blocked, explain why. If continuing is not feasible or the user asks to stop, send `POST <config-plane>/config/git/abort` with the same operation ID and expected revision. Keep the source canonical. **Abort does not undo a push or delete the target repository.** Do not delete the user's GitHub repository, force-revert its refs, or pretend issued credentials vanish instantly. A completed operation cannot be aborted; start a separately confirmed reverse operation.

If push or complete timed out, read the same operation and inspect the actual remote state before retrying. Do not recreate the repository or replay a compound shell command blindly. A rejected completion leaves the source canonical; refresh/integrate the latest checkpoint and retry only the remaining step.

After disconnect, the restored R is a new Manus version. GitHub-only old versions are not automatically republishable, and this project no longer accesses GitHub. Existing deployments are not deleted or republished by switching.


## Boundaries and failures

Canonical switching is unavailable for Mobile Dev. Local Website/Game use the same owner-confirmed transfer protocol with the separate Managed Git transport; ordinary user Git is outside this command domain. GitHub Actions remain unavailable on the managed canonical repository in this phase. Dashboard publishing retains its ordinary checkpoint and confirmation rules.

| Code | Next step |
| --- | --- |
| `confirmation_required` | Wait for the owner through the registered card flow. |
| `canonical_changed` | Refresh the operation, binding and latest checkpoint before continuing. |
| `checkpoint_restore_required` | Complete the latest snapshot recovery; do not disconnect early. |
| `checkpoint_missing` | The project has no saved checkpoint. Save one through the ordinary checkpoint workflow, then reread the transfer. |
| `checkpoint_not_transferred` | Target main does not contain the latest checkpoint. Transfer it from the source and integrate it into target main, then retry complete. Keep the source active; do not wait for an API outage or force-push. |
| `history_diverged` / `unrelated_history` | Preserve both histories and resolve explicitly; do not force-push. |
| `github_connector_required` / `github_installation_required` | Restore the platform's owner connection/App authorization; do not replace the flow with a connector tool. |
| `github_repository_forbidden` / `github_unauthorized` / `github_repository_detached` | Resolve access to the confirmed repository. |
| `github_repository_conflict` / `github_repository_not_empty` | Resolve the target with the owner, without overwriting unrelated content. |
| `github_unreachable` | Leave the source active and retry after the network/API problem is resolved. |

The common envelope is in [configuration](configuration.md). Ordinary transport and checkpoint receipts remain in [Git/checkpoints](git-checkpoints.md).
