# Contributing

### Development environment

The managed environment uses Python 3.11 and supports `ansible-core` 2.19.11
through 2.20. Install the runtime and test dependencies with:

```shell
mise install
mise run static_test
```

The Horizon SDK distribution is named `evertrust-horizon`; its Python import
name is `horizon`.

Run the licensed single-image integration suite with:

```shell
HORIZON_LICENSE_PATH=/path/to/licence.txt \
HORIZON_IMAGE=quay.io/evertrust/horizon:2.10.4 \
HORIZON_SDK_VERSION=2.10.0 \
mise run container_integration_test
```

The test workflow can also be started manually with a fully qualified
`quay.io` image tag or digest and one of the supported SDK release lines.
Each line resolves to its latest patch release. Manual tags are resolved and
reported by digest during the run.

Publication builds the collection artifact once, runs static checks against
that artifact, and then verifies the same artifact across the latest SDK patch
from each 2.8/2.9/2.10 line and pinned Horizon 2.8.10/2.9.4/2.10.4
cross-product. Publication cannot start unless all nine compatibility cells
pass.

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
  collection against the full licensed SDK/Horizon compatibility matrix.
