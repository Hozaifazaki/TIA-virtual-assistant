import os
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import uvicorn

from configs.config import Config
from utils.model_downloader import ModelDownloader
from utils.model_loader import ModelLoader
from utils.path_manager import PathManager
from schemas.chat_models import ChatInput, ChatResponse
from services.llm_service import LLMService


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
llm_assistant = LLMService(llm_model, llm_tokenizer, llm_streamer)

# Create the server
## This initializes the FastAPI app, which will handle incoming HTTP requests.
app = FastAPI()


# Add a root endpoint
@app.get("/")
async def root() -> Dict:
    """Returns a welcome message for the AI Assistant API.

    Returns:
        dict: A dictionary containing a "message" key with the welcome message.
    """
    return {"message": "Welcome to the AI Assistant API"}

# Create the chat end-point
## Defines a POST endpoint /ai-assistant where users can send a question and webpage content.
### FastAPI automatically deserializes the request into a ChatInput object.
#### By marking the function as async, you allow FastAPI to handle the long-running I/O operations (like querying the LLM model) asynchronously.
##### This means that while the request is waiting for an external response (e.g., from the LLM), the server can continue to process other incoming requests.
@app.post("/ai-assistant")
async def get_response(request: ChatInput) -> StreamingResponse:
    """Processes a user's request and webpage content to generate a response using LLM model.

    Args:
        request: A ChatInput object containing the user's prompt and webpage content.

    Returns:
        StreamingResponse: A StreamingResponse object containing the assistant's response generated in chunks.
    """
    try:
        # Construct the prompt template
        prompt = llm_assistant.construct_prompt_template(request.user_prompt)

        # Start streaming response
        return StreamingResponse(llm_assistant.generate_streaming_response(prompt), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
