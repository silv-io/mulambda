VENV_BIN ?= python -m venv
VENV_DIR ?= .venv
PIP_CMD ?= pip
VENV_ACTIVATE = $(VENV_DIR)/bin/activate
VENV_RUN = . $(VENV_ACTIVATE)

$(VENV_ACTIVATE): requirements.txt
	test -d $(VENV_DIR) || $(VENV_BIN) $(VENV_DIR)
	$(VENV_RUN); $(PIP_CMD) install --upgrade pip setuptools
	touch $(VENV_ACTIVATE)

usage:                    ## Show this help
	@grep -Fh "##" $(MAKEFILE_LIST) | grep -Fv fgrep | sed -e 's/:.*##\s*/##/g' | awk -F'##' '{ printf "%-25s %s\n", $$1, $$2 }'

venv: $(VENV_ACTIVATE)    ## Create a new (empty) virtual environment

freeze:                   ## Run pip freeze -l in the virtual environment
	@$(VENV_RUN); pip freeze -l

install-dev: venv         ## Install developer requirements into venv
	$(VENV_RUN); $(PIP_CMD) install $(PIP_OPTS) --upgrade -e ".[dev]"

install-docker: venv      ## Install docker requirements into venv
	$(VENV_RUN); $(PIP_CMD) install $(PIP_OPTS) --no-cache-dir --upgrade -e "."

install-requirements: venv
	$(VENV_RUN); $(PIP_CMD) install $(PIP_OPTS) -r requirements.txt

install: install-dev  	  ## Install into venv

docker-build: venv        ## Build the docker image
	$(VENV_RUN)
	docker build -t agihi/mulambda .
	docker build -t agihi/mulambda-companion -f Dockerfile.companion .

docker-push: venv
	docker push agihi/mulambda
	docker push agihi/mulambda-companion

run: venv                 ## Run the application
	$(VENV_RUN); uvicorn mulambda.api.selector:app --host 0.0.0.0 --port 80

run-companion: venv
	$(VENV_RUN); python mulambda/api/companion.py

kube-deploy-mulambda:
	kubectl apply -f k8s/mulambda.yaml

init-pre-commit: venv     ## Install pre-commit hooks
	$(VENV_RUN); pre-commit install

clean: 				  	  ## Remove all build, test, coverage and Python artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -fr .tox/
	rm -fr .pytest_cache/
	rm -fr .venv
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete
	find . -name '__pycache__' -delete

.PHONY: usage venv freeze install-dev install clean
