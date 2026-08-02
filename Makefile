.PHONY: venv install db-up db-down mlflow-ui api dashboard test

venv:
	python -m venv venv
	@echo "Activate with: source venv/bin/activate (Mac/Linux) or venv\\Scripts\\activate (Windows)"

install:
	pip install -r requirements.txt

db-up:
	docker compose -f infra/docker-compose.yml up -d postgres

db-down:
	docker compose -f infra/docker-compose.yml down

mlflow-ui:
	docker compose -f infra/docker-compose.yml up -d mlflow

api:
	uvicorn src.api.main:app --reload

dashboard:
	streamlit run dashboard/app.py

test:
	pytest tests/
