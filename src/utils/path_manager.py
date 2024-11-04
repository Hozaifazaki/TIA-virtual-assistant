import os


class PathManager:
    
    @classmethod
    def initialize_paths(cls, base_dir: str, model_repo: str, target_file: str = None, revision_id: str = None) -> None:
        """Initializes the paths for the project with the given model repository and target file.

        Args:
            base_dir (str): The base directory for the project.
            model_repo (str): The Hugging Face model repository path.
            target_file (str): The file path within the model repository to be downloaded.
            revision_id (str): Optional. The revision/commit ID for the model version.
        """
        models_dir = os.path.join(base_dir, 'models')

        cls.MODEL_REPO = model_repo
        cls.TARGET_FILE_NAME = target_file
        cls.REVISION_ID = revision_id
        cls.MODEL_NAME = model_repo.split("/")[-1].replace("-", "_").lower()
        
        target_file_dir = os.path.basename(target_file) if target_file else cls.MODEL_NAME

        # Paths where the model will be saved in the local project
        cls.MODEL_DIR_PATH = os.path.join(models_dir, cls.MODEL_NAME, target_file_dir)
        
        # Cache path in the user's system for Hugging Face models
        cls.MODEL_CACHE_DIR = os.path.join(os.path.expanduser('~'), ".cache", "huggingface", "hub", f"models--{model_repo.replace('/', '--')}")

