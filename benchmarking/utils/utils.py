import re
import random
import pandas as pd
import json
import numpy as np
import ast
import os

from typing import List, Dict
from tqdm import tqdm
from torch.utils.data import DataLoader
from vllm import LLM, SamplingParams
from pathlib import Path
from evaluate import load

from utils.evaluations_dataset import EvaluationDataset

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

CODE_EVAL = load("code_eval")

def extract_code_from_markdown(text: str) -> str:
    """Extract code from between ``` markers and clean it up."""
    pattern = r"```(?:python\n|\n)?(.+?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    
    if matches:
        code = matches[0].strip()
    else:
        code = text.strip()
    
    func_pattern = r"(def\s+.*?(?:\n|$).*)"
    func_matches = re.findall(func_pattern, code, re.DOTALL)
    
    if func_matches:
        func_code = func_matches[0].strip()
        while func_code and func_code[-1] in ['"', "'", ',', '.', '\n']:
            func_code = func_code[:-1]
        return func_code
    
    return code.strip()

def extract_mcq_answer(text: str) -> str:
    text = str(text).strip().upper()
    
    answer_patterns = [
        r'(?i)answer[\s:\n\.,]+([ABCD])',
        r'(?i)ответ[\s:\n\.,]+([ABCD])',
        r'(?i)жауап[\s:\n\.,]+([ABCD])'
    ]
    
    for pattern in answer_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    matches = re.findall(r'\b[ABCD]\b', text)
    return matches[0] if matches else None

def extract_drop_answer(result: str) -> str:
    return str(result).strip()

def extract_math_answer(text: str, lang: str = 'en') -> str:
    text = str(text).strip()
    
    markers = {
        'en': 'Exact Answer:',
        'kk': 'Нақты жауап:',
        'ru': 'Точный ответ:'
    }
    
    marker = markers.get(lang, markers['en'])
    
    try:
        # First try to extract by language-specific marker
        if marker in text:
            after_marker = text.split(marker, 1)[1].strip()
            numbers = re.findall(r'[-+]?\d*\.?\d+', after_marker)
            if numbers:
                return numbers[0]
        
        # Then try to extract by #### delimiter
        if '####' in text:
            after_delimiter = text.split('####', 1)[1].strip()
            # Remove any currency symbols and whitespace
            cleaned_text = re.sub(r'[^\d.-]', '', after_delimiter)
            if cleaned_text:
                return cleaned_text
        
        # If no delimiters found, try to find any numbers
        numbers = re.findall(r'[-+]?\d*\.?\d+', text)
        if numbers:
            return numbers[0]
        
        return text
        
    except Exception as e:
        logging.error(f"Error extracting math answer: {e}")
        return text

def evaluate_drop_answer(result: str, answers: List, lang: str = 'en') -> int:
    result_str = str(result).strip()
    
    def normalize_text(text, lang):
        text = text.strip()
        if lang in ['kk', 'ru']:
            text = re.sub(r'(\d+)\.(\d+)', r'\1,\2', text)
        return text
    
    def create_pattern(answer):
        answer_escaped = re.escape(str(answer).strip())
        return fr'\n?\b{answer_escaped}\b[.,\s%\n]*'

    def are_words_similar(word1, word2):
        w1 = re.sub(r'[.,\s%\n]+$', '', word1.lower())
        w2 = re.sub(r'[.,\s%\n]+$', '', word2.lower())
        
        if w1 in w2 or w2 in w1:
            return True
        
        if len(w1) > 2 and len(w2) > 2:
            if w1[:-1] == w2[:-1]:
                return True
        
        return False
    
    count = 0
    normalized_result = normalize_text(result_str, lang)
    
    for answer in answers:
        answer_str = str(answer).strip()
        normalized_answer = normalize_text(answer_str, lang)
        
        if normalized_result == normalized_answer:
            count += 1
            continue
        
        pattern = create_pattern(normalized_answer)
        if re.search(pattern, normalized_result, re.MULTILINE):
            count += 1
            continue
            
        if lang in ['kk', 'ru'] and '.' in answer_str:
            alt_answer = answer_str.replace('.', ',')
            pattern = create_pattern(alt_answer)
            if re.search(pattern, normalized_result, re.MULTILINE):
                count += 1
                continue

        if are_words_similar(normalized_result, normalized_answer):
            count += 1
            continue
    
    return min(count, 1)

