from langchain.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate
)
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

examples = [
    {'input': '2+2', 'output': '4'},
    {'input': '8+2', 'output': '10'}
]

example_prompt = ChatPromptTemplate.from_messages(
    [
        ('human', '{input}'),
        ('ai', '{output}')
    ]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
    input_variables=['input']
)

full_prompt = ChatPromptTemplate.from_messages(
    messages=[
        few_shot_prompt,  # few-shot examples
        ("human", "{input}")  # 最後要問的問題
    ]
)

prompt_value = full_prompt.format_messages(input="3+9")

llm = ChatOpenAI(temperature=0.3, api_key=api_key,max_completion_tokens=50)

print(llm.invoke(prompt_value).content)