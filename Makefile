PROJECT_ROOT = $(PWD)
ENV_NAME_MODEL = envs/qazllm_model_env
REQUIREMENTS_FILE_MODEL = requirements.txt
CODE_DIR = src/main.py
TAG = issai_qazllm_benchmark:latest
# Targets
.PHONY: install_nvidia_docker export_env_vars create_env install_requirements \
		build_via_compose run_via_compose down_via_compose

# Target to install NVIDIA Docker
install_nvidia_docker:
	./install_nvidia_docker.sh

# Build the Docker image via compose
build_via_compose:
	docker-compose build

# Run the Docker container with a custom command via compose
run_via_compose:
	@echo "Running $(DIR)"
	@DIR=$(DIR) docker-compose up --build

# Bring down any running containers
down_via_compose:
	docker-compose down

export_env_vars:
	@echo "export PROJECT_ROOT=$(PROJECT_ROOT)" 
	@echo "Environment variable PROJECT_ROOT exported."

create_env:
	@if [ ! -d $(ENV_NAME_MODEL) ]; then \
		python3 -m venv $(ENV_NAME_MODEL); \
		echo "Virtual environment $(ENV_NAME_MODEL) created."; \
	else \
		echo "Virtual environment $(ENV_NAME_MODEL) already exists."; \
	fi

install_requirements: 
	@. $(ENV_NAME_MODEL)/bin/activate && pip install -r $(REQUIREMENTS_FILE_MODEL)
	@echo "Requirements installed."

