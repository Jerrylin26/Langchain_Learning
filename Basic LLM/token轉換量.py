import tiktoken

encoding = tiktoken.encoding_for_model('gpt-4')

num_token = len(encoding.encode("', every step a testament to perseverance. Baseball, he'"))
print(num_token)

