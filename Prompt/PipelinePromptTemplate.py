from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.pipeline import PipelinePromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")



llm = OpenAI(temperature=0.3, api_key=api_key,max_tokens=50)

full_template = '''
{expect}
{example}
{question}
'''
full_prompt = PromptTemplate(template=full_template)


expect_template = '''
請根據我給的例子，學習，並判斷出我舉出的提問。
提問：陽光明媚嗎？
'''
expect_prompt = PromptTemplate(template=expect_template)

example_template = '''
回覆：多雲轉晴
意義：女朋友心情變好了

回覆：晴轉多雲
意義：女朋友心情開始糟糕

回覆：烏雲密佈
意義：女朋友心情暴躁
'''
example_prompt = PromptTemplate(template=example_template)

question_template = '''
回覆：{input}
意義：
'''
question_prompt = PromptTemplate(template=question_template)

input_prompts =[
    ('expect', expect_prompt),
    ('example', example_prompt),
    ('question', question_prompt)
]

pipeline_prompt = PipelinePromptTemplate(
    final_prompt=full_prompt,
    pipeline_prompts=input_prompts
)

print(pipeline_prompt.format(input="陰雨綿綿"))
print(llm.invoke(pipeline_prompt.format(input="陰雨綿綿")))