import os
import shutil
import time

from huggingface_hub import snapshot_download #, utils
from utils.path_util import PathUtil


class ModelDownloader:
    def __init__(self):
        # Initialize model paths
        self.initialize_model_paths()

        # Disable progress bars in Hugging Face utilities
        # utils.disable_progress_bars()

        # Start the model download process
        self.start_download()

    def initialize_model_paths(self):
        """Initializes the paths for model repository, directory, name, and cache based on GPU availability.

        - If a GPU is available, sets paths for CUDA models.
        - If a GPU is not available, sets paths for CPU models.

        Paths:
            - `onnx_generator_cpu_model_path`: Path to the CPU version of the model.
            - `onnx_generator_cuda_model_path`: Path to the CUDA version of the model.
            - `onnx_model_cpu_repository`: Model repository for the CPU version on Hugging Face.
            - `onnx_model_cuda_repository`: Model repository for the CUDA version on Hugging Face.
            - `model_cache_cpu_dir`: Path to the user cache for the CPU model.
            - `model_cache_cuda_dir`: Path to the user cache for the CUDA model.
        """
        self.model_repository: str = PathUtil.MODEL_REPO
        self.model_dir_path: str = PathUtil.MODEL_DIR_PATH
        self.model_name: str = PathUtil.GGUF_FILE_NAME
        self.model_cache_dir: str = PathUtil.MODEL_CACHE_DIR
        self.revision_id: str = PathUtil.REVISION_ID
        self.model_snapshot_dir: str = os.path.join(self.model_cache_dir, "snapshots")

    def start_download(self) -> None:
        """Starts the model download process if the model path does not exist.

        - Model path: (e.g. models\\step_04_phi3_vision_onnx_cpu\\cpu-int4-rtn-block-32-acc-level-4)
        """
        if not os.path.exists(self.model_dir_path):
            self.download_model_with_retries()

    def remove_old_revisions(self) -> None:
        """Removes old revisions from the snapshots directory.

        - Iterates through the folders within the snapshots directory.
        - Deletes any folder that does not contain the current revision ID.

        Args:
            self: The instance of the class containing this method.
        """
        # Iterate through the folders in the snapshots directory
        for snapshot in os.listdir(self.model_snapshot_dir):
            # Check if the current revision ID is not in the folder name
            print(snapshot)
            if snapshot != self.revision_id:
                # Remove the folder
                shutil.rmtree(os.path.join(self.model_snapshot_dir, snapshot), ignore_errors=True)

    def download_model(self) -> None:
        """Downloads the model and moves it to the final directory (physical path).

        - Downloads the model to the temporary directory (cache).
            - (e.g. user_name\\.cache\\huggingface\\hub\\)
        - Gets the latest snapshot directory.
            - This is a temp folder created with a temp name
        - Moves the relevant model files to the final model directory if they do not exist there.
        """
        # Print a message indicating the start of the installation
        print("Installation is in progress...\n")

        # Remove older revisions
        if os.path.exists(self.model_cache_dir):
            self.remove_old_revisions()

        # Download the model to the temporary directory
        # `allow_patterns`: is used to download a specific folder from huggingface repository of the model
        snapshot_download(repo_id=self.model_repository, allow_patterns=[f"{self.model_name}"], revision=self.revision_id)

        # Define the source directory for the relevant model files in user cache
        src_dir = os.path.join(self.model_snapshot_dir, self.revision_id, self.model_name)

        # Move the relevant model files from user cache folder to the models directory in the project
        # if not exist in the models directory
        if os.path.exists(src_dir):
            os.makedirs(self.model_dir_path, exist_ok=True)
            shutil.copy2(src_dir, self.model_dir_path)

    def download_model_with_retries(self) -> None:
        """Attempts to download the model with retries upon failure.

        - Sets a retry delay 10 seconds.
        - Attempts to download the model.
        - Prints a success message upon successful download.
        - If an exception occurs:
            - Prints an error message and retries upon failure.
            - Removes the model's folder and delays for some time before retrying.
        """
        retry_delay: int = 10
        while True:
            try:
                # Attempt to download the model
                self.download_model()
                # Print success message upon successful download
                print("Installation has been completed successfully.\n")
                return
            except Exception as exc:
                # Print an error message and retry upon failure
                print(f"\nAttempt failed: {exc}")
                print(f"\nRetrying in {retry_delay} seconds...\n")

                # Remove model's folder
                shutil.rmtree(self.model_cache_dir, ignore_errors=True)
                # Delay for some time
                time.sleep(retry_delay)
