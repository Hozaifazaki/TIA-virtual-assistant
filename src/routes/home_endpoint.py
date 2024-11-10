from typing import Dict

from fastapi import APIRouter

home_router = APIRouter()

# Add a root endpoint
@home_router.get("/")
async def root() -> Dict:
    """Returns a welcome message for the AI Assistant API.

    Returns:
        dict: A dictionary containing a "message" key with the welcome message.
    """
    return {"message": "Hello, Welcome to TIA your virtual assistant please go to /ai-assistant to start chatting"}