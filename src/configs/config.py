class Config:
    ONLINE_DOWNLOAD = True
    BATCH_SIZE = 1

    # END_TOKENS = ["<|endoftext|>", "<|end|>", "</s>", "<|assistant|>"]

    GENERATION_ARGS: dict = {
        "max_new_tokens": 1024,
        "do_sample": False,
    }
