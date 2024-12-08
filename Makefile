PROJECT_ROOT = $(shell pwd)
ENV_NAME_MODEL = envs/qazllm_model_env
REQUIREMENTS_FILE_MODEL = requirements.txt
MODEL_IMAGE_TAG=issai_qazllm:latest


# Targets
.PHONY: export_env_vars create_model_env install_model_requirements \
		model_docker_build model_docker_run model_docker_run_default model_docker_tag model_docker_down \
		install_nvidia_docker

# Target to install NVIDIA Docker
install_nvidia_docker:
	./install_nvidia_docker.sh

# Build the Docker image
model_docker_build:
	docker-compose build

# Run the Docker container with a custom command
model_docker_run:
	@echo "Running $(DIR)"
	@DIR=$(DIR) docker-compose up --build

# Bring down any running containers
model_docker_down:
	docker-compose down

export_env_vars:
	@echo "export PROJECT_ROOT=$(PROJECT_ROOT)" 
	@echo "Environment variable PROJECT_ROOT exported."

create_model_env:
	@if [ ! -d $(ENV_NAME_MODEL) ]; then \
		python3 -m venv $(ENV_NAME_MODEL); \
		echo "Virtual environment $(ENV_NAME_MODEL) created."; \
	else \
		echo "Virtual environment $(ENV_NAME_MODEL) already exists."; \
	fi

install_model_requirements: 
	@. $(ENV_NAME_MODEL)/bin/activate && pip install -r $(REQUIREMENTS_FILE_MODEL)
	@echo "Requirements installed."

