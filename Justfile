# vim: set noexpandtab:
#

imageRegistry := "images.octoml.ai"
export OCTOML_AGREE_TO_TERMS := "1"

# list tasks
default:
	just --list

# build model container
build-model:
	echo Downloading Model
	mkdir -p models/tensorflow_models
	[ -f models/tensorflow_models/magenta_arbitrary-image-stylization-v1-256_2.tar.gz ] || wget https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2?tf-hub-format=compressed -O models/tensorflow_models/magenta_arbitrary-image-stylization-v1-256_2.tar.gz

	echo Building Model server
	cd models/tensorflow_models && octoml clean -c && rm -fr .octoml_cache
	docker rmi magenta_image_stylization-local || true
	cd models/tensorflow_models && octoml package -i
	docker tag magenta_image_stylization-local transparent-ai/style

# local development - compose build
compose-build:
	docker-compose build

# local development - compose up
compose-up: compose-build
	docker-compose up -d

# local development - compose down
compose-down:
	docker-compose down

# explicity build images
docker-build: build-model
	echo Tagging Model Server
	docker tag magenta_image_stylization-local {{imageRegistry}}/style

	echo Building API server
	cd api && docker build -t transparent-ai/api .
	docker tag transparent-ai/api {{imageRegistry}}/api

	echo Building Frontend
	cd frontend && docker build -t transparent-ai/frontend .
	docker tag transparent-ai/frontend {{imageRegistry}}/frontend

# push images to a registry
docker-push:
	docker push {{imageRegistry}}/style
	docker push {{imageRegistry}}/api
	docker push {{imageRegistry}}/frontend

# install helm chart for the first time
helm-install:
	echo "did you create the pull-secret? See readme"
	cd deploy/helm && helm install transparentai . -n transparentai

# sync helm files with deployment
helm-upgrade:
	echo "upgradin"
	cd deploy/helm && helm upgrade transparentai . -n transparentai

bounce-api-frontend:
    echo "bouncing pods"
    kubectl get pod -l app=transparentai-api
    kubectl delete pod -l app=transparentai-api
    sleep 2
    kubectl get pod -l app=transparentai-imagefrontend
    kubectl delete pod -l app=transparentai-imagefrontend
    sleep 2
    kubectl get pod

validate-k8s-auth:
	kubectl get pod

validate-plausible-imagereg:
	[ {{imageRegistry}} != images.octoml.ai ]

validate-main:
	[ $(git branch --show-current) = "main" ]

validate-ready-to-deploy: validate-k8s-auth validate-plausible-imagereg validate-main
	echo "validating deploy"

roll-site: validate-ready-to-deploy docker-build docker-push helm-upgrade bounce-api-frontend
	echo "Bouncing/bounced"
