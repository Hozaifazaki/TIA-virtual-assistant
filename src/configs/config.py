class Config:
    BATCH_SIZE = 8

    GENERATION_ARGS: dict = {
        "max_new_tokens": 1024,
        "do_sample": False,
    }
