import requests
import json
from typing import List, Optional

from dagster import ConfigurableResource

from src.prompts import SUMMARY_PROMPT_TEMPLATE


class LlamaResource(ConfigurableResource):
    endpoint: Optional[str]

    def _predict(self, prompt: str, stop: List[str], max_tokens: int):
        data = {"prompt": prompt, "stop": stop, "max_tokens": max_tokens}
        if not self.endpoint:
            raise ValueError("You haven't specified an endpoint for your llama.cpp server")
        response = requests.post(self.endpoint, headers={"Content-Type": "application/json"}, data=json.dumps(data))
        return response.json()["choices"][0]["text"]

    def summarise(self, text):
        summary = self._predict(prompt=SUMMARY_PROMPT_TEMPLATE.format(text=text), stop=["\n"], max_tokens=500)
        return summary
