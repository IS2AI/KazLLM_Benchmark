import os
from vllm import LLM
import pandas as pd
import logging
from typing import List
from evaluate import load
from pathlib import Path
import yaml  
import torch

from huggingface_hub import login

from utils.utils import *

ROOT_DIR = Path(os.getenv("PROJECT_ROOT", "."))

CONFIG_PATH = ROOT_DIR / "conf" / "parameters_benchmark.yaml"
CREDENTIALS = ROOT_DIR / "conf" / "credentials.yaml"

with open(CONFIG_PATH, "r") as file:
        config = yaml.safe_load(file)

if config['tensor_parallel_size']>1:
    os.environ['VLLM_WORKER_MULTIPROC_METHOD']='spawn'
os.environ["HF_ALLOW_CODE_EVAL"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
# os.environ["NVIDIA_VISIBLE_DEVICES"] = "4,5,6,7"

code_eval = load("code_eval")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main(
    model_path: str,
    model_name: str,
    benchmarks: List[str] = ['arc', 'hellaswag', 'winogrande'],
    languages: List[str] = ['en', 'kk', 'ru'],
    batch_size: int = 32,
    tensor_parallel_size: int = 4,
    data_portion: int = 100,
    max_tokens: Dict[str, int] = None,
    is_local_model: bool = False
):
    try:
        with open(CREDENTIALS, "r") as file:
            token = yaml.safe_load(file)
        output_dir = "data/evaluation"
        os.makedirs(output_dir, exist_ok=True)
        logging.info(f"Loading model: {model_path}")
        if is_local_model:
            model_path = Path(model_path).expanduser().resolve().absolute()
        
        for i in range(torch.cuda.device_count()):
            device = torch.device(f"cuda:{i}")

        torch.randn(10, 10).to(device)
        print(f"GPU {i} is operational: {torch.cuda.get_device_name(i)}")

        login(token['hf_token'])
        llm = LLM(
            model=model_path,
            trust_remote_code=True,
            tensor_parallel_size=tensor_parallel_size,
            gpu_memory_utilization=0.90,
        )
        
        accuracy_metrics = {}
        
        # Map benchmarks to their respective token limits
        if max_tokens is None:
            max_tokens = {
                "max_tokens_mmlu": 15,
                "max_tokens_arc": 30,
                "max_tokens_drop": 40,
                "max_tokens_gsm8k": 512,
                "max_tokens_humaneval": 128,
                "max_tokens_hellaswag": 15,
                "max_tokens_winogrande": 15,
            }

        # Create max_tokens_map using the values from max_tokens
        max_tokens_map = {
            'mmlu': max_tokens['mmlu'],
            'arc': max_tokens['arc'],
            'drop': max_tokens['drop'],
            'gsm8k': max_tokens['gsm8k'],
            'humaneval': max_tokens['humaneval'],
            'hellaswag': max_tokens['hellaswag'],
            'winogrande': max_tokens['winogrande']
        }
        
        for benchmark in benchmarks:
            benchmark_results = []
            max_tokens = max_tokens_map[benchmark]
            
            for lang in languages:
                try:
                    # Special handling for different dataset paths
                    if benchmark == 'gsm8k':
                        dataset_path = f"datasets/gsm8k_{lang}_v2.csv"
                    elif benchmark == 'humaneval':
                        dataset_path = f"datasets/humaneval_{lang}.csv"
                    elif benchmark == "arc":
                        dataset_path = f"datasets/arc_{lang}_v2.csv"
                    else:
                        dataset_path = f"datasets/{benchmark}_{lang}.csv"
                        
                    logging.info(f"Processing {benchmark.upper()} dataset for {lang} with {max_tokens} max tokens")
                    
                    dataset = load_dataset(dataset_path, data_portion)
                    results = evaluate_model(llm, dataset, benchmark, lang, max_tokens, batch_size)
                    benchmark_results.extend(results)
                    
                    # Calculate accuracy based on benchmark type
                    if benchmark == 'humaneval':
                        df = pd.read_csv(dataset_path)
                        if data_portion < 100:
                            df = df.iloc[:len(results)]
                        df_generated = pd.DataFrame(results)
                        accuracy = calculate_pass_at_k(df, df_generated)
                    else:
                        correct = sum(1 for r in results if r['status'] == 'correct')
                        total = len(results)
                        accuracy = correct / total if total > 0 else 0
                    
                    accuracy_metrics[f'{benchmark}_{lang}'] = accuracy
                    
                    logging.info(f"Evaluation complete for {benchmark} {lang}")
                    logging.info(f"Accuracy: {accuracy}")
                    
                except Exception as e:
                    logging.error(f"Error processing {benchmark} for {lang}: {str(e)}")
                    continue
            
            save_results(benchmark_results, benchmark, model_name)
        
        save_accuracy_metrics(accuracy_metrics, model_name, output_dir)
        logging.info("All evaluations complete. Results saved.")
        
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main(**config)
