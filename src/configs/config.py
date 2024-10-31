class Config:
    ONLINE_DOWNLOAD = True
    BATCH_SIZE = 8

    END_TOKENS = ["<|endoftext|>", "<|end|>", "</s>", "<|assistant|>"]

    GENERATION_ARGS: dict = {
        "max_new_tokens": 256,
        "do_sample": False,
    }
