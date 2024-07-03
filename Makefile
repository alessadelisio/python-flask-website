.PHONY: help
help:     ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep


.PHONY: venv
venv:     ## Create a virtual environment.
	@echo "=============================="
	@echo "Creating virtual environment..."
	@echo "=============================="
	@rm -rf .venv
	@python3 -m venv .venv
	@./.venv/bin/pip install -U pip
	@echo
	@echo "Run 'source .venv/bin/activate' to enable the environment"


.PHONY: fmt
fmt:      ## Format python code.
	@echo "=============================="
	@echo "Formatting code..."
	@echo "=============================="
	@ruff check --fix --select I
	@ruff format .


.PHONY: install
install:  ## Install dependencies.
	@echo "=============================="
	@echo "Installing dependencies..."
	@echo "=============================="
	pip install -r requirements-test.txt
	pip install -r requirements-dev.txt
	pip install -r requirements.txt


.PHONY: clean
clean:    ## Clean unused files.
	@rm -rf build
	@rm -rf reports/ || true
	@rm -f .coverage || true
	@find . -type d -name '*_cache' -exec rm -rf {} +


.PHONY: lint
lint:     ## Check code smells with Ruff
	@echo "=============================="
	@echo "Searching for code smells..."
	@echo "=============================="
	@echo
	@mkdir -p reports/lint-reports || true
	@ruff check --exit-zero --output-format json -o reports/lint-reports/ruff.json .
	@ruff check --exit-zero --output-format text .


.PHONY: test
test:     ## Run tests and coverage.
	@echo "=============================="
	@echo "Running tests..."
	@echo "=============================="
	@mkdir -p reports || true
	@python -m pytest


.PHONY: Run
run:      ## Run hypercorn
	APP_ENVIRONMENT=local hypercorn --workers=1 --bind=0.0.0.0:8080 --log-level DEBUG --reload src.app:asgi_app
