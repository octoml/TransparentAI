# vim: set noexpandtab:
# Run the main development flow.
dev:
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
	octoml clean -a

	echo OctoML model server
	[ -f models/onnx_models/gpt2-lm-head-10.onnx ] || wget https://github.com/onnx/models/raw/main/text/machine_comprehension/gpt-2/model/gpt2-lm-head-10.onnx -P models/onnx_models
	rm -fr .octoml_cache
	docker rmi gpt2-lm-head-10 || true
	octoml package
	docker tag gpt2-lm-head-10 transparent-ai/gpt2-lm-head-10

	mkdir -p tai-api/models/onnx_models
	[ -f tai-api/models/onnx_models/gpt2-lm-head-10.onnx ] || wget https://github.com/onnx/models/raw/main/text/machine_comprehension/gpt-2/model/gpt2-lm-head-10.onnx -P tai-api/models/onnx_models
	echo python api server
	cd tai-api && docker build -t transparent-ai/tai-api .

compose-up:
	docker-compose up

compose-down:
	docker-compose down
