# vim: set noexpandtab:
# Run the main development flow.
dev:
	uvicorn tai-api.main:app --reload --port 9000

# Setup to run the application locally.
setup:
	pip install -r requirements.txt
	mkdir -p models/onnx_models
	[ -f models/onnx_models/gpt2-lm-head-10.onnx ] || wget https://github.com/onnx/models/raw/main/text/machine_comprehension/gpt-2/model/gpt2-lm-head-10.onnx -P models/onnx_models

# Export Transformer Models
export:
	python

# build all docker images
build-docker:
	echo Building docker images
	cd chat && docker build -t chat .
