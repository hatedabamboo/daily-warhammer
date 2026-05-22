.PHONY: build clean lint lint-python lint-terraform fmt install

SRC_DIR  := src
DIST_DIR := dist
TF_DIR   := terraform

build: clean
	mkdir -p $(DIST_DIR)/package
	uv export --no-dev --no-hashes -o $(DIST_DIR)/requirements.txt
	uv pip install -r $(DIST_DIR)/requirements.txt --target $(DIST_DIR)/package --quiet
	cp -r $(SRC_DIR) $(DIST_DIR)/package/
	@echo "Build complete: $(DIST_DIR)/package/"

clean:
	rm -rf $(DIST_DIR)

lint: lint-python lint-terraform

lint-python:
	uv run ruff check $(SRC_DIR)
	uv run ruff format --check $(SRC_DIR)
	uv run mypy $(SRC_DIR)

lint-terraform:
	terraform -chdir=$(TF_DIR) fmt -check -recursive
	terraform -chdir=$(TF_DIR) init -backend=false -reconfigure
	terraform -chdir=$(TF_DIR) validate

fmt:
	uv run ruff format $(SRC_DIR)
	terraform -chdir=$(TF_DIR) fmt -recursive

install:
	uv sync
