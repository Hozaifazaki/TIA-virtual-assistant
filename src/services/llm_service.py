from models.prompts import Prompts

class LLMService:
    def __init__(self, model, tokenizer, user_prompt, webpage_content) -> None:
        self.model = model
        self.tokenizer = tokenizer
        self.user_prompt = user_prompt
        self.webpage_content = webpage_content

    def construct_prompt_template(self):
        prompt_template = Prompts.PROMPT_TEMPLATE.format(system_prompt=Prompts.SYSTEM_PROMPT, 
                                                         user_prompt=self.user_prompt)
        return prompt_template

    def generate_response(self, prompt: str):
        response = self.model.run(prompt)
        return response