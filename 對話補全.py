import openai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=api_key)
response = client.chat.completions.create(
    model='gpt-4.1-nano-2025-04-14',
    max_tokens=50,
    messages=[
        {
            'role': 'system',
            'content': [
                {'type': 'text', 'text': '你不是AI助理'},
                {'type': 'text', 'text': '你是位暢銷作家'}
            ]
        },
        {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': '你是誰'}
            ]
        }
    ]
)

print(response.model_dump())
print(response.choices[0].message.content) 

print('------- 查看 response.choices[0] -------')
print(response.choices[0])
