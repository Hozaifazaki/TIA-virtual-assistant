class Config:
    ONLINE_DOWNLOAD = True
    BATCH_SIZE = 8

    GENERATION_ARGS: dict = {
        "max_tokens": 1024,
        "temperature": 0.1,
    }
