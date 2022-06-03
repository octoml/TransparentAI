# Run the main development flow.
dev:
	uvicorn tai-api.main:app --reload --port 9000

# Setup to run the application locally.
setup:
	pip install -r requirements.txt
	mkdir -p models/onnx_models
	wget https://github.com/onnx/models/raw/main/text/machine_comprehension/gpt-2/model/gpt2-lm-head-10.onnx -P models/onnx_models
	cd ariel; poetry build; pip install dist/ariel-0.1.0-py3-none-any.whl --force-reinstall

# Export Transformer Models
export:
	python
