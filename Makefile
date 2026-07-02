MCP_DIR := tools/kapitan-mcp
UV := uv --directory $(MCP_DIR)

.PHONY: help sync lint format typecheck test test-integration evals all \
        sync-plugins check-plugins validate-skills

help:
	@echo "Targets: sync lint format typecheck test test-integration evals all"
	@echo "         sync-plugins check-plugins validate-skills"

sync:
	$(UV) sync

lint:
	$(UV) run ruff check .
	$(UV) run ruff format --check .

format:
	$(UV) run ruff format .
	$(UV) run ruff check --fix .

typecheck:
	$(UV) run mypy

test:
	$(UV) run pytest -m "not integration and not e2e"

test-integration:
	$(UV) run pytest -m integration

validate-skills:
	python3 scripts/validate_skills.py

sync-plugins:
	python3 scripts/sync_plugins.py

check-plugins:
	python3 scripts/sync_plugins.py --check

evals:
	@echo "trigger-rate evals run via the skill-creator harness with an API key"

all: lint typecheck test validate-skills check-plugins
