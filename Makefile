# combined build target
build: types-check lint-check ruff-format-check \
	coverage-erase run-unit-tests run-integration-tests coverage-check

types-check:
	@echo "Running type check"
	poetry run mypy . --show-error-codes
	@echo

lint-check:
	@echo "Running lint check"
	poetry run ruff check
	@echo

ruff-format-check:
	@echo "Running ruff (Black) style check"
	poetry run ruff format --check
	@echo

coverage-erase:
	@echo "Running coverage erase"
	poetry run coverage erase
	@echo

run-unit-tests:
	@echo "Running unit tests"
	poetry run coverage run -m pytest tests/unit
	@echo

run-integration-tests:
	@echo "Running integration tests"
	poetry run coverage run -m pytest tests/integration
	@echo

coverage-check:
	@echo "Running coverage check"
	poetry run coverage report --fail-under 100
	@echo

run-server:
	@echo "Running the API server"
	poetry run python -m app.web.main
	@echo
