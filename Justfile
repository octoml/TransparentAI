# vim: set noexpandtab:
#

imageRegistry := "images.octoml.ai"
export OCTOML_AGREE_TO_TERMS := "1"


# List tasks
default:
	just --list

# Run the main development flow.
# Note that it may be easier to docker-compose up, then turn off the service you want to dev on and dev that locally
dev:
	cd chat && npm install && npm start &
	cd tai-api && uvicorn main:app --reload --port 9000

# Setup to run the application locally.
setup:
	pip install -r requirements.txt
	mkdir -p models/onnx_models
	mkdir -p tai-api/models/onnx_models
	[ -f models/onnx_models/gpt2-lm-head-10.onnx ] || wget https://github.com/onnx/models/raw/main/text/machine_comprehension/gpt-2/model/gpt2-lm-head-10.onnx -P models/onnx_models
	[ -f tai-api/models/onnx_models/gpt2-lm-head-10.onnx ] || wget https://github.com/onnx/models/raw/main/text/machine_comprehension/gpt-2/model/gpt2-lm-head-10.onnx -P tai-api/models/onnx_models

# Export Transformer Models
export:
	python

# build all docker images
docker-build:
	echo Building docker images
	echo Node App
	cd chat && docker build -t transparent-ai/chat .
	docker tag transparent-ai/chat {{imageRegistry}}/chat

	echo OctoML model server
	[ -f models/onnx_models/gpt2-lm-head-10.onnx ] || wget https://github.com/onnx/models/raw/main/text/machine_comprehension/gpt-2/model/gpt2-lm-head-10.onnx -P models/onnx_models
	rm -fr .octoml_cache
	cd models/onnx_models && octoml clean -a
	docker rmi gpt2-lm-head-10-local || true
	cd models/onnx_models && octoml package
	docker tag gpt2-lm-head-10-local transparent-ai/gpt2-lm-head-10
	docker tag gpt2-lm-head-10-local {{imageRegistry}}/gpt2

	mkdir -p tai-api/models/onnx_models
	cp models/onnx_models/gpt2-lm-head-10.onnx tai-api/models/onnx_models/
	echo python api server
	cd tai-api && docker build -t transparent-ai/tai-api .
	docker tag transparent-ai/tai-api {{imageRegistry}}/tai-api

# push images to registry 
push:
	docker push {{imageRegistry}}/tai-api
	docker push {{imageRegistry}}/chat
	docker push {{imageRegistry}}/gpt2

# up localdev
compose-up:
	docker-compose up -d

# down localdev
compose-down:
	docker-compose down
