from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.prompts import FewShotPromptTemplate, PromptTemplate

examples = [
    {'input': 'happy', 'output': 'sad'},
    {'input': 'tall', 'output': 'short'},
    {'input': 'hot', 'output': 'cold'},
    {'input': 'fast', 'output': 'slow'},
    {'input': 'rich', 'output': 'poor'},
]

# ChromaDB 快速測試向量資料庫
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples=examples,
    embeddings=OpenAIEmbeddings(),
    vectorstore_cls= Chroma,
    k=2
)

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

print(prompt.format(input='sunny'))