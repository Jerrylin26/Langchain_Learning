import tiktoken

encoding = tiktoken.encoding_for_model('gpt-4')

num_token = len(encoding.encode("hello i'm jerry how are you"))
print(num_token)
