from pathlib import Path
import pytest

from llms.prompts import QuestionAnswerPromptCrafter
from llms.openai_gpt import OpenAIAssistant
from llms.datastores import LogFiles


TEST_PATH = Path(__file__).resolve().parent


@pytest.fixture
def assistant():
    crafter = QuestionAnswerPromptCrafter(TEST_PATH / 'assets/prompt_templates/prompt_bigger_item.txt')
    datastore = LogFiles(log_path=TEST_PATH/'assets/temp')
    assistant = OpenAIAssistant(
        model='gpt-3.5-turbo',
        prompt_crafter=crafter,
        datastore=datastore,
    )
    return assistant


def test_openai_gpt(assistant):
    data = {
        'justify': ' and a justfy in a single sentence with minimum words possible but no more than 15.',
        'thing1': 'Mercury',
        'thing2': 'Mars'
    }
    result = assistant.get_completion(data)
    message = assistant.get_message(result)
    print(message)