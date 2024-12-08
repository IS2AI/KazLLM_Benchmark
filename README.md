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

