from langchain.prompts import NGramOverlapExampleSelector
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

examples = [
    {'input': 'green apple', 'output':'綠綠的'},
    {'input': 'i ate green apple', 'output':'好吃好吃'},
    {'input': 'green orange', 'output':'怪怪的'},
    {'input': 'red banana', 'output':'哈哈的'},
    {'input': 'i love trump', 'output':'騙你的'},
]

example_prompt = PromptTemplate.from_template(
    'Input: {input}\nOutput: {output}'
)

example_selector = NGramOverlapExampleSelector(
    examples=examples,
    example_prompt=example_prompt,
    threshold=-1
)

prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    prefix='Please learn examples and answer questions: ',
    example_prompt=example_prompt,
    suffix='Input: {input}\nOutput:',
    input_variables=['input']
)

# threshold 來決定相似度
for threshold in [-0.1, 0.01, 0.1, 0.3, 1.0]:
    print(f"\n======= threshold: {threshold} ============")
    example_selector.threshold = threshold
    print(prompt.format(input='yesterday, i ate green apple'))

print('-----------------------------')

example_selector.threshold = 0.01
llm = OpenAI(temperature=0.3, api_key=api_key,max_tokens=50)
print('🎖️', llm.invoke(prompt.format(input='yesterday, i ate green apple')))
print('🎖️', llm.invoke(prompt.format(input='i trump the trump')))