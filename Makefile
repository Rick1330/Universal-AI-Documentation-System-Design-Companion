.PHONY: test test-unit test-integration test-api test-agents coverage clean

# Default environment, can be overridden (e.g., ENV=dev make test)
ENV ?= test

# Activate virtual environment if it exists and is used
# VENV_ACTIVATE = . ../venv/bin/activate; \

# Pytest command with coverage
PYTEST_CMD = RUNNING_PYTEST=true PYTHONPATH=.. pytest --cov=backend --cov-report=term-missing --cov-report=xml:coverage.xml --cov-report=html:cov_html

# Base directory for tests
TEST_DIR = tests

all: test

test:
	@echo "Running all tests..."
	@cd backend && $(PYTEST_CMD) $(TEST_DIR)

test-unit:
	@echo "Running unit tests..."
	@cd backend && $(PYTEST_CMD) $(TEST_DIR)/unit

test-integration:
	@echo "Running integration tests..."
	@cd backend && $(PYTEST_CMD) $(TEST_DIR)/integration

test-api:
	@echo "Running API tests..."
	@cd backend && $(PYTEST_CMD) $(TEST_DIR)/api

test-agents:
	@echo "Running AI agent tests..."
	@cd backend && $(PYTEST_CMD) $(TEST_DIR)/agents

coverage:
	@echo "Generating coverage report... (Run after tests)"
	@echo "HTML report available at backend/cov_html/index.html"
	@echo "XML report available at backend/coverage.xml"

clean:
	@echo "Cleaning up test artifacts..."
	@rm -rf backend/.pytest_cache
	@rm -rf backend/**/__pycache__
	@rm -rf backend/**/*.pyc
	@rm -rf backend/coverage.xml
	@rm -rf backend/cov_html

# Example: how to set up environment variables if needed for tests
# export PYTHONPATH=.:$(PYTHONPATH)
# export APP_ENV=$(ENV)

