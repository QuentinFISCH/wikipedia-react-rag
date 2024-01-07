import requests
from langchain.prompts import ChatPromptTemplate
from langchain.llms import HuggingFaceEndpoint
from langchain.schema.output_parser import StrOutputParser

from react.prompt import ReAct_Prompt

HF_API_KEY = "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"
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


mistral_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
model_endpoint = HuggingFaceEndpoint(
    endpoint_url=mistral_url,
    huggingfacehub_api_token=HF_API_KEY,
    task="text2text-generation",
)
template = "[INST] {prompt} [/INST]"

class MistralOutputParser(StrOutputParser):
    """OutputParser that parser llm result from Mistral API"""

    def parse(self, text: str) -> str:
        """
        Returns the input text with no changes.

        Args:
            text (str): text to parse

        Returns:
            str: parsed text
        """
        return text.split("[/INST]")[-1].strip()


class StreamCompletion:
    def __init__(self, model: str):
        # self.pipeline = MistralPipeline(model=model)
        self.model = model

    def __call__(self, message: str, system_prompt: str):
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("user", "[INST] {prompt} [/INST]"),
            ]
        )
        output_parser = MistralOutputParser()
        
        try:
            chain = prompt_template | model_endpoint | output_parser
            yield chain.invoke({"prompt": message})
            # for resp in self.pipeline(messages, stream=True, temperature=0.2, max_tokens=2_000):
            #     content = resp.get("text")
            #     if content is not None:
            #         yield content
        except Exception as err:
            print(err)


# Example usage
stream_completion = StreamCompletion(model="bigscience/mistral-13b")
for content in stream_completion("Question: how old am I?" + "\nSearchKB with search_text: \"user's age\"\nSearch Result: I am a 15 years old boy", ReAct_Prompt):
    print(content)