def evaluate_math_answer(result: str, answers: List, lang: str = 'en') -> int:
    """Evaluate math answers with special handling for numerical comparisons."""
    result_str = str(result).strip()
    
    def normalize_text(text, lang):
        text = text.strip()
        if lang in ['en', 'kk', 'ru']:
            text = re.sub(r'(\d+)\.(\d+)', r'\1,\2', text)
        return text
    
    def are_numbers_equal(num1, num2):
        try:
            n1 = float(str(num1).replace(',', '').replace(' ', '').replace('،', '').rstrip('.,'))
            n2 = float(str(num2).replace(',', '').replace(' ', '').replace('،', '').rstrip('.,'))
            return abs(n1 - n2) < 1e-10
        except ValueError:
            return False
    
    normalized_result = normalize_text(result_str, lang)
    
    for answer in answers:
        if are_numbers_equal(normalized_result, answer):
            return 1
            
    return 0


def load_dataset(file_path: str, data_portion: int = 100) -> List[Dict]:
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        
        data = df.to_dict('records')
        
        if data_portion < 100:
            num_samples = int(len(data) * (data_portion / 100))
            return random.sample(data, num_samples)
        return data
        
    except Exception as e:
        logging.error(f"Error loading dataset {file_path}: {str(e)}")
        raise

def evaluate_model(llm: LLM, dataset: List[Dict], benchmark: str, lang: str, max_tokens: int, batch_size: int = 32) -> List[Dict]:
    eval_dataset = EvaluationDataset(dataset, benchmark, lang)
    dataloader = DataLoader(eval_dataset, batch_size=batch_size, shuffle=False)

    results = []
    sampling_params = SamplingParams(
        temperature=0.01,
        max_tokens=max_tokens,
        stop=['=================================================='] if benchmark != 'gsm8k' else None
    )
    
    for batch in tqdm(dataloader, desc=f"Evaluating {benchmark.upper()} {lang}"):
        prompts = batch['prompt']
        outputs = llm.generate(prompts, sampling_params)
        generated = [output.outputs[0].text.strip() for output in outputs]
        
        if benchmark == 'humaneval':
            for i, gen in enumerate(generated):
                clean_code = extract_code_from_markdown(gen)
                results.append({
                    'task_id': batch['task_id'][i],
                    'original_prompt': batch['original_prompt'][i],
                    'generated': clean_code,
                    'language': lang,
                    'status': 'pending'  # Will be updated after pass@k calculation
                })
        elif benchmark == 'gsm8k':
            for i, gen in enumerate(generated):
                answer = batch['answer'][i]
                extracted_answer = extract_math_answer(gen, lang)
                
                try:
                    answers = [float(answer)]
                except (ValueError, TypeError):
                    answers = [answer]
                
                is_correct = evaluate_math_answer(extracted_answer, answers, lang) > 0
                
                results.append({
                    'question': batch['question'][i],
                    'hints': batch['hints'][i],
                    'answer': batch['answer'][i],
                    'generated': gen,
                    'extracted_answer': extracted_answer,
                    'language': lang,
                    'status': 'correct' if is_correct else 'incorrect'
                })
        elif benchmark == 'drop':
            for i, gen in enumerate(generated):
                answers = ast.literal_eval(batch['answers'][i])
                is_correct = evaluate_drop_answer(gen, answers, lang) > 0
                
                results.append({
                    'query_id': batch['query_id'][i],
                    'passage': batch['passage'][i],
                    'question': batch['question'][i],
                    'answers': batch['answers'][i],
                    'generated': gen,
                    'language': lang,
                    'status': 'correct' if is_correct else 'incorrect'
                })
        elif benchmark == 'winogrande':
            for i, gen in enumerate(generated):
                # Extract just the number from the generated text
                extracted_answer = ''.join(filter(str.isdigit, gen))[:1]  # Take first digit
                is_correct = extracted_answer == batch['answer'][i]
                
                results.append({
                    'sentence': batch['sentence'][i],
                    'option1': batch['option1'][i],
                    'option2': batch['option2'][i],
                    'correct_answer': batch['answer'][i],
                    'generated': gen,
                    'extracted_answer': extracted_answer,
                    'language': lang,
                    'status': 'correct' if is_correct else 'incorrect'
                })
        elif benchmark == 'hellaswag':
            for i, gen in enumerate(generated):
                # Extract just the number from the generated text
                extracted_answer = ''.join(filter(str.isdigit, gen))[:1]  # Take first digit
                is_correct = extracted_answer == batch['answer'][i]
                
                results.append({
                    'ctx': batch['ctx'][i],
                    'option1': batch['option1'][i],
                    'option2': batch['option2'][i],
                    'option3': batch['option3'][i],
                    'option4': batch['option4'][i],
                    'correct_answer': batch['answer'][i],
                    'generated': gen,
                    'extracted_answer': extracted_answer,
                    'language': lang,
                    'status': 'correct' if is_correct else 'incorrect'
                })        
        else:
            for i, gen in enumerate(generated):
                extracted_answer = extract_mcq_answer(gen)
                is_correct = extracted_answer == batch['answer'][i] if extracted_answer else False
                
                results.append({
                    'question': batch['question'][i],
                    'A': batch['A'][i],
                    'B': batch['B'][i],
                    'C': batch['C'][i],
                    'D': batch['D'][i],
                    'correct_answer': batch['answer'][i],
                    'generated': gen,
                    'extracted_answer': extracted_answer,
                    'language': lang,
                    'status': 'correct' if is_correct else 'incorrect'
                })

    return results

