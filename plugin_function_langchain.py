import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage
from langchain_core.messages import ToolMessage
from langchain.chat_models import init_chat_model

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


tools = [
    {
        "name": "get_city_temperature",
        "description": "透過城市名稱取得當前溫度", 
        "parameters": {
            "type": "object",
            "properties": {
                "city_name": {
                    "type": "string",
                    "description": "城市名稱"
                }
            },
            "required": ["city_name"]
        },    
    }
]

def get_city_temperature(city_name):
    if city_name == '台灣':
        return '20 度'
    else:
        return '30 度'


llm = init_chat_model(model="gpt-4.1-nano-2025-04-14", model_provider="openai")
llm_with_tools = llm.bind_tools(tools)

query = "今天杭州幾度"
message = [HumanMessage(query)]
tool_response = llm_with_tools.invoke(message)


#print(tool_response)
print(tool_response.tool_calls)  # 檢查是否呼叫 function

print('-----------------')


message.append(tool_response) #加入 AIMessage
print(message)
print('-----------------')

for tool_call in tool_response.tool_calls:
    selected_tool = {"get_city_temperature": get_city_temperature}[tool_call["name"].lower()]
    print("selected tool: ", selected_tool)
    # 此處為函式寫法
    tool_output = selected_tool(**tool_call["args"])

    message.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))
    
print(message)

final_response = llm_with_tools.invoke(message)
print('回覆： ', final_response.content)