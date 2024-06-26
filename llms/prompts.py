from abc import ABC, abstractmethod
import re
import os
import json
from pathlib import Path
from jinja2 import Template


class PromptCrafter(ABC):
    """Crafts final prompt replacing template fields with data or conditional prompt changes."""

    def __init__(self, prompt_template_file):
        if not os.path.exists(prompt_template_file):
            raise FileNotFoundError(f'Prompt template not found: {prompt_template_file}')

        with open(prompt_template_file, 'rt') as fp:
            self._raw_prompt = fp.read()

        self.template = Template(self._raw_prompt)

    @abstractmethod
    def craft_prompt(self, data):
        pass


class QuestionAnswerPromptCrafter(PromptCrafter):
    def __init__(self, prompt_template_file):
        super().__init__(prompt_template_file)
    def craft_prompt(self, sdata):
        data = json.loads(sdata)
        justify = " and a justify in a single sentence with minimum words possible but no more than 15."
        prompt = self.template.render(
            justify=justify if data['justify'] else '',
            thing1=data['thing1'],
            thing2=data['thing2']
        )
        return prompt




class ClassifyPromptCrafter(PromptCrafter):
    """Create prompt for classifying given query text into one of the provided classes."""
    def craft_prompt(self, data):
        data = json.loads(data)
        query_text = data['query']
        categories = data['classes']
        categories = [f"{d['class_id']}, {d['class_name']}, {d['class_description']}" for d in categories]
        categories = '\n'.join(categories)

        multilabel = 'or more ' if data['options']['multilabel'] else ''
        if data['options'].get('show_reasoning', True):
            show_reasoning = 'Provide reasoning for the decision in a maximum 15 word long sentence.'
        else:
            show_reasoning = ''

        prompt2 = self.template.render(
            query_text=query_text,
            categories = categories,
            multilabel = multilabel,
            show_reasoning = show_reasoning
        )

        return prompt2


if __name__ == "__main__":
    path = Path(__file__).resolve().parent.parent
    crafer = ClassifyPromptCrafter(path / 'prompt_templates/prompt3.txt')
    data = """{
    "query": "the text to be classified",
    "options": {
      "multilabel": true,
      "show_reasoning": true
    },
    "classes": [
        {
            "class_id": "C1",
            "class_name": "Class 1",
            "class_description": "Description of class 1"
        },
        {
            "class_id": "C2",
            "class_name": "Class 2",
            "class_description": "Description of class 2"
        }
    ]
    }"""
    print(crafer.craft_prompt(data))