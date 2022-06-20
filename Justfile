# vim: set noexpandtab:
#

imageRegistry := "images.octoml.ai"
export OCTOML_AGREE_TO_TERMS := "1"

# list tasks
default:
	just --list

# setup to download resources
setup:
	mkdir -p models/onnx_models
	mkdir -p models/tensorflow_models
	[ -f models/tensorflow_models/magenta_arbitrary-image-stylization-v1-256_2.tar.gz ] || wget https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2?tf-hub-format=compressed -O models/tensorflow_models/magenta_arbitrary-image-stylization-v1-256_2.tar.gz

# build all docker images
docker-build:
	echo Building docker images

	echo Building Frontend
	cd frontend && docker build -t transparent-ai/frontend .
	docker tag transparent-ai/frontend {{imageRegistry}}/frontend

	echo Building Model server
	rm -fr .octoml_cache
	[ -f models/tensorflow_models/magenta_arbitrary-image-stylization-v1-256_2.tar.gz ] || wget https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2?tf-hub-format=compressed -O models/tensorflow_models/magenta_arbitrary-image-stylization-v1-256_2.tar.gz
	cd models/tensorflow_models && octoml clean -c && rm -fr .octoml_cache
	docker rmi magenta_image_stylization-local || true
	cd models/tensorflow_models && octoml package -i
	docker tag magenta_image_stylization-local transparent-ai/style
	docker tag magenta_image_stylization-local {{imageRegistry}}/style

	echo Building API server
	cd api && docker build -t transparent-ai/api .
	docker tag transparent-ai/api {{imageRegistry}}/api

# push images to registry
push:
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
