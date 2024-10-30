import os
from utils.path_util import PathUtil
from optimum.onnxruntime import ORTModelForCausalLM
from transformers import AutoTokenizer, TextIteratorStreamer

class ModelLoader:
    _initialized = False

    def __init__(self):
        if not self._initialized:
            # Text Generation
            self.llm_model = None
            self.llm_tokenizer = None
            self.llm_streamer = None

            # Load model
            self.load_models()
            self._initialized = True

    def load_models(self):
        if not self.llm_model:
            self.llm_model = ORTModelForCausalLM.from_pretrained(
                PathUtil.MODEL_DIR_PATH,
                file_name=os.path.join(PathUtil.MODEL_DIR_PATH,
                                               "phi3-mini-4k-instruct-cpu-int4-rtn-block-32-acc-level-4.onnx"),
                decoder_with_past_file_name=os.path.join(PathUtil.MODEL_DIR_PATH,
                                                         "phi3-mini-4k-instruct-cpu-int4-rtn-block-32-acc-level-4.onnx"),
                use_merged=True,
                provider="CPUExecutionProvider",
                trust_remote_code=True,
                local_files_only=True
            )
            self.llm_tokenizer = AutoTokenizer.from_pretrained(PathUtil.MODEL_DIR_PATH)

            # Load streamer as an iterator
            self.llm_streamer = TextIteratorStreamer(self.llm_tokenizer, skip_prompt=True, skip_special_tokens=True)