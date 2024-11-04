from typing import List, Tuple
from threading import Thread

from configs.config import Config
from schemas.prompts import Prompts


class LLMService:
    def __init__(self, model,
                 tokenizer, streamer) -> None:

        self.model = model
        self.tokenizer = tokenizer
        self.streamer = streamer

        # self.end_tokens = [self.tokenizer.convert_tokens_to_ids(token) for token in Config.END_TOKENS]
        self.system_kv_cache, self.system_mask = self.cache_system_prompt_kv()
        self.system_kv_cache = self.prepare_system_kv_cache()

    def construct_prompt_template(self, user_prompt: str) -> str:
        """Constructs the prompt template by combining the system prompt, user prompt, and webpage content.

        Returns:
            str: The formatted prompt template.
        """
        prompt_template = Prompts.PROMPT_TEMPLATE.format(system_prompt=Prompts.SYSTEM_PROMPT,
                                                         user_prompt=user_prompt)
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
                                     past_key_values=self.system_kv_cache,  # Reuse cached KV for system prompt
                                     use_cache=True,
                                     streamer=self.streamer,
                                    #  eos_token_id=self.end_tokens,
                                     **Config.GENERATION_ARGS)
            thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
            thread.start()

            # Yield tokens as they become available
            for next_token in self.streamer:
                yield next_token

        except Exception as e:
            print(f"Exception from generate streaming function: {e}")

    def cache_system_prompt_kv(self) -> Tuple:
            """Caches the system prompt.

            Returns:
                Tuple: kv cache and the system prompt attention_mas;
            """
            system_prompt = f"<|im_start|>system\n{Prompts.SYSTEM_PROMPT}<|im_end|>\n"
            inputs = self.tokenizer(system_prompt, return_tensors='pt')

            # Generate KV cache for the system prompt
            outputs = self.model(**inputs, use_cache=True)
            system_kv_cache = outputs.past_key_values
            
            return system_kv_cache, inputs['attention_mask']

    def prepare_system_kv_cache(self) -> List:
        """Expand the system prompt KV cache to match the batch size.

        Returns:
            list: List of system prompt matched the batch size.
        """
        # Expand the system prompt KV cache to match the batch size
        expanded_kv_cache = []
        for layer_past in self.system_kv_cache:
            expanded_layer_past = []
            for tensor in layer_past:
                # Expand and repeat the tensor along the batch dimension
                expanded_tensor = tensor.expand(Config.BATCH_SIZE, -1, -1, -1)
                expanded_layer_past.append(expanded_tensor)
            expanded_kv_cache.append(tuple(expanded_layer_past))

        return expanded_kv_cache
        
    def generate_response(self, prompt: str) -> str:
        """Generates a non-streaming response to the given prompt.

        Args:
            prompt (str): The input prompt.

        Returns:
            str: The generated response.
        """
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            # attention_mask = torch.cat([self.system_mask, inputs['attention_mask']], dim=1)

            response = self.model.generate(**inputs,
                                        #    past_key_values=self.system_kv_cache,
                                        #    use_cache=True, 
                                           **Config.GENERATION_ARGS)
            response = self.tokenizer.decode(response[0], skip_special_tokens=False)
            return response

        except Exception as e:
            print(f"Exception: {e}")
