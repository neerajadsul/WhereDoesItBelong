import json
import logging
import random
import os
from pathlib import Path

import openai

from llms.openai_gpt import OpenAIAssistant
from llms.prompts import ClassifyPromptCrafter
from llms.datastores import LogFiles


RESPONSE_DATA_PATH = Path(os.getenv('HOME')) / 'GptResponses'
PROMPT_TEMPLATES_PATH = Path(__file__).resolve().parent / 'prompt_templates'

logger = logging.getLogger()

def mock_completion_random(prompt, categories, query_text, options):
    """Random classification for testing baseline."""
    multiclass, reasoning = options
    query = set(query_text.split())
    N = 2 if multiclass else 1
    result = [random.choice(categories) for _ in range(N)]
    return [res['class_id'] for res in result]


class Prediction:
    def __init__(self):
        self.datastore = LogFiles(log_path=RESPONSE_DATA_PATH)
        self.crafter = ClassifyPromptCrafter(PROMPT_TEMPLATES_PATH / 'prompt1.txt')
        self.assistant = OpenAIAssistant(
            model='gpt-3.5-turbo',
            prompt_crafter=self.crafter,
            datastore=self.datastore
        )

    def predict(self, data):
        #TODO: Add caching, async call perhaps
        try:
            response = self.assistant.get_completion(data)
        except openai.RateLimitError as e:
            return json.dumps({'result': e.message})
        else:
            message = self.assistant.get_message(response)
            self.assistant.log_response(response)

        return message

    def format_result(self, message):
        try:
            message = json.loads(message)
        except json.decoder.JSONDecodeError as e:
            logger.error(e)
            logger.info(message)
            message = json.dumps({'result': [], 'reasoning': 'Error encountered while classifying.'})
        else:
            for name in ['ids', 'categories', 'classes']:
                if name in message:
                    message['result'] = message.get(name, [])
                    del message[name]
                    break
        return message
