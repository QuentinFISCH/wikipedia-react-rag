"""
LLM call
"""

from transformers import AutoTokenizer, AutoModelForCausalLM


PROMPT_TEMPLATE = '''[INST] <<SYS>>{system_prompt}<</SYS>>{prompt}[/INST]'''

class LLM:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-70b-chat-hf")
        self.model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-70b-chat-hf")

    def _get_llm_output(self, input_text: str, system_prompt: str):
        """
        Get LLM output
        """
        prompt = PROMPT_TEMPLATE.format(system_prompt=system_prompt, prompt=input_text)
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        output_ids = self.model.generate(input_ids)
        output_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return output_text

    def function_call(self, input_text: str, system_prompt: str):
        """
        Retrieve the function from the LLM output
        """
        output_text = self._get_llm_output(input_text, system_prompt)
        return output_text  # .split(":")[0].strip()

    def __call__(self, input_text: str, system_prompt: str):
        """
        Call the action
        """
        return self._get_llm_output(input_text, system_prompt)
