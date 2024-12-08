from typing import List, Dict
from torch.utils.data import Dataset
from prompts import *

class EvaluationDataset(Dataset):
    def __init__(self, dataset: List[Dict], benchmark: str, lang: str):
        self.dataset = dataset
        self.benchmark = benchmark
        self.lang = lang

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        item = self.dataset[idx]
        if self.benchmark == 'humaneval':
            prompt = create_humaneval_prompt_old(item)
            return {
                'prompt': prompt,
                'task_id': item['task_id'],
                'original_prompt': item['prompt'],
                'lang': self.lang
            }
        elif self.benchmark == 'gsm8k':
            prompt = create_math_prompt(item, self.lang)
            return {
                'prompt': prompt,
                'question': item['question'],
                'hints': item.get('hints', ''),
                'answer': item['answer']
            }
        elif self.benchmark == 'drop':
            prompt = create_drop_prompt(item, self.lang)
            return {
                'prompt': prompt,
                'query_id': item['query_id'],
                'passage': item['passage'],
                'question': item['question'],
                'answers': item['answers']
            }
        elif self.benchmark == 'winogrande':
            prompt = create_winogrande_prompt(item, self.lang)
            return {
                'prompt': prompt,
                'sentence': item['sentence'],
                'option1': item['option1'],
                'option2': item['option2'],
                'answer': str(item['answer'])
            }
        elif self.benchmark == 'hellaswag':
            prompt = create_hellaswag_prompt(item, self.lang)
            return {
                'prompt': prompt,
                'ctx': item['ctx'],
                'option1': item['option1'],
                'option2': item['option2'],
                'option3': item['option3'],
                'option4': item['option4'],
                'answer': str(item['answer'])
            }
        else:
            prompt = create_mcq_prompt(item, self.benchmark, self.lang)
            return {
                'prompt': prompt,
                'question': item['question'],
                'A': item['A'],
                'B': item['B'],
                'C': item['C'],
                'D': item['D'],
                'answer': str(item['answer']).strip().upper()
            }