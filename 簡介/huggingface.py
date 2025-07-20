from langchain_openai import OpenAI,ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
huggingface_api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")

'''
# 使用託管在HuggingFaceHub的model
llm = HuggingFaceEndpoint(
    repo_id="jondurbin/airoboros-l2-13b-gpt4-2.0",
    max_new_tokens=128,
    temperature=0.5,
    huggingfacehub_api_token=huggingface_api_key,
    #provider="together",  # set your provider here hf.co/settings/inference-providers
    # provider="hyperbolic",
    provider="featherless-ai",
    # provider="together",
)
question = "Who won the FIFA World Cup in the year 1994? "
print(llm.invoke(question))
'''

# 下載到本地
from langchain_huggingface import HuggingFacePipeline
llm = HuggingFacePipeline.from_model_id(
    model_id="gpt2",
    task="text-generation",
    pipeline_kwargs={"max_new_tokens": 10},
)

print(llm.invoke('你是誰'))