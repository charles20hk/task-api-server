# combined build target
build: types-check lint-check ruff-format-check \
	run-tests

run-tests:
	@echo "Running integration tests"
	poetry run pytest tests/integration
	@echo

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

run-server:
	@echo "Running the API server"
	poetry run python -m app.web.main
	@echo
