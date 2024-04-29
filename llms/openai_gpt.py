import os
from pathlib import Path
import json
import time

from openai import OpenAI

from .llms import ChatAssistant
from .prompts import ClassifyPromptCrafter
from .datastores import LogFiles


class OpenAIAssistant(ChatAssistant):
    def __init__(self, model, prompt_crafter, datastore):
        self.model = model
        self.datastore = datastore
        self.prompt_crafter = prompt_crafter

        if os.getenv('OPENAI_SECRET_KEY') is None:
            raise EnvironmentError('API Key not set.')
        self.client = OpenAI(api_key=os.getenv('OPENAI_SECRET_KEY'))

    def get_completion(self, data):
        prompt = self.prompt_crafter.craft_prompt(data)
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            response_format={"type": "json_object"}
        )
        return response

    def get_message(self, response):
        return response.choices[0].message.content

    def log_response(self, response):
        """Records full response to setup datastore."""
        data = json.dumps(json.loads(response.model_dump_json()), indent=4)
        self.datastore.save(data)


if __name__ == "__main__":
    RESPONSE_PATH = Path(os.getenv('HOME')) / 'GptResponses'
    datastore = LogFiles(log_path=RESPONSE_PATH)
    FPATH = Path(__file__).resolve().parent.parent
    crafter = ClassifyPromptCrafter(FPATH / 'prompt_templates/prompt1.txt')
    assistant = OpenAIAssistant(
        model='gpt-3.5-turbo',
        prompt_crafter=crafter,
        datastore=datastore
    )

