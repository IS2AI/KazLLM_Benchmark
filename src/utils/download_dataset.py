import os
from pathlib import Path
import yaml

from datasets import load_dataset
from huggingface_hub import HfApi, login

ROOT_DIR = Path(os.getenv("PROJECT_ROOT", "."))  # Root directory for the project
CONFIG_PATH = ROOT_DIR / "conf" / "parameters_benchmark.yaml"
CREDENTIALS_PATH = ROOT_DIR / "conf" / "credentials.yaml"
DATA_SAVE_DIR = ROOT_DIR / "data"/"datasets"

# Functions
def load_yaml(file_path: Path) -> dict:
   
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

def filter_files(api: HfApi, repo_id: str) -> list:
    """
    Filter files from a Hugging Face repository based on keywords and prefixes.

    Args:
        api (HfApi): Hugging Face API instance.
        repo_id (str): ID of the repository.
        keyword (str): Keyword to match in file names.
        file_prefix (str): Prefix to match in file names.

    Returns:
        list: Filtered list of file names.
    """
    all_files = api.list_repo_files(repo_id=repo_id, repo_type="dataset")
    print(all_files)
    for i,v in enumerate(all_files):
        if 'csv' not in v:
            all_files.pop(i) 
    return sorted([f for f in all_files])

def process_and_save_dataset(config: dict, file_name: str, save_dir: Path):
    """
    Process a dataset file and save the filtered content to a CSV.

    Args:
        config (dict): Configuration containing dataset repository details.
        file_name (str): Name of the dataset file.
        save_dir (Path): Directory to save the processed CSV.
    """
    # Load the dataset
    dataset = load_dataset(config["data_repo"], data_files=file_name, split="train")
    
    save_path = save_dir / f"{file_name}"
    save_path.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(save_path)

# Main Execution
if __name__ == "__main__":
    # Load credentials and configuration
    credentials = load_yaml(CREDENTIALS_PATH)
    config = load_yaml(CONFIG_PATH)
    
    # Login to Hugging Face
    login(credentials["hf_token"])
    
    # Initialize Hugging Face API
    api = HfApi()
    
    # Get filtered files from the repository
    repo_id = config["data_repo"]
    files_to_process = filter_files(api, repo_id)
    
    # Process and save each dataset
    for file_name in files_to_process:
        process_and_save_dataset(config, file_name, DATA_SAVE_DIR)
