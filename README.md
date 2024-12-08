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


# Function Documentation

## Core Functions

### `get_math_examples(lang: str) -> str`
Returns example math problems and solutions in the specified language.
- **Parameters**: 
  - `lang`: Language code ('en', 'kk', or 'ru')
- **Returns**: String containing math examples in the specified language
- **Purpose**: Provides consistent example problems for GSM8K math prompts

### `extract_code_from_markdown(text: str) -> str`
Extracts and cleans code from markdown-formatted text.
- **Parameters**:
  - `text`: Markdown text containing code
- **Returns**: Cleaned code string
- **Features**:
  - Removes markdown code block markers
  - Extracts function definitions
  - Cleans trailing punctuation
  - Handles both explicit code blocks and raw code

### `create_mcq_prompt(row: Dict, benchmark: str, lang: str) -> str`
Generates prompts for multiple-choice questions (MCQ).
- **Parameters**:
  - `row`: Dictionary containing question data
  - `benchmark`: Benchmark identifier
  - `lang`: Language code
- **Returns**: Formatted MCQ prompt
- **Supported Languages**: English, Kazakh, Russian

### `create_winogrande_prompt(row: Dict, lang: str) -> str`
Creates prompts for Winogrande commonsense reasoning tasks.
- **Parameters**:
  - `row`: Dictionary with sentence and options
  - `lang`: Language code
- **Returns**: Formatted Winogrande prompt
- **Features**: 
  - Handles sentence completion tasks
  - Provides two options for blank filling

### `create_hellaswag_prompt(row: Dict, lang: str) -> str`
Generates prompts for HellaSwag sentence completion tasks.
- **Parameters**:
  - `row`: Dictionary with context and options
  - `lang`: Language code
- **Returns**: Formatted HellaSwag prompt
- **Features**:
  - Handles four-option sentence endings
  - Maintains context consistency

### `create_drop_prompt(row: Dict, lang: str) -> str`
Creates prompts for DROP reading comprehension tasks.
- **Parameters**:
  - `row`: Dictionary with passage and question
  - `lang`: Language code
- **Returns**: Formatted DROP prompt
- **Features**:
  - Includes passage and question context
  - Maintains language consistency

### `create_math_prompt(row: Dict, lang: str) -> str`
Generates prompts for GSM8K math problems.
- **Parameters**:
  - `row`: Dictionary with question and hints
  - `lang`: Language code
- **Returns**: Formatted math prompt
- **Features**:
  - Includes step-by-step solution hints
  - Provides example problems

## Answer Extraction and Evaluation

### `extract_mcq_answer(text: str) -> str`
Extracts multiple-choice answers from model outputs.
- **Parameters**:
  - `text`: Model's response text
- **Returns**: Single letter answer (A, B, C, or D)
- **Features**:
  - Pattern matching for different answer formats
  - Case-insensitive matching
  - Multi-language support

### `extract_drop_answer(result: str) -> str`
Extracts answers from DROP task responses.
- **Parameters**:
  - `result`: Model's response text
- **Returns**: Cleaned answer string
- **Features**: Basic text cleaning and normalization

### `extract_math_answer(text: str, lang: str = 'en') -> str`
Extracts numerical answers from math problem responses.
- **Parameters**:
  - `text`: Model's response text
  - `lang`: Language code
- **Returns**: Extracted numerical answer
- **Features**:
  - Handles multiple answer formats
  - Language-specific markers
  - Numerical pattern matching

### `evaluate_drop_answer(result: str, answers: List, lang: str = 'en') -> int`
Evaluates DROP task answers.
- **Parameters**:
  - `result`: Model's answer
  - `answers`: List of correct answers
  - `lang`: Language code
- **Returns**: Binary score (0 or 1)
- **Features**:
  - Text normalization
  - Pattern matching
  - Handles multiple correct answers
  - Language-specific formatting

### `evaluate_math_answer(result: str, answers: List, lang: str = 'en') -> int`
Evaluates mathematical answers.
- **Parameters**:
  - `result`: Model's answer
  - `answers`: List of correct answers
  - `lang`: Language code
- **Returns**: Binary score (0 or 1)
- **Features**:
  - Numerical comparison
  - Handles different number formats
  - Language-specific number formatting

## Dataset and Model Evaluation

### `EvaluationDataset(Dataset)`
Custom dataset class for benchmark evaluation.
- **Methods**:
  - `__init__`: Initializes dataset
  - `__len__`: Returns dataset size
  - `__getitem__`: Returns formatted items
- **Features**:
  - Supports multiple benchmarks
  - Handles different prompt formats
  - Multi-language support

### `load_dataset(file_path: str, data_portion: int = 100) -> List[Dict]`
Loads and processes benchmark datasets.
- **Parameters**:
  - `file_path`: Path to dataset file
  - `data_portion`: Percentage of data to use
- **Returns**: List of data samples
- **Features**:
  - CSV file handling
  - Random sampling
  - Error handling

### `evaluate_model(llm: LLM, dataset: List[Dict], benchmark: str, lang: str, max_tokens: int, batch_size: int = 32) -> List[Dict]`
Core model evaluation function.
- **Parameters**:
  - `llm`: Language model instance
  - `dataset`: Evaluation dataset
  - `benchmark`: Benchmark type
  - `lang`: Language code
  - `max_tokens`: Maximum generation length
  - `batch_size`: Batch size for evaluation
- **Returns**: List of evaluation results
- **Features**:
  - Batch processing
  - Multiple benchmark support
  - Result extraction and evaluation
  - Progress tracking

## Results Management

### `save_results(results: List[Dict], benchmark: str, model_name: str, output_dir: str = "results")`
Saves evaluation results to CSV files.
- **Parameters**:
  - `results`: Evaluation results
  - `benchmark`: Benchmark type
  - `model_name`: Model identifier
  - `output_dir`: Output directory
- **Features**:
  - Benchmark-specific formatting
  - CSV file generation
  - Error handling

### `save_accuracy_metrics(accuracy_results: Dict, model_name: str, output_dir: str = "results")`
Saves accuracy metrics in JSON format.
- **Parameters**:
  - `accuracy_results`: Dictionary of accuracy scores
  - `model_name`: Model identifier
  - `output_dir`: Output directory
- **Features**:
  - Structured JSON output
  - Multi-language results organization
  - Error handling

## Main Execution

### `main()`
Main execution function with comprehensive configuration options.
- **Features**:
  - Model loading and configuration
  - Multi-benchmark evaluation
  - Multi-language support
  - Progress logging
  - Result aggregation and saving
- **Parameters**: Extensive configuration options for:
  - Model settings
  - Benchmark selection
  - Language selection
  - Token limits
  - Output configuration
