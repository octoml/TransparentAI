# Run the main development flow.
dev:
	uvicorn tai-api.main:app --reload

# Setup to run the application locally.
setup:
	pip install -r requirements.txt

# Export Transformer Models
export:
	python
