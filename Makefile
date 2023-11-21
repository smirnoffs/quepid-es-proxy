.PHONY: lint prepare-env tests

# Removes the existing virtualenv, creates a new one, install dependencies.
prepare-env:
	rm -rf .venv
	python3.11 -m venv .venv
	.venv/bin/pip install -U pip
	.venv/bin/pip install -r requirements-dev.txt


lint:
	.venv/bin/ruff format .

tests:
	PYTHONPATH=`pwd` .venv/bin/pytest -vv -W ignore tests/units --cov-report xml:cov.xml --cov .

run-server:
	PROXY_USERNAME="lab_user" \
	PROXY_PASSWORD="jhHB73bYBKk6G^" \
	ES_HOST="localhost" ES_PORT=9200 ES_USE_SSL=false \
	WEB_CONCURRENCY=2 \
	.venv/bin/uvicorn quepid_es_proxy.main:app \
	--reload \
	--port 5000 \
	--host localhost \
	--use-colors \
	--access-log \


# Docker part
IMAGE="quay.io/amboss-mededu/quepid_es_proxy"
IMAGE_TAG=latest

.PHONY: image-build image-push
image-build:
	docker build -t $(IMAGE):$(IMAGE_TAG) .

image-push:
	docker push $(IMAGE):$(IMAGE_TAG)