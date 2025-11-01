from abc import ABC, abstractmethod
from openai import OpenAI
from config import settings
from typing import Dict, Any, Optional
import json


class BaseAgent(ABC):
    """Base class for all agents in the pipeline."""

    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.temperature = settings.openai_temperature
        self.max_tokens = settings.max_tokens

    def call_gpt(
        self,
        user_prompt: str,
        response_format: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> str:
        """Call GPT-4 with the given prompt."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": response_format} if response_format else None
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"Error calling GPT-4 in {self.name}: {str(e)}")

    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return output. Must be implemented by subclasses."""
        pass

    def log(self, message: str):
        """Log agent activity."""
        print(f"[{self.name}] {message}")
