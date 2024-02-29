"""
LLM call
"""

import json
import requests
from transformers import AutoTokenizer, AutoModelForCausalLM

PROMPT_TEMPLATE = '''[INST] <<SYS>>
{system_prompt}
<</SYS>> [/INST]
[INST] The user input is: {prompt}
What is the next action?
[/INST]
'''


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


class LLM_local:
    def __init__(self) -> None:
        self._url = 'http://localhost:11434/api/generate'
        self._headers = {'Content-Type': 'application/json'}
        self._model = "llama2"

    def _get_llm_output(self, input_text: str, system_prompt: str):
        """
        Get LLM output
        """
        prompt = PROMPT_TEMPLATE.format(system_prompt=system_prompt, prompt=input_text)
        data = {
            "model": self._model,
            "prompt": prompt
        }
        response = requests.post(self._url, data=json.dumps(data), headers=self._headers, stream=True)
        full_response = []
        try:
            for line in response.iter_lines():
                # filter out keep-alive new lines
                if line:
                    decoded_line = json.loads(line.decode('utf-8'))
                    # print(decoded_line['response'])  # uncomment to results, token by token
                    full_response.append(decoded_line['response'])
        finally:
            response.close()
        return ''.join(full_response)

    def function_call(self, input_text: str, system_prompt: str):
        """
        Retrieve the function from the LLM output
        """
        output_text = self._get_llm_output(input_text, system_prompt)
        # keep the first line of the output
        output_text = output_text.split("\n")[0]
        # parse output to get function name and arguments
        out_split = output_text.split(":")
        function = out_split[0].strip()
        arguments = ":".join(out_split[1:]).strip()
        print(output_text)
        print(arguments)
        if function == "FinalAnswer":
            return function, {"reached_final_answer": True}
        if function == "Action":
            search_text = arguments.split("search_text")[1].strip().replace('"', "").strip()
            return function, {"search_text": search_text}
        if function == "Thought":
            return function, {"thought_text": arguments}
        if function == "Observation":
            return function, {"observation_text": arguments}
        return function, {"arguments": arguments}

    def __call__(self, input_text: str, system_prompt: str):
        """
        Call the action
        """
        return self._get_llm_output(input_text, system_prompt)
