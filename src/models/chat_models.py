from pydantic import BaseModel



class ChatInput(BaseModel):
    user_prompt: str
    webpage_content: str

class ChatResponse(BaseModel):
    assistant_response: str
