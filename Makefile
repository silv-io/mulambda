VENV_BIN ?= python -m venv
VENV_DIR ?= .venv
PIP_CMD ?= pip
VENV_ACTIVATE = $(VENV_DIR)/bin/activate
VENV_RUN = . $(VENV_ACTIVATE)

usage:                    ## Show this help
	@grep -Fh "##" $(MAKEFILE_LIST) | grep -Fv fgrep | sed -e 's/:.*##\s*/##/g' | awk -F'##' '{ printf "%-25s %s\n", $$1, $$2 }'

venv: $(VENV_ACTIVATE)    ## Create a new (empty) virtual environment

freeze:                   ## Run pip freeze -l in the virtual environment
	@$(VENV_RUN); pip freeze -l

entrypoints:              ## Run setup.py develop to build entry points
	$(VENV_RUN); python setup.py egg_info
	# make sure that the entrypoints were correctly created and are non-empty
	test -s mulambda.egg-info/entry_points.txt || (echo "Entrypoints were not correctly created! Aborting!" && exit 1)

install-dev: venv         ## Install developer requirements into venv
	$(VENV_RUN); $(PIP_CMD) install $(PIP_OPTS) -e ".[dev]"

install: install-dev entrypoints  	  ## Install into venv and build entry points