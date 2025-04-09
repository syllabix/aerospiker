.PHONY: help benchmark deps devenv.start devenv.stop testdata gopsike.run

# Default target
.DEFAULT_GOAL := help

# Colors for help output
BLUE := \033[34m
GREEN := \033[32m
RESET := \033[0m

help: ## Display this help message
	@echo "$(BLUE)Available targets:$(RESET)"
	@grep -E '^[a-zA-Z0-9_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'

deps: ## Install dependencies (installs rust, go, uv (for python), and oha (for benchmarking))
	curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
	curl -LsSf https://astral.sh/uv/install.sh | sh
	brew install go
	cargo install oha

devenv.start: ## Setup development environment
	docker compose up

devenv.stop: ## Stop development environment
	docker compose down

testdata: ## Load test data into aerospike and generate urls
	cd loader && uv venv && . .venv/bin/activate && uv pip install -r requirements.txt && python load_data.py && python generate_urls.py

urls: ## Generate urls
	cd loader && uv venv && . .venv/bin/activate && python generate_urls.py
	mv loader/urls.txt benchmark/urls.txt

gopsike.run: ## Run the gopsike server
	cd gopsike && go run main.go

rspike.run: ## Run the rspike server
	cd rspike && cargo run

benchmark: ## Run the benchmark
	cd benchmark && oha -c 1 -z 5m --urls-from-file urls.txt

