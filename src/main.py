import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from schemas.chat_models import ChatInput, ChatResponse
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
llm_tokenizer = model_loader.llm_tokenizer
llm_streamer = model_loader.llm_streamer

# Create the server
## This initializes the FastAPI app, which will handle incoming HTTP requests.
app = FastAPI()


# Add a root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the AI Assistant API"}

# Create the chat end-point
## Defines a POST endpoint /ai-assistant where users can send a question and webpage content.
### FastAPI automatically deserializes the request into a ChatInput object.
#### By marking the function as async, you allow FastAPI to handle the long-running I/O operations (like querying the LLM model) asynchronously.
##### This means that while the request is waiting for an external response (e.g., from the LLM), the server can continue to process other incoming requests.
@app.post("/ai-assistant")
async def get_response(request: ChatInput):
    try:
        # print(request.user_prompt, request.webpage_content)
        llm_assistant = LLMService(llm_model,
                                   llm_tokenizer,
                                   llm_streamer,
                                   request.user_prompt,
                                   request.webpage_content)

        # Construct the prompt template
        prompt = llm_assistant.construct_prompt_template()

        # Start streaming response
        return StreamingResponse(llm_assistant.generate_streaming_response(prompt), media_type="text/event-stream")

        ## For single response
        # assistant_response = llm_assistant.generate_response(prompt)
        # return ChatResponse(assistant_response=assistant_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To test without server
# def main(request: ChatInput):
#     try:
#         llm_assistant = LLMService(llm_model, llm_tokenizer, request['user_prompt'], request['webpage_content'])

#         prompt = llm_assistant.construct_prompt_template()
#         assistant_response = llm_assistant.generate_response(prompt)
#         print('-'*10)
#         print(assistant_response)
#         print('-'*10)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
    ## To debug
    # uvicorn.run("main:app", host="localhost", port=8000, reload=True, log_level="debug")

    # main({"user_prompt": "What is the main topic of this page?", "webpage_content": "This is the content of the webpage. It discusses various topics related to artificial intelligence and machine learning."})
