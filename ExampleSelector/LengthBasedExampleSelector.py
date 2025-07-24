from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector

example_prompt = PromptTemplate.from_template(
    'Input: {input}\nOutput: {output}'
)

examples = [
    {'input': 'happy', 'output': 'sad'},
    {'input': 'tall', 'output': 'short'},
    {'input': 'hot', 'output': 'cold'},
    {'input': 'fast', 'output': 'slow'},
    {'input': 'rich', 'output': 'poor'},
]

example_selector = LengthBasedExampleSelector(
    example_prompt=example_prompt,
    examples=examples,
    max_length=16,
)

prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    prefix='Please learn examples and answer questions: ',
    example_prompt=example_prompt,
    suffix='Input: {input}\nOutput:',
    input_variables=['input']
)

print(prompt.format(input='open'))
