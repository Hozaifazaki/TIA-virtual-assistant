from schemas.prompts import Prompts
from configs.config import Config
from threading import Thread

class LLMService:
    def __init__(self, model, tokenizer, streamer, user_prompt, webpage_content) -> None:
        self.model = model
        self.tokenizer = tokenizer
        self.streamer = streamer
        self.user_prompt = user_prompt
        self.webpage_content = webpage_content

    def construct_prompt_template(self):
        # full_prompt = "Helper Context: " + self.webpage_content + "Question: " + self.user_prompt
        prompt_template = Prompts.PROMPT_TEMPLATE.format(system_prompt=Prompts.SYSTEM_PROMPT,
                                                         user_prompt=self.user_prompt)
        return prompt_template

    def generate_streaming_response(self, prompt: str):
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")

            # Run the generation in a separate thread
            generation_kwargs = dict(inputs, streamer=self.streamer, **Config.GENERATION_ARGS)
            thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
            thread.start()

            # Yield tokens as they become available
            for next_token in self.streamer:
                yield next_token

        except Exception as e:
            print(f"exception from generate streaming {e}")

    def generate_response(self, prompt: str):
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            response = self.model.generate(**inputs, **Config.GENERATION_ARGS)
            response = self.tokenizer.decode(response[0], skip_special_tokens=True)
            return response

        except Exception as e:
            print(f"exception {e}")