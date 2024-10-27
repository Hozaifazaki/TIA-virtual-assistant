class Config:
    ONLINE_DOWNLOAD = True
    BATCH_SIZE = 8

    GENERATION_ARGS: dict = {
        "max_new_tokens": 1024,
        "temprature": 0.1,
    }
