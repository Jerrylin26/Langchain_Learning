import openai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=api_key)
response = client.completions.create(
    model='gpt-3.5-turbo-instruct',
    prompt='這樣要花多少錢',
    max_tokens= 50
)

print(response)
print(response.choices[0].text)