from schemas.prompts import Prompts
from configs.config import Config

class LLMService:
    def __init__(self, model, tokenizer, user_prompt, webpage_content) -> None:
        self.model = model
        self.tokenizer = tokenizer
        self.user_prompt = user_prompt
        self.webpage_content = webpage_content

    def construct_prompt_template(self):
        # full_prompt = "Helper Context: " + self.webpage_content + "Question: " + self.user_prompt
        prompt_template = Prompts.PROMPT_TEMPLATE.format(system_prompt=Prompts.SYSTEM_PROMPT,
                                                         user_prompt=self.user_prompt)
        return prompt_template

    def generate_response(self, prompt: str):
        try:
            print("before tokenization")
            # print(self.tokenizer)
            inputs = self.tokenizer(prompt, return_tensors="pt")
            print(f"after tokenization inputs: {inputs}")

            response = self.model.generate(**inputs, **Config.GENERATION_ARGS)
            print(f"after generation: {response}")

            response = self.tokenizer.decode(response[0], skip_special_tokens=True)
            print(f"after decoding: {response}")

            return response

        except Exception as e:
            print(f"exception {e}")