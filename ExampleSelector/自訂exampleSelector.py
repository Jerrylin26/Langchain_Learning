import random
from typing import Dict, List
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.prompts.example_selector.base import BaseExampleSelector

class RandomExampleSelector(BaseExampleSelector):
    def __init__(self, examples, count=2):
        self.examples = examples
        self.count = count
    
    def add_example(self, example: dict[str, str]) :
        self.examples.append(example)
        
    
    def select_examples(self, input_variables: dict[str, str]) -> list[dict]:
        return random.sample(self.examples, self.count)
    
    def show(self):
        print('🌺', self.examples)

examples = [
    {'input': 'happy', 'output': 'sad'},
    {'input': 'tall', 'output': 'short'},
    {'input': 'hot', 'output': 'cold'},
    {'input': 'fast', 'output': 'slow'},
    {'input': 'rich', 'output': 'poor'},
]

example_selector = RandomExampleSelector(examples,2)
example_selector.show()

example_prompt = PromptTemplate.from_template(
    'Input: {input}\nOutput: {output}'
)

prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    prefix='Please learn examples and answer questions: ',
    example_prompt=example_prompt,
    suffix='Input: {input}\nOutput:',
    input_variables=['input']
)

print(prompt.format(input='rainy'))
