from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


chat = ChatOpenAI(
    model="gpt-4.1-nano-2025-04-14",
    max_tokens=50,
    api_key=api_key,
)


# __call__
print('-------------__call__-------------')
res = chat([
    HumanMessage(content="你是誰")
])
print(res)
print(type(res))

print('-------------invoke-------------')
res = chat.invoke("你是誰")
print(res)
print(type(res))


print('-------------predict_messages-------------')
res = chat.predict_messages([
    SystemMessage(content="你是剛出獄的作家，請用這個身份回答所有問題。"),
    HumanMessage(content="你是誰")
])
print(res)
print(type(res))

print('-------------generate-------------')
batch_messages = [[
    SystemMessage(content="你是剛出獄的作家，請用這個身份回答所有問題。"),
    HumanMessage(content="你是誰")
],[
    SystemMessage(content="你是剛出獄的醫生，請用這個身份回答所有問題。"),
    HumanMessage(content="你是誰")
]
]

res = chat.generate(batch_messages)
print(res)
print(res.llm_output)
print('------------')
print(res.model_dump())




