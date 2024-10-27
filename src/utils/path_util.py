import os

class PathUtil:

    @classmethod   
    def initialize_paths(cls, base_dir):
        models_dir = os.path.join(base_dir, 'models')

        cls.MODEL_REPO: str = "microsoft/Phi-3-mini-4k-instruct-gguf"
        cls.GGUF_FILE_NAME: str = "Phi-3-mini-4k-instruct-q4.gguf"

        cls.MODEL_DIR_PATH = os.path.join(models_dir, "Phi_3_mini_4k_instruct_gguf")
        cls.MODEL_CACHE_DIR = os.path.join(os.path.expanduser('~'),
                                           ".cache",
                                           "huggingface",
                                           "hub",
                                           "models--microsoft--Phi-3-mini-4k-instruct-gguf")
        # Commit ID
        cls.REVISION_ID = "999f761fe19e26cf1a339a5ec5f9f201301cbb83"

