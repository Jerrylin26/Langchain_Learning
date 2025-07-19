from typing import Any, List, Mapping, Optional, ClassVar
import openai
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from dotenv import load_dotenv
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


class MyOpenAI(LLM):

    model_name: ClassVar[str] = "gpt-4.1-nano-2025-04-14"
    max_tokens: ClassVar[int] = 50
    temperature: ClassVar[float] = 0.8

    @property
    def _llm_type(self) -> str:
        return "My_Custom_OpenAI"
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {
            "model_name":self.model_name,
            "max_tokens":self.max_tokens,
            "temperature":self.temperature
        }

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        client = openai.OpenAI(
            api_key = api_key,
        )
        response = client.completions.create(
            model = self.model_name,
            max_tokens = self.max_tokens,
            prompt= prompt,
            temperature=self.temperature
        )


        return response.choices[0].text

myopenai = MyOpenAI()
print("dict function: ", myopenai.dict())
print("回覆： " , myopenai.invoke("排球好玩嗎"))
