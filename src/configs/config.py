class Config:
    ONLINE_DOWNLOAD = True
    BATCH_SIZE = 8

    GENERATION_ARGS: dict = {
        "max_new_tokens": 256,
        "do_sample": True,
        "temperature": 0.2,
    }
