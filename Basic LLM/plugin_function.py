import openai
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

tools = [
    {
        "type": "function",
        "function": {
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
            }
        }
    }
]


def get_city_temperature(city_name):
    if city_name == '台灣':
        return '20 度'
    else:
        return '30 度'


query = "今天杭州幾度"
client = openai.OpenAI(api_key=api_key)
response = client.chat.completions.create(
    model='gpt-4.1-nano-2025-04-14',
    messages=[
        {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': query},
            ]
        }
    ],
    max_tokens= 50,
    tools =  tools,
    tool_choice= 'auto'
)

tool_calls = response.choices[0].message.tool_calls
response_assistant = response.choices[0].message
'''
ChatCompletionMessage(
    content=None, 
    refusal=None, 
    role='assistant', 
    annotations=[], 
    audio=None, 
    function_call=None, 
    tool_calls=[ChatCompletionMessageToolCall(id='call_URCf8fezbdkUKhNKKnz07Dzx', 
                                              function=Function(arguments='{"city_name": "杭州"}', name='get_city_temperature'), 
                                              type='function')])
'''
city_name = json.loads(response.choices[0].message.tool_calls[0].function.arguments)["city_name"]

final_response = client.chat.completions.create(
    model='gpt-4.1-nano-2025-04-14',
    messages=[
        {'role': 'user', 'content': query}, # 原始提問
        response_assistant, # 模型提出的 tool_call
        {
            "role": "tool",
            "tool_call_id": tool_calls[0].id, # 對應剛才模型提出的那個 call id
            "content": get_city_temperature(city_name) # 工具回傳的實際結果
        } 
    ]
)
print(response.choices[0].message)
print(final_response.choices[0].message.content)





