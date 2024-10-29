from schemas.prompts import Prompts

class LLMService:
    def __init__(self, model, user_prompt, webpage_content) -> None:
        self.model = model
        self.user_prompt = user_prompt
        self.webpage_content = webpage_content

    def construct_prompt_template(self):
        full_prompt = "Helper Context: " + self.webpage_content + "Question: " + self.user_prompt
        prompt_template = Prompts.PROMPT_TEMPLATE.format(system_prompt=Prompts.SYSTEM_PROMPT, 
                                                         user_prompt=full_prompt)
        return prompt_template

    def generate_response(self, prompt: str):
        print(prompt)
        response = self.model.run(prompt)
        return response