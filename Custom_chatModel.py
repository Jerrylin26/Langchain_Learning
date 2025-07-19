from typing import Any, Dict, Iterator, List, Optional, ClassVar
import openai
from langchain_core.language_models import BaseChatModel
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ChatMessage
)
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


class MyChatOpenAI(BaseChatModel):

    model_name: ClassVar[str] = "gpt-4.1-nano-2025-04-14"
    max_tokens: ClassVar[int] = 300
    temperature: ClassVar[float] = 0.4

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model."""
        return "MyChatOpenAI"

    @property
    def _identifying_params(self) -> Dict[str, Any]:

        return {

            "model_name": self.model_name,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        message_dicts = [self._convert_message_to_dict(m) for m in messages]

        client = openai.OpenAI(
            api_key= api_key
        )
        response = client.chat.completions.create(
            model = self.model_name,
            messages= message_dicts,
            max_tokens= self.max_tokens,
            temperature= self.temperature,
            stop = stop
        )
        print("gernerating-----------------")
        return self._create_chat_result(response)

    def _create_chat_result(self, response) -> ChatResult:
        generations = []

        for res in response.choices:
            message: BaseMessage = self._convert_dict_to_message(res.message) # type (BaseMessage)
            gen = ChatGeneration(
                generation_info = dict(finish_reason=res.finish_reason),
                message=message
            )
            generations.append(gen)
        
        token_usage = response.usage
        llm_output = {'token_usage': token_usage, 'model_name':self.model_name}
        print(generations)
        return ChatResult(generations=generations, llm_output=llm_output)
    
    @staticmethod
    def _convert_dict_to_message(message) -> BaseMessage:
        role = message.role

        if role == 'user':
            return HumanMessage(content=message.content)
        elif role == 'assistant':
            return AIMessage(content=message.content)
        elif role == 'system':
            return SystemMessage(content=message.content)
        else:
            return ChatMessage(content=message.content, role=role)

    @staticmethod
    def _convert_message_to_dict(message) -> dict:
        content = message.content
        if isinstance(message, HumanMessage):
            message_dict = {'role':'user','content':content}
        elif isinstance(message, AIMessage):
            message_dict = {'role':'assistant','content':content}
        elif isinstance(message, SystemMessage):
            message_dict = {'role':'system','content':content}
        elif isinstance(message, ChatMessage):
            message_dict = {'role':message.role,'content':content}
        else:
            raise TypeError(f'Got unknown type {message}')
        
        return message_dict
    
MyChatopenai = MyChatOpenAI()
response = MyChatopenai.invoke([HumanMessage(content='我是誰')])
print("dict: ", MyChatopenai.dict())
print("type(response): ", type(response))

