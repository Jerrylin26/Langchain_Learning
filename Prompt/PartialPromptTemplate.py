from langchain.prompts import PromptTemplate
from datetime import datetime

# 使用字串partial填充
prompt_tpl = PromptTemplate.from_template(
    '請給我講{num}個關於{type}的笑話,'
    '並且不要出現{location1}和{location2}'
)

partial_prompt1 = prompt_tpl.partial(num='3')
partial_prompt2 = partial_prompt1.partial(
    location1='辦公室',
    location2 = '學校'
)
print(partial_prompt2.format(type='程式設計師'))

# 使用字串Callable[]傳回字串partial填充
prompt_tpl = PromptTemplate.from_template(
    '你是一位優秀的{role}運動員,你清楚知道現在時間為{date}'

)

def get_date():
    return datetime.now().strftime("%H:%M:%S")

partial_prompt1 = prompt_tpl.partial(date=get_date)
print(partial_prompt1.format(role='排球'))


# format後才有partial
prompt_tpl = PromptTemplate.from_template(
    '你是一位優秀的{role}運動員,你清楚知道現在時間為{date}',
    partial_variables={'date':get_date}

)

def get_date():
    return datetime.now().strftime("%H:%M:%S")

print(partial_prompt1.format(role='排球'))