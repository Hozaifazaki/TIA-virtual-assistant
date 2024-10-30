import os

class PathManager:

    @classmethod
    def initialize_paths(cls, base_dir: str) -> None:
        """Initializes the paths for the project.

        Args:
            base_dir (str): The base directory for the project.
        """
        models_dir = os.path.join(base_dir, 'models')

        cls.MODEL_REPO: str = "microsoft/Phi-3-mini-4k-instruct-onnx"
        cls.TARGET_FILE_NAME: str = "cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4"

        cls.MODEL_DIR_PATH = os.path.join(models_dir,
                                          "phi_3_mini_4k_instruct_onnx_cpu",
                                          "cpu-int4-rtn-block-32-acc-level-4")

        cls.MODEL_CACHE_DIR = os.path.join(os.path.expanduser('~'),
                                           ".cache",
                                           "huggingface",
                                           "hub",
                                           "models--microsoft--Phi-3-mini-4k-instruct-onnx")
        # Commit ID
        cls.REVISION_ID = "24fd626412942b0bcd8f16393ef10b69cfc2d162"
