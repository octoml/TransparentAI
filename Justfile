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
	mkdir -p models/onnx_models
	mkdir -p tai-api/models/onnx_models
	[ -f models/onnx_models/gpt2-lm-head-10.onnx ] || wget https://github.com/onnx/models/raw/main/text/machine_comprehension/gpt-2/model/gpt2-lm-head-10.onnx -P models/onnx_models
	[ -f tai-api/models/onnx_models/gpt2-lm-head-10.onnx ] || wget https://github.com/onnx/models/raw/main/text/machine_comprehension/gpt-2/model/gpt2-lm-head-10.onnx -P tai-api/models/onnx_models
	[ -f models/tensorflow_models/magenta_arbitrary-image-stylization-v1-256_2.tar.gz ] || wget https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2?tf-hub-format=compressed -O models/tensorflow_models/magenta_arbitrary-image-stylization-v1-256_2.tar.gz
	[ -f models/onnx_models/mosaic-9.onnx ] || wget https://github.com/onnx/models/raw/main/vision/style_transfer/fast_neural_style/model/mosaic-9.onnx -P models/onnx_models


# Export Transformer Models
export:
	python

# build all docker images
docker-build:
	echo Building docker images
	echo Node App
	cd chat && docker build -t transparent-ai/chat .
	docker tag transparent-ai/chat {{imageRegistry}}/chat

	echo Image Frontend
	cd imagefrontend && docker build -t transparent-ai/imagefrontend .
	docker tag transparent-ai/chat {{imageRegistry}}/imagefrontend

	echo OctoML model server [gpt]
	[ -f models/onnx_models/gpt2-lm-head-10.onnx ] || wget https://github.com/onnx/models/raw/main/text/machine_comprehension/gpt-2/model/gpt2-lm-head-10.onnx -P models/onnx_models
	rm -fr .octoml_cache
	cd models/onnx_models && octoml clean -c
	docker rmi gpt2-lm-head-10-local || true
	cd models/onnx_models && octoml package -i
	docker tag gpt2-lm-head-10-local transparent-ai/gpt2-lm-head-10-local
	docker tag gpt2-lm-head-10-local {{imageRegistry}}/gpt2

	echo OctoML model server [style]
	rm -fr .octoml_cache
	[ -f models/tensorflow_models/magenta_arbitrary-image-stylization-v1-256_2.tar.gz ] || wget https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2?tf-hub-format=compressed -O models/tensorflow_models/magenta_arbitrary-image-stylization-v1-256_2.tar.gz
	cd models/tensorflow_models && octoml clean -c && rm -fr .octoml_cache
	docker rmi magenta_arbitrary-image-stylization-v1-256_2-local || true
	cd models/tensorflow_models && octoml package -i
	docker tag magenta_arbitrary-image-stylization-v1-256_2-local transparent-ai/style
	docker tag magenta_arbitrary-image-stylization-v1-256_2-local {{imageRegistry}}/style


	echo ML API Server
	mkdir -p tai-api/models/onnx_models
	cp models/onnx_models/gpt2-lm-head-10.onnx tai-api/models/onnx_models/
	echo python api server
	cd tai-api && docker build -t transparent-ai/tai-api .
	docker tag transparent-ai/tai-api {{imageRegistry}}/tai-api

# push images to registry 
push: docker-build
	docker push {{imageRegistry}}/tai-api
	docker push {{imageRegistry}}/chat
	docker push {{imageRegistry}}/gpt2
	docker push {{imageRegistry}}/style
	docker push {{imageRegistry}}/imagefrontend

# up localdev
compose-up:
	docker-compose up -d

# down localdev
compose-down:
	docker-compose down
