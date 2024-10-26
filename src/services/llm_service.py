
from models.data_models import Prompts

class AIAssistant:
    def __init__(self, user_prompt, webpage_content, tokenizer) -> None:
        self.user_prompt = user_prompt
        self.webpage_content = webpage_content
        self.tokenizer = tokenizer

    def construct_prompt_template(self):
        messages = [
            {
                "role": "system",
                "content": Prompts.system_prompt
            },
            {
                "role": "user",
                "content": self.user_prompt
            }
        ]
        prompt_template = self.tokenizer.apply_chat_tempalte(messages, add_generation_tokens=True)
        return prompt_template
    
    def generate_response(self):
        return f"Your prompt is {self.user_prompt}"