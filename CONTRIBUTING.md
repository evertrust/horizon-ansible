# Contributing

### Documentation
Documentation tasks are managed with `mise`.

```shell
mise run install_init_deps_doc
```

Generate the Sphinx project from the locally installed collection:

```shell
mise run docs_init
```

Then build the HTML documentation:

```shell
mise run docs_build
```

This will build the docs in the `docs/build/html` folder.

### Notes

- Every interaction is Horizon is implemented trough action plugins, so that they're executed on the host. Modules in the `modules/` are empty and present for documentation purposes.
