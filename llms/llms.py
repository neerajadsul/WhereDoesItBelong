from abc import ABC, abstractmethod, abstractstaticmethod


class ChatAssistant(ABC):
    """Abstract baseclass to support variety of LLMs."""
    @abstractmethod
    def get_completion(self, raw_prompt):
        """LLM API specific completion method.
        Args:
            raw_prompt: raw text template containing fields to replace.
        """
        pass

    @abstractmethod
    def get_message(self, response):
        """Return message only part from completion response.

        Args:
            response: full response from LLM API, typically in JSON format.
        """
        pass

    @abstractmethod
    def log_response(self, response):
        """Save entire response in the datastore including traceability info 
        and message for dissimination later.

        Args:
            response: full response from LLM API, typically in JSON format.
        """
        pass