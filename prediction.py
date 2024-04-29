import json
import logging
import random
import os
from pathlib import Path
import re

import openai

from llms.openai_gpt import OpenAIAssistant
from llms.prompts import ClassifyPromptCrafter
from llms.datastores import LogFiles


RESPONSE_DATA_PATH = Path(os.getenv('HOME')) / '.gptlog' / 'responses'
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
        self.crafter = ClassifyPromptCrafter(PROMPT_TEMPLATES_PATH / 'prompt3.txt')
        self.assistant = OpenAIAssistant(
            model='gpt-3.5-turbo',
            prompt_crafter=self.crafter,
            datastore=self.datastore,
            response_format='json'
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

    def format_result_from_plain(self, message):
        result_regex = re.compile(r'\[{1}.+\]{1}')
        result = result_regex.findall(message)
        result = [s.strip() for s in result[0][1:-1].split(',')]
        reasoning_regex = re.compile(r'```{1}.+```{1}')
        reasoning = reasoning_regex.findall(message)
        result = { 'result': result, 'reasoning': reasoning}
        return result
        
    def format_result_from_json(self, message):
        try:
            f_message = json.loads(message)
        except json.decoder.JSONDecodeError as e:
            logger.error(e)
            logger.info(message)
            f_message = json.dumps({'result': [], 'reasoning': 'Error encountered while classifying.'})
        else:
            if len(f_message) == 0:
                return {'result': []}

            for name in ['ids', 'categories', 'classes']:
                if name in f_message:
                    f_message['result'] = f_message.get(name, [])
                    break

        return f_message
