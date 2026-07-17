# Contributing

### Development environment

The managed environment uses Python 3.10 and supports `ansible-core` 2.15
through 2.20. Install the runtime and test dependencies with:

```shell
mise install
mise run static_test
```

The Horizon SDK distribution is named `Anto-test-hrz`; its Python import name
is `horizon`.

Run the licensed single-image integration suite with:

```shell
HORIZON_LICENSE_PATH=/path/to/licence.txt mise run container_integration_test
```

Older releases or candidate builds are tested manually when needed by
overriding `HORIZON_IMAGE` with another fully qualified `quay.io` image.

CI follows the Horizon SDK workflow's infrastructure setup: it reads the Quay
credentials from `ci/data/repositories/evertrust/horizon-ansible/quay` and
the `licence` field from
`ci/data/repositories/evertrust/horizon-ansible/horizon`. It logs in to
`quay.io` before pulling the images, writes the licence to a temporary
mode-restricted file, and removes it after the run. Ansible and Horizon logs
are retained as workflow artifacts.

### Documentation
Generate and build the documentation with `mise`:

```shell
mise run docs_build
```

This will build the docs in the `docs/build/html` folder.

### Notes

- Every interaction with Horizon is implemented through action plugins so it
  executes on the controller. Files in `plugins/modules/` provide documentation
  and argument specifications.
- Unit tests mock the generated SDK boundary. Release validation also runs the
  collection against one licensed Horizon image.
