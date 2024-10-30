from pydantic import BaseModel


class ChatInput(BaseModel):
    """Represents the input.

    Args:
        user_prompt (str): The prompt provided by the user.
        webpage_content (str): The content of the webpage to be considered.
    """
    user_prompt: str
    webpage_content: str

class ChatResponse(BaseModel):
    """Represents the output/response.

    Args:
        assistant_response (str): The response generated by the assistant.
    """
    assistant_response: str
