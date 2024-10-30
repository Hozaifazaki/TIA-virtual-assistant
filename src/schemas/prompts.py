class Prompts:
    SYSTEM_PROMPT = "You are a helpful assistant"

    DEAFUALT_RESPONSE = "How can I help you!"

    PROMPT_TEMPLATE = """<|system|>\n{system_prompt}<|end|>\n<|user|>\n{user_prompt}<|end|>\n<assistant>\n"""

