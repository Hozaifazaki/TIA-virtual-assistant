from ctransformers import AutoModelForCausalLM, AutoTokenizer

from utils.path_util import PathUtil

class ModelLoader:
    _initialized = False

    def __init__(self):
        if not self._initialized:
            self.llm_model = None
            self.llm_tokenizer = None

            # Load model
            self.load_models()
            self._initialized = True

    def load_models(self):
        if not self.llm_model:
            self.llm_model = AutoModelForCausalLM.from_pretrained(model_path_or_repo_id=PathUtil.MODEL_PATH,
                                                                  model_file=PathUtil.GGUF_FILE_NAME,
                                                                  gpu_layers=0)
            self.llm_tokenizer = AutoTokenizer(self.llm_model)
