# LLM Benchmarking Framework

## Overview
This framework provides a standardized approach to evaluating Large Language Models (LLMs) using established benchmarks. It implements a systematic process for testing model performance across various cognitive and technical tasks.

## General Approach

The benchmarking process follows these key steps:

1. Input Data: Collection of benchmark-specific datasets
2. Prompt Generation: Creation of tailored task-specific prompts
3. Model Execution: Processing prompts through the LLM
4. Evaluation: Comparison with ground truth using appropriate metrics
5. Result Aggregation: Computing and storing performance metrics

## Benchmarks

### [MMLU (Massive Multitask Language Understanding)](https://arxiv.org/abs/2009.03300)
- **Description**: Tests knowledge across 57 domains including STEM, humanities, and social sciences
- **Input**: Multiple-choice questions (A, B, C, D)
- **Output**: Single letter selection
- **Metric**: Accuracy
- **Shot Setting**: Zero-shot

### [ARC (AI2 Reasoning Challenge)](https://arxiv.org/abs/1803.05457)
- **Description**: Evaluates logical reasoning and domain knowledge
- **Input**: Question with four options (A, B, C, D)
- **Output**: Single letter selection
- **Metric**: Accuracy
- **Shot Setting**: Zero-shot

### [HellaSwag](https://arxiv.org/abs/1905.07830)
- **Description**: Tests sentence completion plausibility
- **Input**: Context with four possible endings
- **Output**: Number selection (1-4)
- **Metric**: Accuracy
- **Shot Setting**: Zero-shot

### [Winogrande](https://arxiv.org/abs/1907.10641)
- **Description**: Assesses commonsense reasoning through sentence completion
- **Input**: Sentence with blank and two options
- **Output**: Number selection (1 or 2)
- **Metric**: Accuracy
- **Shot Setting**: Zero-shot

### [GSM8K (Grade School Math 8K)](https://arxiv.org/abs/2110.14168)
- **Description**: Evaluates multi-step mathematical problem-solving
- **Input**: Math problem with three solved examples
- **Output**: Numerical answer
- **Metric**: Numerical accuracy
- **Shot Setting**: Three-shot chain-of-thought

### [DROP (Discrete Reasoning Over Paragraphs)](https://arxiv.org/abs/1903.00161)
- **Description**: Tests reading comprehension and numerical reasoning
- **Input**: Passage and question
- **Output**: Text or numerical answer
- **Metric**: Exact match accuracy
- **Shot Setting**: Zero-shot

### [HumanEval](https://arxiv.org/abs/2107.03374)
- **Description**: Assesses Python code generation capabilities
- **Input**: Function definition prompt
- **Output**: Complete Python function
- **Metric**: Pass@1
- **Shot Setting**: Zero-shot

## Shot Settings

The framework employs two primary shot settings:

- **Zero-Shot**: Used for most benchmarks
  - No examples provided
  - Clear task description and instructions only

- **Three-Shot Chain-of-Thought**: Used for GSM8K
  - Includes three worked examples
  - Guides step-by-step problem solving

## Evaluation Metrics

The framework uses various metrics depending on the benchmark:

- **Accuracy**: Used for:
  - MMLU
  - ARC
  - HellaSwag
  - Winogrande

- **Exact Match**: Used for:
  - DROP (with normalization for formatting)

- **Numerical Accuracy**: Used for:
  - GSM8K

- **Pass@1**: Used for:
  - HumanEval

## Usage

### Prerequisites

1. **Check if Docker is installed**:
   ```bash
   docker --version
   ```
   If Docker is not installed, refer to the [official Docker installation guide](https://docs.docker.com/get-docker/).

2. **Check if Docker Compose is installed**:
   ```bash
   docker-compose --version
   ```
   If Docker Compose is not installed, refer to the [official Docker Compose installation guide](https://docs.docker.com/compose/install/).

3. **Check if CUDA and GPUs are available**:
   ```bash
   nvidia-smi
   ```
   If CUDA is not configured or GPUs are not detected, refer to the [CUDA Toolkit Installation Guide](https://developer.nvidia.com/cuda-toolkit).

4. **Check if NVIDIA Docker is installed**:
   ```bash
   nvidia-docker --version
   ```
   If NVIDIA Docker is not installed, run the following command in the project root directory (where the `Makefile` is located):
   ```bash
   make install_nvidia_docker
   ```
   For further information, refer to the [NVIDIA Docker installation guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).

5. **Configure GPU access**:
   In the `docker-compose.yaml` file, set the `NVIDIA_VISIBLE_DEVICES` environment variable to specify the GPUs you want to use.

---

### Setting Configurations

Edit the `conf/parameters_benchmark.yaml` file to set your desired configurations for benchmarking.

---

### Download Datasets

To download the required datasets for benchmarking, run:
```bash
make run_via_compose DIR=src/utils/download_dataset.py
```

---

### Build Docker Images (if required)

If Docker images need to be built, run:
```bash
make build_via_compose
```

---

### Run Benchmark

To start the benchmarking process, run:
```bash
make run_via_compose
```
