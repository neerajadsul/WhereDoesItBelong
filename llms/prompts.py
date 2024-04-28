from abc import ABC, abstractmethod
import re
import os
import json
from pathlib import Path


class PromptCrafter(ABC):
    """Crafts final prompt replacing template fields with data or conditional prompt changes."""

    def __init__(self, prompt_template_file):
        if not os.path.exists(prompt_template_file):
            raise FileNotFoundError(f'Prompt template not found: {prompt_template_file}')

        with open(prompt_template_file, 'rt') as fp:
            self._raw_prompt = fp.read()
        # Regex to find all template fields enclosed in curly braces
        regex_fields = re.compile(r'\{{1}\S+\}{1}')
        fields = regex_fields.findall(self._raw_prompt)
        fields = [f[1:-1] for f in fields]  # Remove curley braces
        self.field_map = {k: None for k in fields}

    @abstractmethod
    def craft_prompt(self, data):
        pass


class QuestionAnswerPromptCrafter(PromptCrafter):
    def __init__(self, prompt_template_file):
        super().__init__(prompt_template_file)
    def craft_prompt(self, data):
        data = json.loads(data)
        justify = " and a justfy in a single sentence with minimum words possible but no more than 15."
        prompt = self._raw_prompt.format(
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
        if data['options'].get('show_reasoning', False):
            show_reasoning = 'Provide reason for the decision in a maximum 15 word long sentence.'
        else:
            show_reasoning = ''

        prompt = self._raw_prompt.format(
            query_text=query_text,
            categories = categories,
            multilabel = multilabel,
            show_reasoning = show_reasoning
        )

        return prompt


if __name__ == "__main__":
    path = Path(__file__).resolve().parent
    crafer = ClassifyPromptCrafter(path / 'prompt_templates/prompt1.txt')
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