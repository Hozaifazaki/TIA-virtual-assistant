import os

from optimum.onnxruntime import ORTModelForCausalLM
from transformers import AutoTokenizer, TextIteratorStreamer

from utils.path_manager import PathManager


class ModelLoader:
    _initialized = False

    def __init__(self) -> None:
        if not self._initialized:
            # Text Generation
            self.llm_model = None
            self.llm_tokenizer = None
            self.llm_streamer = None

            # Load model
            self.load_models()
            self._initialized = True
    
    def _find_onnx_file(self) -> None:
        """Finds the ONNX file in the model directory and stores its name in PathManager.
        """
        for root, _, files in os.walk(PathManager.MODEL_DIR_PATH):
            for file in files:
                if file.endswith('.onnx'):
                    return file

    def load_models(self) -> None:
        """Loads the models and tokenizers.
        """
        if not self.llm_model:
            onnx_file_name = self._find_onnx_file()
            
            self.llm_model = ORTModelForCausalLM.from_pretrained(
                PathManager.MODEL_DIR_PATH,
                file_name=os.path.join(PathManager.MODEL_DIR_PATH, onnx_file_name),
                decoder_with_past_file_name=os.path.join(PathManager.MODEL_DIR_PATH, onnx_file_name),
                use_merged=True,
                trust_remote_code=True,
                local_files_only=True,
                provider="CPUExecutionProvider"
            )
            self.llm_tokenizer = AutoTokenizer.from_pretrained(PathManager.MODEL_DIR_PATH)

            # Load streamer as an iterator
            self.llm_streamer = TextIteratorStreamer(self.llm_tokenizer, skip_prompt=True, skip_special_tokens=False)
