# Contributing

### Licensed integration tests

The container integration suite tests the current handwritten Horizon client
against the latest configured Horizon release (currently 2.10.3). The
generated Horizon SDK is a test-only dependency used to provision and verify
the isolated Horizon container; the Ansible collection does not use it for
lifecycle requests on this branch.

Run the same suite locally with:

```shell
HORIZON_LICENSE_PATH=/path/to/licence.txt mise run container_integration_test
```

Older releases are tested manually when needed by overriding both
`HORIZON_VERSION` and the digest-pinned `HORIZON_IMAGE`.

CI follows the Horizon SDK workflow's infrastructure setup: it reads the Quay
credentials from `ci/data/repositories/evertrust/horizon-ansible/quay` and
the `licence` field from
`ci/data/repositories/evertrust/horizon-ansible/horizon`. It logs in to
`quay.io` before pulling the images, writes the licence to a temporary
mode-restricted file, and removes it after the run. Ansible and Horizon logs
are retained as workflow artifacts. The runner audits request-level warnings
and failures before considering an image successful.

### Documentation
Generate and build the documentation with `mise`:

```shell
mise run docs_build
```

This will build the docs in the `docs/build/html` folder.

### Notes

- Every interaction is Horizon is implemented trough action plugins, so that they're executed on the host. Modules in the `modules/` are empty and present for documentation purposes.
