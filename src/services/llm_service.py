from threading import Thread

from configs.config import Config
from schemas.prompts import Prompts


class LLMService:
    def __init__(self, model,
                 tokenizer, streamer,
                 user_prompt, webpage_content) -> None:

        self.model = model
        self.tokenizer = tokenizer
        self.streamer = streamer
        self.user_prompt = user_prompt
        self.webpage_content = webpage_content

        self.end_tokens = [self.tokenizer.convert_tokens_to_ids(token) for token in Config.END_TOKENS]

    def construct_prompt_template(self) -> str:
        """Constructs the prompt template by combining the system prompt, user prompt, and webpage content.

        Returns:
            str: The formatted prompt template.
        """
        # full_prompt = "Helper Context: " + self.webpage_content + "Question: " + self.user_prompt
        prompt_template = Prompts.PROMPT_TEMPLATE.format(system_prompt=Prompts.SYSTEM_PROMPT,
                                                         user_prompt=self.user_prompt)
        return prompt_template

    def generate_streaming_response(self, prompt: str) -> str:
        """
        Generates a streaming response to the given prompt.

        Args:
            prompt (str): The input prompt.

        Yields:
            str: The generated tokens as they become available.
        """
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")

            # Run the generation in a separate thread
            generation_kwargs = dict(inputs,
                                     streamer=self.streamer,
                                     eos_token_id=self.end_tokens,
                                     **Config.GENERATION_ARGS)
            thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
            thread.start()

            # Yield tokens as they become available
            for next_token in self.streamer:
                yield next_token

        except Exception as e:
            print(f"Exception from generate streaming function: {e}")

    def generate_response(self, prompt: str) -> str:
        """Generates a non-streaming response to the given prompt.

        Args:
            prompt (str): The input prompt.

        Returns:
            str: The generated response.
        """
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            response = self.model.generate(**inputs, **Config.GENERATION_ARGS)
            response = self.tokenizer.decode(response[0], skip_special_tokens=False)
            return response

        except Exception as e:
            print(f"Exception: {e}")
