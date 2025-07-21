from langchain.prompts import PromptTemplate
from langchain.prompts.loading import load_prompt

# to_json
prompt = PromptTemplate(
    template='告訴我NBA{num}隻球隊名稱',
    input_variables=['num']
)

prompt.save('prompt/load_prompt/prompt.json')


# load_prompt
prompt_load = load_prompt('prompt/load_prompt/prompt.json')
print("🧩load_prompt: ",prompt_load)

# load_prompt
## 使用template_path
prompt_load = load_prompt(
    'prompt/load_prompt/template_path.json')
print("🧩load_prompt template_path: ",prompt_load)


# FewShotPromptTemplate load_prompt
prompt_load = load_prompt(
    'prompt/load_prompt/fewshotPrompt.json')
print("🧩load_prompt FewShotPromptTemplate load_prompt: ",prompt_load)


