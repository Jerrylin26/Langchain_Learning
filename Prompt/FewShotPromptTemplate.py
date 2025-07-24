from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


llm = OpenAI(temperature=0.3, api_key=api_key,max_tokens=50)
example_prompt = PromptTemplate.from_template(
    '回覆:{text}\n意義:{mood}'
)

examples = [
    {'text':'多雲轉晴', 'mood':'女朋友心情變好了'},
    {'text':'晴轉多雲', 'mood':'女朋友心情開始糟糕'},
    {'text':'烏雲密佈', 'mood':'女朋友心情暴躁'}
]

prompt = FewShotPromptTemplate(
    prefix = '''請根據我給的例子，學習，並判斷出我舉出的提問。
            提問：陽光明媚嗎？''',
    example_prompt = example_prompt,
    examples = examples,
    suffix = '\n回覆:{input}\n意義: ',
    input_variables=["input"]

)

print(prompt.format(input='陰雨綿綿'))

print(llm.invoke(prompt.format(input='陰雨綿綿')))