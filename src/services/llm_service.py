from models.data_models import Prompts

class LLMService:
    def __init__(self, model, tokenizer, user_prompt, webpage_content) -> None:
        self.model = model
        self.tokenizer = tokenizer
        self.user_prompt = user_prompt
        self.webpage_content = webpage_content

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

    def generate_response(self, prompt: str):
        response = self.model(prompt)
        return response