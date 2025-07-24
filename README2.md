# 📘 目錄總覽：特定功能筆記

##  多種tools BaseTool&普通 Python 函式 寫法(plugin_function_langchain.py)
### 1. 繼承BaseModel使用 .invoke
class Add(BaseModel):
    """Add two integers together."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")


class Multiply(BaseModel):
    """Multiply two integers together."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")


tools = [Add, Multiply]
selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]

tool_output = selected_tool.invoke(tool_call["args"])

### 2. 使用函式用 函式帶入
[
    {'name': 'get_city_temperature', 
'args': {'city_name': '杭州'}, 
'id': 'call_frmE2NtvIAU1dPb7wdrpD04P', 
'type': 'tool_call'}
]

tool_map = {
    "get_city_temperature": get_city_temperature,
    "another_tool": another_function
}

### selected_tool = get_city_temperature
selected_tool = tool_map[tool_call["name"]] 
tool_output = selected_tool(**tool_call["args"])



### ChatMessage 
「HumanMessage、AIMessage、SystemMessage 都是有特定角色的 BaseMessage；
而 ChatMessage 是沒有限定角色、可以自由指定角色的 BaseMessage，代表其他所有角色的訊息。


### 4種快取 ## SQLite cache
result = cache.lookup(prompt, llm_string) 未解

### tsvector & pgvector (SQL自訂表格)
tsvector : 找出包含特定關鍵字的產品描述	
pgvector: 找出與某張圖片語意接近的圖片

### Union[Callable[[Any, str], None]] (GPTCache)
Union: 這個東西可以是多種型別中的任一種

這個 Callable 型別的意思是：

Callable：表示「可被呼叫的東西」——也就是「函式」。

[Any, str]：表示這個函式需要兩個參數：

第一個是 Any（可以是任何型別）

第二個是 str

None：表示這個函式的回傳型別是 None（也就是不回傳任何值，或回傳 None）

### 這裡的內部邏輯值得學習 (GPTCache)
set_llm_cache(GPTCache(init_gptcache))

### 相似匹配 openai版本問題 (GPTCache)

### PromptTemplate prompt轉型選擇
    - .format_messages() => 給ChatOpenAI
    - .format_prompt() => 中間產物
        - .to_messages() => 給ChatOpenAI
        - .to_string() => 給OpenAI




