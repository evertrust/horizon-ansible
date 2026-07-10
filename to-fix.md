# To Fix

Fresh Makefile-to-mise and GitHub Actions review, 2026-07-10.

Only this tracking file was created. Findings reflect the current worktree, including the in-progress Syft/Grype rewrite in `.github/workflows/scan.yml`.

## Priority Summary

| ID | Severity | Area | Summary |
| --- | --- | --- | --- |
| SEC-PUBLISH-001 | High | Galaxy token | Manual publishing has no protected environment or trusted-ref validation. |
| CI-PUBLISH-001 | High | Release correctness | `release_check` invokes integration tests without the required Horizon secrets. |
| MISE-PUBLISH-001 | Medium | Task graph | `publish` does not build or validate the artifact it publishes. |
| CI-TEST-001 | Medium | Test coverage | Tests run only after pushes to `main`, and unit tests are blocked behind secret-dependent integration tests. |
| MISE-REPRO-001 | Medium | Reproducibility | mise, Python, Ansible, and Python dependencies are not fully pinned or locked. |
| MISE-DOCS-001 | Medium | Portability | `docs_build` relies on non-portable, non-idempotent in-place `sed` behavior. |
| CI-SCAN-002 | Medium | Detection | High findings remain non-blocking and artifact-only. |
| SEC-ANSIBLE-001 | Low | Plugin secrets | Lookup and inventory authentication bypass the action-plugin masking path. |
| DOCS-001 | Low | Documentation | Contributor documentation still says documentation generation needs a Galaxy token. |
| CI-HARDEN-001 | Low | Workflow hardening | Long-running jobs have no explicit timeouts. |

## High

### [ ] SEC-PUBLISH-001: Protect and bind manual releases to an approved ref

Files:
- `.github/workflows/publish.yaml:2-3`
- `.github/workflows/publish.yaml:9-33`
- `mise.toml:85-106`

The manual workflow has no `environment` and no ref, tag, or version validation. A dispatcher can select a ref whose repository-controlled `mise publish` task runs with the Galaxy token. Branch protection on `main` alone does not constrain a manually selected ref.

Fix:
- Attach the job to a dedicated protected release Environment with required reviewers and no self-approval.
- Restrict publication to an expected tag/ref and verify that the tag and `galaxy.yml` version agree.
- Build a fresh artifact from that exact reviewed commit and publish only that artifact.
- Keep the current step-only token mapping and temporary `0600` token-file pattern.

### [ ] CI-PUBLISH-001: Make the release check runnable on a fresh runner

Files:
- `.github/workflows/publish.yaml:27-33`
- `mise.toml:77-79`
- `mise.toml:108-115`

`release_check` depends on `test`, which now correctly creates its integration config only after the collection is built and installed. The publish workflow still does not supply `HORIZON_ENDPOINT`, `HORIZON_API_ID`, or `HORIZON_API_KEY`, so a clean release runner fails fast before integration tests can run.

Fix:
- Split unit and integration tasks so the release job can run deterministic checks without hidden state.
- If integration is a release gate, provision its secrets through a protected Environment and retain the current secure post-install config lifecycle.

## Medium

### [ ] MISE-PUBLISH-001: Restore the publish task's build dependency

Files:
- `mise.toml:85-106`

The task description says it builds and publishes, and the old Make `publish` target depended on `build`, but the mise task has no dependency. `mise run publish` therefore publishes whichever single tarball happens to be in `build/`, including a stale artifact.

Fix:
- Make the publish path produce a fresh, clean artifact from the current commit and validate its manifest before publication.
- Keep the workflow release checks explicit if integration secrets should not be implicit dependencies of a local publish task.

### [ ] CI-TEST-001: Split secretless unit CI from protected integration CI

Files:
- `.github/workflows/run_test.yaml:2-5`
- `.github/workflows/run_test.yaml:24-37`
- `mise.toml:108-115`

The only test trigger is a push to `main`, so pull requests receive no pre-merge test signal. The single task runs integration first and unit second; missing credentials, endpoint downtime, or an integration failure prevents unit tests from running. Repository integration secrets are exposed to repository code on every main push.

Fix:
- Run unit tests as a separate secretless job for `pull_request` and `push`.
- Run integration tests in a separate job with explicit trusted-ref policy, a protected Environment where appropriate, a timeout, and secure config cleanup.

### [ ] MISE-REPRO-001: Pin the execution stack and dependency freshness inputs

Files:
- `mise.toml:1-19`
- `.github/workflows/build_doc.yaml:24-25`
- `.github/workflows/publish.yaml:15-25`
- `.github/workflows/run_test.yaml:21-22`

The action commit is pinned, but `jdx/mise-action` installs the latest mise release when `with.version` is omitted. That is especially risky because `[deps]` is experimental. Python comes from each runner's system installation, `ansible` is unconstrained, most requirements are unpinned, and no lock file is present. The publish workflow also installs a distro Ansible before the auto dependency provider installs another Ansible into the venv.

The dependency marker watches only `requirements.txt`; changing the install commands or Ansible constraint in `mise.toml` does not invalidate an existing `.venv/.requirements.installed` on a reused workspace.