def calculate_pass_at_k(df: pd.DataFrame, df_generated: pd.DataFrame) -> float:
    pass_k = np.zeros(df.shape[0])

    for idx, row in tqdm(df.iterrows(), total=len(df)):
        tests = ast.literal_eval(row['tests'])
        test_pass = []
        for test in tests:
            test_cases = [test]
            candidates = [[df_generated['generated'].iloc[idx]]]
            pass_at_k, _ = CODE_EVAL.compute(references=test_cases, predictions=candidates, k=[1])
            test_pass.append(pass_at_k['pass@1'])
        pass_k[idx] = sum(test_pass) / len(test_pass)

    return np.mean(pass_k)

def save_results(results: List[Dict], benchmark: str, model_name: str):
    try:
        output_path = Path("data/evaluation") 
        output_path.parent.resolve().mkdir(parents=True, exist_ok=True)
        output_file = os.path.join(output_path, f"{benchmark}_generated_{model_name}.csv")
        
        df = pd.DataFrame(results)
        
        # Define columns for each benchmark type
        if benchmark == 'drop':
            columns = ['query_id', 'passage', 'question', 'answers', 'generated', 'status', 'language']
        elif benchmark == 'gsm8k':
            columns = ['question', 'hints', 'answer', 'generated', 'extracted_answer', 'status', 'language']
        elif benchmark == 'humaneval':
            columns = ['task_id', 'original_prompt', 'generated', 'status', 'language']
        elif benchmark == 'winogrande':
            columns = ['sentence', 'option1', 'option2', 'correct_answer', 'generated', 'extracted_answer', 'status', 'language']
        elif benchmark == 'hellaswag':
            columns = ['ctx', 'option1', 'option2', 'option3', 'option4', 'correct_answer', 'generated', 'extracted_answer', 'status', 'language']
        else:  # for MMLU and ARC
            columns = ['question', 'A', 'B', 'C', 'D', 'correct_answer', 'generated', 'extracted_answer', 'status', 'language']
        
        # Select only columns that exist in the DataFrame
        columns = [col for col in columns if col in df.columns]
        
        df = df[columns]
        df.to_csv(output_file, index=False, encoding='utf-8')
        logging.info(f"Results saved to {output_file}")
        
    except Exception as e:
        logging.error(f"Error saving results: {str(e)}")
        raise

def save_accuracy_metrics(accuracy_results: Dict, model_name: str, output_dir: str = "data/evaluation"):
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"accuracy_metrics_{model_name}.json")
        
        # Restructure the results according to the new format
        formatted_results = {
            "model_name": model_name,
            "results": {
                "en": {},
                "kk": {},
                "ru": {}
            }
        }
        
        # Populate the results
        for key, value in accuracy_results.items():
            benchmark, lang = key.split('_')
            formatted_results["results"][lang][benchmark] = {"acc": value}
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(formatted_results, f, indent=2)
        logging.info(f"Accuracy metrics saved to {output_file}")
        
    except Exception as e:
        logging.error(f"Error saving accuracy metrics: {str(e)}")
        raise