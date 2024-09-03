# Makefile used to build the collection docs

ANSIBLEGALAXYBUILD ?= ansible-galaxy
ANSIBLEGALAXYOPTS  ?= --token="${ANSIBLE_GALAXY_TOKEN}" 
ANTSIBULLBUILD     ?= antsibull-docs
ANTSIBULLOPTS	   ?=
SPHINXBUILD        ?= sphinx-build
SPHINXOPTS         ?=

.PHONY: docs

docs:
	@$(ANTSIBULLBUILD) "collection" "--use-current" "--squash-hierarchy" "--dest-dir=docs/" "evertrust.horizon" $(ANTSIBULLOPTS)
	@$(SPHINXBUILD) "docs/" "docs/html/" $(SPHINXOPTS)

build: clean
	@$(ANSIBLEGALAXYBUILD) "collection" "build" "--output-path=build/" $(ANSIBLEGALAXYPOTS)

clean: ## Clean build artifacts
	@rm -f build/*
	
publish: build ## Build and publish build artifact to Ansible Galaxy
	@ARTIFACT=$$(find "build" -name "*.tar.gz" ); \
	echo $$ARTIFACT; \
	$(ANSIBLEGALAXYBUILD) "collection" "publish" $$ARTIFACT $(ANSIBLEGALAXYPOTS)
