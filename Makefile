# Makefile used to build the collection docs

ANSIBLEGALAXYBUILD ?= ansible-galaxy
ANSIBLEGALAXYOPTS  ?= --token="$(ANSIBLE_GALAXY_API_TOKEN)" 
ANTSIBULLBUILD     ?= antsibull-docs
ANTSIBULLOPTS	     ?=
SPHINXBUILD        ?= sphinx-build
SPHINXOPTS         ?=
ANSIBLETEST				 ?= ansible-test
COLLECTIONPATH     ?= ~/.ansible/collections/ansible_collections/evertrust/horizon

.PHONY: docs

docs:
	@$(ANTSIBULLBUILD) "collection" "--use-current" "--squash-hierarchy" "--dest-dir=docs/" "evertrust.horizon" $(ANTSIBULLOPTS)
	@$(SPHINXBUILD) "docs/" "docs/html/" $(SPHINXOPTS)

build: clean
	@$(ANSIBLEGALAXYBUILD) "collection" "build" "--output-path=build/" $(ANSIBLEGALAXYPOTS)

install: 
	ARTIFACT=$$(find "build" -name "*.tar.gz" ); \
	echo $$ARTIFACT; \
	$(ANSIBLEGALAXYBUILD) "collection" "install" $$ARTIFACT

clean: ## Clean build artifacts
	@rm -f build/*
	
publish: build ## Build and publish build artifact to Ansible Galaxy
	ARTIFACT=$$(find "build" -name "*.tar.gz" ); \
	echo $$ARTIFACT; \
	$(ANSIBLEGALAXYBUILD) "collection" "publish" $$ARTIFACT $(ANSIBLEGALAXYOPTS)

test: build install
	cd $(COLLECTIONPATH); \
	$(ANSIBLETEST) "integration"; \
	$(ANSIBLETEST) "units"