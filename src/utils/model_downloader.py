import os
import time
import shutil

from huggingface_hub import snapshot_download #, utils

from utils.path_manager import PathManager


class ModelDownloader:
    def __init__(self) -> None:
        # Initialize model paths
        self.initialize_model_paths()

        # Disable progress bars in Hugging Face utilities
        # utils.disable_progress_bars()

        # Start the model download process
        self.start_download()

    def initialize_model_paths(self) -> None:
        """Initializes the paths for model repository, directory, name, and cache.
        """
        self.model_repository: str = PathManager.MODEL_REPO
        self.model_dir_path: str = PathManager.MODEL_DIR_PATH
        self.target_file_name: str = PathManager.TARGET_FILE_NAME
        self.model_name: str = os.path.basename(PathManager.TARGET_FILE_NAME)
        self.model_cache_dir: str = PathManager.MODEL_CACHE_DIR
        self.revision_id: str = PathManager.REVISION_ID
        self.model_snapshot_dir: str = os.path.join(self.model_cache_dir, "snapshots")

    def start_download(self) -> None:
        """Starts the model download process if the model path does not exist.
        """
        if not os.path.exists(self.model_dir_path):
            self.download_model_with_retries()

    def remove_old_revisions(self) -> None:
        """Removes old revisions from the snapshots directory.

        - Iterates through the folders within the snapshots directory.
        - Deletes any folder that does not contain the current revision ID.
        """
        # Iterate through the folders in the snapshots directory
        for snapshot in os.listdir(self.model_snapshot_dir):
            if snapshot != self.revision_id:
                # Remove the folder
                shutil.rmtree(os.path.join(self.model_snapshot_dir, snapshot), ignore_errors=True)

    def download_model(self) -> None:
        """Downloads the model and moves it to the final directory (physical path).

        - Downloads the model to the temporary directory (cache).
        - Gets the latest snapshot directory.
        - Moves the relevant model files to the final model directory if they do not exist there.
        """
        # Print a message indicating the start of the installation
        print("Installation is in progress...\n")

        # Remove older revisions
        if os.path.exists(self.model_cache_dir):
            self.remove_old_revisions()

        # Download the model to the temporary directory
        snapshot_download(repo_id=self.model_repository, allow_patterns=[f"{self.target_file_name}/*"], revision=self.revision_id)

        # Define the source directory for the relevant model files in user cache
        src_dir = os.path.join(self.model_snapshot_dir, self.revision_id, self.target_file_name)

        # Move the relevant model files from user cache folder to the models directory in the project
        if os.path.exists(src_dir):
            os.makedirs(self.model_dir_path, exist_ok=True)
            shutil.copytree(src_dir, self.model_dir_path, dirs_exist_ok=True)

    def download_model_with_retries(self) -> None:
        """Attempts to download the model with retries upon failure.
        """
        retry_delay: int = 10
        while True:
            try:
                self.download_model()
                print("Installation has been completed successfully.\n")
                return
            except Exception as exc:
                print(f"\nAttempt failed: {exc}")
                print(f"\nRetrying in {retry_delay} seconds...\n")

                # Remove model's folder
                shutil.rmtree(self.model_cache_dir, ignore_errors=True)

                time.sleep(retry_delay)
