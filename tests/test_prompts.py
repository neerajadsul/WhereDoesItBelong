from pathlib import Path
import pytest

from llms.prompts import QuestionAnswerPromptCrafter, ClassifyPromptCrafter

TEST_PATH = Path(__file__).resolve().parent


def test_question_answer_prompt_crafter():
    data = '''{"justify": true, "thing1": "Mercury", "thing2": "Mars"}'''

    crafter = QuestionAnswerPromptCrafter(TEST_PATH / 'assets/prompt_templates/prompt_bigger_item.txt')
    prompt = crafter.craft_prompt(data)
    print(prompt)
    assert len(prompt.splitlines()) == 6


def test_classify_prompt_crafter():
    data = '''{ "classes": [
        {
            "class_id": "C1",
            "class_name": "Chocolate Ice Cream",
            "class_description": "With real chocolate"
        },
        {
            "class_id": "V1",
            "class_name": "Vanilla Ice Cream",
            "class_description": "Made with real Madagascan vanilla"
        },
        {
            "class_id": "CO1",
            "class_name": "Coconut Ice Cream",
            "class_description": "Made with real coconut milk"
        },
        {
            "class_id": "RR1",
            "class_name": "Rum and Raisin Ice Cream",
            "class_description": "With rum-soaked raisins"
        }
    ],
    "options": {
        "multilabel": true
    },
    "query": "Can I get a scoop of vanilla and a scoop of chocolate?"
    }
    '''
    crafter = ClassifyPromptCrafter(TEST_PATH.parent / 'prompt_templates/prompt1.txt')
    prompt = crafter.craft_prompt(data)
    print(prompt)
    assert len(prompt.splitlines()) == 14