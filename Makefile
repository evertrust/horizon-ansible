# Makefile used to build the collection docs

ANTSIBULLBUILD	?= antsibull-docs
ANTSIBULLOPTS	?=
SPHINXBUILD   	?= sphinx-build
SPHINXOPTS   	?=

.PHONY: docs

docs:
	@$(ANTSIBULLBUILD) "collection" "--use-current" "--squash-hierarchy" "--dest-dir=docs/" "evertrust.horizon" $(ANTSIBULLOPTS)
	@$(SPHINXBUILD) "docs/" "webdocs/" $(SPHINXOPTS)