Fix:
- Pin mise with the action's `version` and `sha256` inputs consistently.
- Declare a supported Python version in `[tools]` and test any required compatibility matrix explicitly.
- Lock or constrain Ansible and Python packages, and include `mise.toml` plus the lock/constraints file in dependency freshness sources.
- Remove the redundant `apt-get install ansible` path once mise owns the toolchain.

### [ ] MISE-DOCS-001: Replace the generated-script `sed` patch

Files:
- `mise.toml:48-54`

`sed -i` without a backup suffix is GNU-specific and fails with BSD `sed` on macOS. Each repeated run also inserts another `reformat.py` invocation before the same `sphinx-build` line. The task mutates a generated shell script instead of invoking the two operations explicitly.

Fix:
- Run the reformatter and Sphinx commands explicitly, or patch the generated file with a portable, idempotent structured/scripted operation.
- Add task dependencies or a composite `docs` task so a clean checkout has one complete documented entry point.

### [ ] CI-SCAN-002: Make scheduled vulnerability findings actionable

Files:
- `.github/workflows/scan.yml:20-43`

`severity-cutoff: high` is neutralized as a gate by `fail-build: false`. The SARIF is only stored as a workflow artifact, and the previous Linear notification path has been removed. Scheduled high/critical findings can therefore produce a successful run with no durable code-scanning result or notification.

Fix:
- Either fail on the chosen severity or route SARIF/notifications to a monitored sink with the minimum required permission.

## Low

### [ ] SEC-ANSIBLE-001: Audit lookup and inventory secret handling

Files:
- `plugins/doc_fragments/auth_options.py:19-36`
- `plugins/lookup/horizon_lookup.py:320-343`
- `plugins/inventory/horizon_inventory.py:142-182`
- `plugins/module_utils/horizon_action.py:14-30`

Action plugins mark tasks as `no_log` when sensitive arguments are present, but lookup and inventory plugins instantiate `Horizon` directly and do not inherit that protection. The shared documentation fragment also does not mark `x_api_key` or `client_key` as sensitive metadata.

No current statement directly logs the authentication dictionary, so this review did not confirm an active value disclosure. The gap remains because both plugins forward Horizon error messages outside the action masking path, and future debug or exception changes could expose authentication inputs without a regression test detecting it.

Fix:
- Mark sensitive plugin options with supported `no_log` metadata and add explicit redaction where lookup/inventory plugin APIs do not honor it.
- Add failure-path tests using sentinel credentials and assert that exceptions, display output, and inventory parsing output never contain them.
- Document `no_log: true` for tasks containing secret-bearing lookup expressions and secure storage/permissions for inventory configuration credentials.

### [ ] DOCS-001: Remove the stale Galaxy-token wording from contributor docs

File:
- `CONTRIBUTING.md:10`

The command was correctly changed to `mise run docs_init` without a token, but its preceding sentence still says documentation generation uses an Ansible Galaxy token.

Fix:
- Remove the token reference and describe documentation generation as using the locally installed current collection.

### [ ] CI-HARDEN-001: Limit residual workflow credentials and runtime

Files:
- `.github/workflows/build_doc.yaml:15-44`
- `.github/workflows/publish.yaml:9-33`
- `.github/workflows/run_test.yaml:9-37`
- `.github/workflows/scan.yml:9-43`

All current checkout actions set `persist-credentials: false`. Jobs still lack `timeout-minutes`; integration, package installation, docs generation, and network-backed scanners can hang until the platform limit.

Fix:
- Add job-level timeouts sized for each workload; add Pages deployment concurrency if overlapping tag/manual deployments are possible.

## Confirmed Fixed or Validated

- Workflows contain no remaining `make` invocation, and every referenced mise task exists.
- `[deps.install_requirements]` is a valid auto dependency provider in the current mise implementation; it is automatically invoked before `mise run`. The earlier concern that it was not in the task dependency tree does not apply.
- The publish artifact check now rejects both multiple artifacts and an unmatched/nonexistent glob.
- Galaxy token handling in `publish` avoids command-line exposure, uses a temporary `0600` YAML token file, and removes it with a trap.
- The Galaxy token is scoped to the publish step rather than the release-check steps.
- `docs_init` and the docs workflow no longer receive or require `ANSIBLE_GALAXY_API_TOKEN`; `publish` is now the only mise task that needs it.
- All current checkout steps disable persistent Git credentials.
- Workflow and job permissions are explicit and least-privilege; the hosted scan now has only `contents: read`.
- Every current third-party action reference is pinned to a full commit SHA, and each version comment matches the corresponding tag, including the new Syft and Grype actions.
- The current scan rewrite removes Vault/Linear secret retrieval and the custom upload action, moves the scan off the EverTrust self-hosted runner, and avoids duplicate SBOM artifact uploads.
- Integration credentials are created only after the collection artifact is installed, use owner-only permissions and structured JSON/YAML serialization, and are removed by a shell exit trap.
- The collection manifest excludes integration config/template files, local environments, CI metadata, generated docs, build output, caches, and review files. A manifest probe confirmed those paths are absent from the tarball.
