import os
import uvicorn
from fastapi import FastAPI, HTTPException
from models.chat_models import ChatInput, ChatResponse
from services.llm_service import LLMService
from configs.config import Config
from utils.model_loader import ModelLoader
from utils.model_downloader import ModelDownloader
from utils.path_util import PathUtil


# Initialize paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PathUtil.initialize_paths(base_dir)

# Download models
if Config.ONLINE_DOWNLOAD:
    ModelDownloader()

# Load models
model_loader = ModelLoader()
llm_model = model_loader.llm_model

# Create the server
## This initializes the FastAPI app, which will handle incoming HTTP requests.
app = FastAPI()

# Create the chat end-point
## Defines a POST endpoint /ai-assistant where users can send a question and webpage content.
### FastAPI automatically deserializes the request into a ChatInput object.
#### By marking the function as async, you allow FastAPI to handle the long-running I/O operations (like querying the LLM model) asynchronously.
##### This means that while the request is waiting for an external response (e.g., from the LLM), the server can continue to process other incoming requests.
@app.post("/ai-assistant")
async def get_response(request: ChatInput):
    try:
        print(request.user_prompt, request.webpage_content)
        llm_model.warm_up()
        llm_assistant = LLMService(llm_model, request.user_prompt, request.webpage_content)

        prompt = llm_assistant.construct_prompt_template()
        assistant_response = llm_assistant.generate_response(prompt)
        return ChatResponse(assistant_response=assistant_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
