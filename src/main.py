import os

from fastapi import FastAPI, Depends
import uvicorn

from configs.config import Config
from utils.model_downloader import ModelDownloader
from utils.model_loader import ModelLoader
from utils.path_manager import PathManager
from services.llm_service import LLMService
from routes import home_endpoint, llm_endpoint


# Create the FastAPI app
## This initializes the FastAPI app, which will handle incoming HTTP requests.
app = FastAPI()

# Initialize paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Initialize paths for any model
PathManager.initialize_paths(
    base_dir=base_dir,
    model_repo="Orange-Innovation-Egypt/Qwen2.5-0.5B-Instruct-onnx-cpu",
    target_file=None,
    revision_id="05be32a0cc6d9b323b8f7d5739ec7070af6e2408"
)

# Download models
if Config.ONLINE_DOWNLOAD:
    ModelDownloader()

# Load models
model_loader = ModelLoader()
llm_model = model_loader.llm_model
llm_tokenizer = model_loader.llm_tokenizer
llm_streamer = model_loader.llm_streamer

# Load services
### Here we will add the service to FastAPI state in order to access it easily within the routes
app.state.llm_assistant = LLMService(llm_model, llm_tokenizer, llm_streamer)

# Include app routes/ endpoints
app.include_router(home_endpoint.home_router)
app.include_router(llm_endpoint.llm_router)


## To test without server
# def main(request: ChatInput):
#     try:
#         prompt = llm_assistant.construct_prompt_template(request["user_prompt"])
#         assistant_response = llm_assistant.generate_response(prompt)
#         print('-'*10)
#         print(assistant_response)
#         print('-'*10)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
    # uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    # main({"user_prompt": "What is the captital city of Egypt?", "webpage_content": ""})
