import os
from utils.path_util import PathUtil
from configs.config import Config
from haystack_integrations.components.generators.llama_cpp import LlamaCppGenerator


class ModelLoader:
    _initialized = False

    def __init__(self):
        if not self._initialized:
            self.llm_model = None

            # Load model
            self.load_models()
            self._initialized = True

    def load_models(self):
        if not self.llm_model:
            self.llm_model = LlamaCppGenerator(
                                model=os.path.join(PathUtil.MODEL_DIR_PATH, PathUtil.GGUF_FILE_NAME),
                                # n_ctx=512,
                                # n_batch=128,
                                # model_kwargs={"n_gpu_layers": -1},
                                generation_kwargs=Config.GENERATION_ARGS,
                            )
