import types
import random
from langchain_core.utils import formatter
from langchain.prompts.base import StringPromptTemplate


class FunctionPromptTemplate(StringPromptTemplate):
    template :str

    def format(self, **kwargs) -> str:
        kwargs = self._merge_partial_and_user_variables(**kwargs)
        for key, value in kwargs.items():
            if isinstance(value, types.FunctionType):
                kwargs[key] = value()
        
        return formatter.format(self.template, **kwargs)
    
    @property
    def _prompt_type(self) -> str:
        return 'function_prompt'
    
def get_num():
    return random.randint(1,10)

prompt = FunctionPromptTemplate(
    template='請給我{num}個笑話',
    input_variables=['num']
)

print(prompt.format(num=get_num))
print(prompt.dict())