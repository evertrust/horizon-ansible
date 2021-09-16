# Contributing

### Documentation
In order to generate the documentation for the collection, you'll need to install both `antsibull` and `sphinx` with the `sphinx-ansible-theme` :

```shell
pip install antsibull
pip install sphinx
pip install sphinx-ansible-theme
```

Once everything is installed, navigate to the project root and run :
```
make docs
```
This will build the docs in the `docs/html` folder.

If your `antsibull-docs` or `sphinx-build` binaries aren't located in your `PATH`, you can pass them to the Makefile via environment variables :

```shell
SPHINXBUILD=<sphinx-build location> ANTSIBULLBUILD=<antsibull-docs location> make docs
```

### Notes

- Every interaction is Horizon is implemented trough action plugins, so that they're executed on the host. Modules in the `modules/` are empty and present for documentation purposes. 