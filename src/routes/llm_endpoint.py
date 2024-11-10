

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse

from schemas.chat_models import ChatInput
from services.llm_service import LLMService

# APIRouter class, used to group path operations, for example to structure an app in multiple files. 
# It would then be included in the FastAPI app,
llm_router = APIRouter()

# Create the chat end-point
## Defines a POST endpoint /ai-assistant where users can send a question and webpage content.
### FastAPI automatically deserializes the request into a ChatInput object.
#### By marking the function as async, you allow FastAPI to handle the long-running I/O operations (like querying the LLM model) asynchronously.
##### This means that while the request is waiting for an external response (e.g., from the LLM), the server can continue to process other incoming requests.
@llm_router.post("/ai-assistant")
async def get_response(http_request: ChatInput, app_state: Request) -> StreamingResponse:
    """Processes a user's request and webpage content to generate a response using LLM model.
    
    This endpoint retrieves the LLM service instance (`llm_assistant`) from the application state and 
    uses it to construct a prompt based on the user's request (`request.user_prompt`). The prompt is then 
    used by the LLM service to generate a response which is streamed back to the client.
    
    Args:
        http_request (ChatInput): A Pydantic model containing the user's prompt and webpage content.
        app_state (Request): The FastAPI request object used to retrieve the LLM service instance from the application state.

    Returns:
        StreamingResponse: A StreamingResponse object containing the assistant's response generated in chunks.
    """
    try:
        # Retrive the service from the app's state
        llm_assistant: LLMService = app_state.app.state.llm_assistant

        # Construct the prompt template
        prompt = llm_assistant.construct_prompt_template(http_request.user_prompt)

        # Start streaming response
        return StreamingResponse(llm_assistant.generate_streaming_response(prompt), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))