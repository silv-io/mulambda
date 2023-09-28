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

install: install-dev  	  ## Install into venv

docker-build-latest:
	docker build -t agihi/mulambda:latest .

docker-push-latest: docker-build-latest
	docker push agihi/mulambda:latest

run: venv                 ## Run the application
	$(VENV_RUN); uvicorn mulambda.api.selector:app --host 0.0.0.0 --port 80

run-companion: venv
	$(VENV_RUN); mulambda-companion

run-client: venv
	$(VENV_RUN); uvicorn mulambda.api.client:app --host 0.0.0.0 --port 80

run-dummy: venv
	$(VENV_RUN); uvicorn mulambda.api.dummy:app --host 0.0.0.0 --port 80

run-experiment: venv
	$(VENV_RUN); mulambda-experiment

k3d-create:
	mkdir -p $(HOME)/k8s/volume
	k3d cluster create --volume $(HOME)/k8s/volume:/var/lib/rancher/k3s/storage@all --agents 4 --k3s-node-label "mulambda.vasiljevic.at/region=local@agent:0" --k3s-node-label "mulambda.vasiljevic.at/region=edge@agent:1" --k3s-node-label "mulambda.vasiljevic.at/region=datacenter@agent:2" --k3s-node-label "mulambda.vasiljevic.at/region=cloud@agent:3"

kube-deploy-infra:
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/dragonfly.yaml
	#kubectl apply -f k8s/minio.yaml


SELECTOR_TYPE ?= round-robin
#SELECTOR_TYPE ?= random
#SELECTOR_TYPE ?= plain-net-latency
#SELECTOR_TYPE ?= mulambda
export SELECTOR_TYPE
kube-deploy-selector:
	cat ./k8s/selector.yaml | envsubst | kubectl apply -f -

kube-upload-models:
	mcli ls localminio/models || mcli mb localminio/models
	mcli cp -r ./assets/models/* localminio/models

CLIENT_ID ?= $(SELECTOR_TYPE)-client
TARGET_SELECTOR ?= $(SELECTOR_TYPE)-selector
export CLIENT_ID TARGET_SELECTOR
kube-deploy-client:
	cat ./k8s/client.yaml | envsubst | kubectl apply -f -

MODEL_NAME ?= test_model
MODEL_ID ?= demo-model
MODEL_TYPE ?= dummy
MODEL_INPUT ?= floatvector
MODEL_OUTPUT ?= floatvector
MODEL_ACCURACY ?= 1.0
MODEL_PATH ?= /v1/models/$(MODEL_NAME):predict
MODEL_PORT ?= 8500
export MODEL_NAME MODEL_ID MODEL_TYPE MODEL_INPUT MODEL_OUTPUT MODEL_ACCURACY MODEL_PATH MODEL_PORT
kube-deploy-tf-model:
	cat ./k8s/tf-model.yaml | envsubst | kubectl apply -f -

DUMMY_MEAN ?= 500
DUMMY_STD ?= 100
export DUMMY_MEAN DUMMY_STD
kube-deploy-dummy-model:
	cat ./k8s/dummy-model.yaml | envsubst ##| echo ## kubectl apply -f -

EXP_NAME ?= test
EXP_ID ?= $(shell date +%Y%0m%0d%0k%0M%0S)
export EXP_NAME EXP_ID
kube-run-experiment-job:
	cat ./k8s/experiment.yaml | envsubst | kubectl apply -f -

MODEL_ID ?= 1
export MODEL_ID
test_model:
	source <(./k8s/set_model_env.sh ./k8s/dummy-models.csv)
	cat ./k8s/test | envsubst

kube-deploy-all: kube-deploy-infra kube-deploy-tf-model kube-deploy-client

kube-clear-completed-jobs:
	kubectl get jobs -n mulambda -o json | jq '.items[] | select(.status.completionTime) | .metadata.name' | xargs kubectl delete jobs

kube-clear-all-jobs:
	kubectl delete jobs -n mulambda --all

kube-teardown-all:
	kubectl delete all --all -n mulambda

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
