# vim: set noexpandtab:
#

imageRegistry := "images.octoml.ai"
export OCTOML_AGREE_TO_TERMS := "1"

# List tasks
default:
	just --list

# Setup to run the application locally.
setup:
	mkdir -p models/onnx_models
	# [ -f models/onnx_models/gpt2-lm-head-10.onnx ] || wget https://github.com/onnx/models/raw/main/text/machine_comprehension/gpt-2/model/gpt2-lm-head-10.onnx -P models/onnx_models
	# [ -f models/onnx_models/mosaic-9.onnx ] || wget https://github.com/onnx/models/raw/main/vision/style_transfer/fast_neural_style/model/mosaic-9.onnx -P models/onnx_models
	mkdir -p models/tensorflow_models
	[ -f models/tensorflow_models/magenta_arbitrary-image-stylization-v1-256_2.tar.gz ] || wget https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2?tf-hub-format=compressed -O models/tensorflow_models/magenta_arbitrary-image-stylization-v1-256_2.tar.gz

# build all docker images
docker-build:
	echo Building docker images

	echo Frontend
	cd frontend && docker build -t transparent-ai/frontend .
	docker tag transparent-ai/frontend {{imageRegistry}}/frontend

	echo Pre/Post Proc API Server
	cd api && docker build --no-cache -t transparent-ai/api .
	docker tag transparent-ai/api {{imageRegistry}}/api	

	echo OctoML model server [style]
	rm -fr .octoml_cache
	[ -f models/tensorflow_models/magenta_arbitrary-image-stylization-v1-256_2.tar.gz ] || wget https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2?tf-hub-format=compressed -O models/tensorflow_models/magenta_arbitrary-image-stylization-v1-256_2.tar.gz
	cd models/tensorflow_models && octoml clean -c && rm -fr .octoml_cache
	docker rmi magenta_image_stylization-local || true
	cd models/tensorflow_models && octoml package -i
	docker tag magenta_image_stylization-local transparent-ai/style
	docker tag magenta_image_stylization-local {{imageRegistry}}/style

# push images to registry
docker-push:
	docker push {{imageRegistry}}/api
	docker push {{imageRegistry}}/style
	docker push {{imageRegistry}}/frontend

# up localdev
compose-up:
	docker-compose up -d

# down localdev
compose-down:
	docker-compose down

# install helm chart for the first time
helm-install:
	echo "did you create the pull-secret? See readme"
	cd deploy/helm && helm install transparentai . -n transparentai

# sync helm files with deployment
helm-upgrade:
	echo "upgradin"
	cd deploy/helm && helm upgrade transparentai . -n transparentai
