from langchain_community.document_loaders import JSONLoader


# jq語法
loader = JSONLoader(
    '/home/jerry/code/Langchain_大型ReAct/Langchain_ReAct書/Prompt/load_prompt/fewshotPrompt.json',
    jq_schema = '.prefix'
)

for x in loader.load():
    print(x)


# 處理 metadata
def metadata_func(my_json, metadata):
    metadata['try_metadata_func'] = my_json['_type']
    metadata['test_metadata_func'] = my_json['input_variables']
    return metadata


loader = JSONLoader(
    '/home/jerry/code/Langchain_大型ReAct/Langchain_ReAct書/Prompt/load_prompt/fewshotPrompt.json',
    jq_schema = '.',
    metadata_func=metadata_func,
    text_content=False # 有非字串要False
)

for x in loader.load():
    print(x)
