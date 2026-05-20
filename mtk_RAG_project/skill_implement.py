from langchain.agents.middleware import AgentMiddleware
from langgraph.graph import MessagesState
from typing import Annotated, List
from langgraph.types import Command
from langchain_core.messages import ToolMessage,HumanMessage
from langchain.agents.middleware.types import ModelRequest
from langchain_core.tools import tool,BaseTool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import InjectedToolCallId
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


class LoggingMiddleware(AgentMiddleware):

    def __init__(self,name = "Logger"):
        super().__init__()
        self.name = name
        self.call_count = 0 # 檢查

    def wrap_model_call(self, request, handler):
        self.call_count +=1

        # 1.調用前
        print(f"\n{'='*60}")
        print(f"[{self.name}] 第 {self.call_count} 次調用模型")
        print(f"{'='*60}")
        
        # 印出工具訊息
        if hasattr(request, 'tools') and request.tools:
            tool_names = [t.name for t in request.tools]
            print(f"可用工具 ({len(tool_names)}個):{tool_names}")

        # 印出狀態訊息
        if hasattr(request, 'state') and request.state:
            print(f"當前狀態: {request.state}")

        # 2.調用下一個處理器
        response = handler(request)

        # 3.調用後:可以處理響應
        print("模型調用完成")
        print(f"{'='*60}")

        return response
    


'''
*
*定義工具與狀態 schema (當前加載哪個skill)
*
'''

# 第一種模式: 替換模式 (用新的列表替換舊的)
# def skill_list_reducer(current: List[str], new: List[str]) -> List[str]:
#     return new 

# # 使用MessagesState 作為基類
# class SkillState(MessagesState):
#     skills_loaded: Annotated[List[str],skill_list_reducer] = []
    

# 第二種模式: 累積模式
def skill_list_accumulator(current: List[str], new: List[str]) -> List[str]:

    if not current:
        return new
    
    combined = current + [s for s in new if s not in current]
    return combined

# 使用MessagesState 作為基類
class SkillState(MessagesState):
    skills_loaded: Annotated[List[str],skill_list_accumulator] = []



'''
*
*定義外部工具
*
* loader:始終可見的工具，用於加載tool
* A_loader: 加載A的部分
* B_loader: 加載B的部分

'''


"""
* loader: skill_data_analysis、skill_tesxt_processing
"""
@tool
def skill_data_analysis(tool_call_id: Annotated[str, InjectedToolCallId]) -> Command:
    """加載數據分析技能"""

    instructions = """
    數據分析技能已成功加載!
    現在你可以使用以下工具:
    * calculate_statistics(numbers): 計算統計數據
    * B tool
    請繼續使用這些工具完成數據分析任務。
    """

    # for langgraph
    return Command(
        update={
            "messages": [
                ToolMessage(
                    content=instructions,
                    tool_call_id=tool_call_id
                )
            ],
            "skills_loaded": ["data_analysis"]
        }
    )


@tool
def skill_text_processing(tool_call_id: Annotated[str, InjectedToolCallId]) -> Command:
    """
    加載文本處理技能。
    調用此工具後，你將獲得以下文本處理相關的工具:
    - summarize_text: 生成文本摘要

    使用場景: 當用戶需要處理文本、生成摘要時，
    請先調用此工具加載文本處理技能。
    """

    instructions = """
    文本處理技能已成功加載!
    現在你可以使用以下工具:
    * summarize_text(text,max_length): 生成文本摘要
    * B tool
    請繼續使用這些工具完成文本處理任務。
    """

    # for langgraph
    return Command(
        update={
            "messages": [
                ToolMessage(
                    content=instructions,
                    tool_call_id=tool_call_id
                )
            ],
            "skills_loaded": ["text_processing"]
        }
    )


"""
* data_analysis tools
"""

@tool
def calculate_statistics(numbers: list[float]) -> dict:
    """計算一組數字的統計訊息，包括平均值、最大值、最小值、標準差等"""
    import statistics

    if not numbers:
        return "錯誤，列表為空"

    result ={
        "count": len(numbers),
        "sum": sum(numbers),
        "mean": statistics.mean(numbers),
        "median": statistics.median(numbers),
        "min": min(numbers),
        "max": max(numbers)
    }

    if len(numbers) > 1:
        result["stdev"] = statistics.stdev(numbers)
    
    return f"統計結果: {result}"


"""
* text_processing tools
"""

@tool
def summarize_text(text:str, max_length:int=100) -> str:
    """
    生成文本摘要。

    Args:
        text: 要摘要的文本
        max_length: 摘要最大長度
    """
    if len(text) <= max_length:
        return f"摘要: {text}"
    return f"摘要: {text[:max_length]}..."


"""
* 組織工具
"""
LOADER_TOOLS = [skill_data_analysis, skill_text_processing]
DATA_ANALYSIS_TOOLS = [calculate_statistics]
TEXT_PROCESSING_TOOLS = [summarize_text]
ALL_TOOLS = LOADER_TOOLS + DATA_ANALYSIS_TOOLS + TEXT_PROCESSING_TOOLS

print("工具定義完成")
print(f" Loader工具 ({len(LOADER_TOOLS)}): {[t.name for t in LOADER_TOOLS]}")
print(f" 數據分析工具 ({len(DATA_ANALYSIS_TOOLS)}): {[t.name for t in DATA_ANALYSIS_TOOLS]}")
print(f" 文本處理工具 ({len(TEXT_PROCESSING_TOOLS)}): {[t.name for t in TEXT_PROCESSING_TOOLS]}")
print(f" 總計: {len(ALL_TOOLS)}個工具")


# 舊式寫法
# @tool
# def skill_data_analysis(runtime) -> Command:

#     instructions = """數據分析技能已成功加載!
#     現在你可以使用以下工具:
#     * calculate_statistics(numbers): 計算一組數字的統計訊息
#     * B tool
#     請繼續使用這些工具完成用戶的數據分析任務。"""

#     return Command(
#         update={
#             "messages":[ToolMessage(
#                 content=instructions,
#                 tool_call_id=runtime.tool_call_id
#             )],
#             "skills_loaded": ["data_analysis"]
#         }
#     )



"""
*
* 定義工具映射
*
"""
# Skill mapping loaders
SKILL_TOOL_MAPPING = {
    "data_analysis": DATA_ANALYSIS_TOOLS,
    "text_processing": TEXT_PROCESSING_TOOLS
}

def get_tools_for_skills(skills_loaded: List[str]) -> List[BaseTool]:
    
    # 原始 tools list
    tools = list(LOADER_TOOLS)

    # 添加其餘 tools
    for skill_name in skills_loaded:
        if skill_name in SKILL_TOOL_MAPPING:
            tools.extend(SKILL_TOOL_MAPPING[skill_name])
    
    return tools

# 測試工具函數
print("測試 get_tools_for_skills 函數")
print(f"\n1. skills_loaded = []")
tools = get_tools_for_skills([])
print(f"    返回 {len(tools)} 個工具: {[t.name for t in tools]}")

print(f"\n2. skills_loaded = ['data_analysis']")
tools = get_tools_for_skills(['data_analysis'])
print(f"    返回 {len(tools)} 個工具: {[t.name for t in tools]}")

print(f"\n3. skills_loaded = ['data_analysis','text_processing']")
tools = get_tools_for_skills(['data_analysis','text_processing'])
print(f"    返回 {len(tools)} 個工具: {[t.name for t in tools]}")


"""
*
* 實現 SkillMiddleware
*
workflow:
    1. 攔截請求
    2. 從 request.state 讀取 skills_loaded
    3. 調用 get_tools_for_skills() 獲取過濾後的工具
    4. 使用 request.override(tools=filtered_tools) 創建新請求
    5. 調用 handler(filtered_request) 傳遞給模型
    6. 返回響應
"""

class SkillMiddleware(AgentMiddleware):
    """
    實現動態工具過濾
    為claude skills 核心組件

    1. 攔截請求
    2. 從 request.state 讀取 skills_loaded
    3. 調用 get_tools_for_skills() 獲取過濾後的工具
    4. 使用 request.override(tools=filtered_tools) 創建新請求
    5. 調用 handler(filtered_request) 傳遞給模型

    每次，模型在調用時，只會看到相關工具
    """

    def __init__(self, verbose: bool =True):
        super().__init__()
        self.verbose = verbose
        self.call_count = 0

    def __get_skills_from_state(self, request: ModelRequest) -> List[str]:

        """
        從請求狀態中提取 skills_loaded
        """

        skills_loaded = []

        if hasattr(request, "state") and request.state is not None:
            if isinstance(request.state, dict):
                skills_loaded = request.state.get("skills_loaded",[]) #自訂義的
            else:
                skills_loaded = getattr(request.state, "skills_loaded",[])
        
        return skills_loaded
    

    def wrap_model_call(self, request, handler):
        
        """
        攔截模型調用，動態過濾工具，
        整個 claude skills 最關鍵方法 
        """
        
        self.call_count +=1

        # 1. 從狀態中獲取已加載的 skills
        skills_loaded = self.__get_skills_from_state(request)

        # 2. 獲取過濾後工具
        filtered_tools = get_tools_for_skills(skills_loaded)

        # 3. 印出日誌
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"[SkillMiddleware]  第 {self.call_count} 次調用模型")
            print(f"{'='*60}")
            print(f"skills_loaded: {skills_loaded}")
            print(f"過濾後工具{len(filtered_tools)} 個: {[t.name for t in filtered_tools]}")
            
            # 對比原始工具數量
            if hasattr(request, 'tools') and request.tools:
                original_count = len(request.tools)
                print(f"工具數量變化: {original_count} -> {len(filtered_tools)}")

        # 替換工具
        # 創建新的 ModelRequest，其中 tools 被替換為過濾後的列表
        filtered_request = request.override(tools=filtered_tools)

        if self.verbose:
            print(f"已將過濾後工具傳遞給模型")
            print(f"{'='*60}\n")

        return handler(filtered_request)

    async def awrap_model_call(self, request, handler):
        
        """
        攔截模型調用，動態過濾工具，
        整個 claude skills 最關鍵方法 
        """
        
        self.call_count +=1

        # 1. 從狀態中獲取已加載的 skills
        skills_loaded = self.__get_skills_from_state(request)

        # 2. 獲取過濾後工具
        filtered_tools = get_tools_for_skills(skills_loaded)

        # 3. 印出日誌
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"[SkillMiddleware] (async) 第 {self.call_count} 次調用模型")
            print(f"{'='*60}")
            print(f"skills_loaded: {skills_loaded}")
            print(f"過濾後工具{len(filtered_tools)} 個: {[t.name for t in filtered_tools]}")
            
            # 對比原始工具數量
            if hasattr(request, 'tools') and request.tools:
                original_count = len(request.tools)
                print(f"工具數量變化: {original_count} -> {len(filtered_tools)}")

        # 替換工具
        # 創建新的 ModelRequest，其中 tools 被替換為過濾後的列表
        filtered_request = request.override(tools=filtered_tools)

        if self.verbose:
            print(f"已將過濾後工具傳遞給模型")
            print(f"{'='*60}\n")

        return await handler(filtered_request)
    
print(f"SkillMiddleware 類已定義")
print("\n關鍵方法說明;")
print("* wrap_model_call() : 同步攔截模型調用")
print("* awrap_model_call() : 異步攔截模型調用")
print("* .request.override() : 創建修改後請求對象")



# 創建 SkillMiddleware
skill_middleware = SkillMiddleware(verbose=True)

# 定義System prompt
SYSTEM_PROMPT = """
你是一名智能助手，可以使用各種技能來幫助用戶完成任務。

## 工作方式

1. 你有兩類工具:
    - **Skill Loader** (技能加載氣): 用於加載特定技能，名稱以 skill_ 開頭
    - **功能工具**: 執行具體任務的工具

2. 當用戶請求某個功能時:
    - 首先檢查是否有對應的功能工具
    - 如果沒有，調用相應的 SKill Loader 加載技能
    - 加載後，使用新獲得的工具完成任務

3. 可用的 Skill Loaders:
    - skill_data_analysis: 加載數據分析相關工具
    - skill_text_processing: 加載文本處理相關工具

請根據用戶的需求，靈活使用工具完成任務。
"""

print("準備創建 Agent...")
print(f"模型: OPENAI MODEL")
print(f"工具數量: {(ALL_TOOLS)}")
print(f"中間件: SkillMiddleware")




try:

    # 創建 model
    llm = ChatOpenAI(
        api_key = api_key,
        model = 'gpt-4.1'
        )
    
    # 創建 Agent
    agent = create_agent(
        model= llm,
        tools= ALL_TOOLS,
        middleware=(skill_middleware,),
        state_schema=SkillState,
        system_prompt=SYSTEM_PROMPT
    )

    print("\nAgent 創建成功!")
    print("\n關鍵配置:")
    print(f"-註冊工具總數: {len(ALL_TOOLS)}")
    print(f"-初始可見工具: {len(LOADER_TOOLS)} (僅 Loaders)")
    print(f"-Middleware: SkillMiddleware (動態過濾)")

except TypeError as e:
    print(f"創建時遇到參數問題: {e}")
    print("嘗試簡化版本")
    agent = create_agent(
        model=llm,
        tools=ALL_TOOLS,
        middleware=(skill_middleware,),
    )
    print('Agent 創建成功 (簡化版本)')




# 測試
print("="*60)
print("測試場景 1:初始狀態 - 簡單問候")
print("="*60)
print("\n預期行為")
print("-skills_loaded: [] (空)")
print("-可見工具: 2個 (僅 Loaders)")
print("\n" + "="*60)

test_input = {
    "messages": [HumanMessage(content="你好，請告訴我現在可以使用哪些工具")],
    "skills_loaded": []
}

# 調用 Agent
result = agent.invoke(test_input)

print("="*60)
print("\nAI 響應:")
for msg in result.get("messages",[]):
    if msg.__class__.__name__ == "AIMessage" and msg.content:
        print(msg.content)


# 測試2
print("="*60)
print("測試場景 2:動態加載數據分析技能")
print("="*60)
print("\n預期行為")
print("1. 第一次調用: skills_loaded: [] -> 2個工具")
print("2. AI調用: skill_data_analysis: 加載數據分析技能")
print("3. 第二次調用: skills_loaded: ['data_analysis'] -> 4個工具")
print("4. AI使用: calculate_statistics 完成任務")
print("-可見工具: 2個 (僅 Loaders)")
print("\n" + "="*60)

# 重置 Middleware 計數
skill_middleware.call_count = 0

test_input = {
    "messages": [HumanMessage(content="我有一組銷售數據 [150,36,48,99,789,12]，請幫我計算統計訊息")],
    "skills_loaded": []
}

# 調用 Agent
result = agent.invoke(test_input)

print("="*60)

print(f"skills_loaded: {result.get('skills_loaded',[])}")
print("\nAI 響應:")
for msg in result.get("messages",[]):
    if msg.__class__.__name__ == "AIMessage" and msg.content:
        print(msg.content)



# 測試3
print("="*60)
print("測試場景 3:多技能組合")
print("="*60)
print("\n預期行為")
print("加載多個技能")
print("工具數量逐步增加")
print("\n" + "="*60)

# 重置 Middleware 計數
skill_middleware.call_count = 0

test_input = {
    "messages": [HumanMessage(
        content="""請幫我完成以下任務:
        1. 我有一組銷售數據 [150,36,48,99,789,1254,-78]，請幫我計算統計訊息
        2. 從文本進行摘要: "解析度大提升：在 Switch 1 的掌機模式下，《海賊無雙4》的解析度常常在 540p 左右徘徊，甚至會動態降到更低，畫面看起來總是有些模糊。但在 Switch 2 上，解析度明顯更穩定。當你在掌機模式下，看到魯夫和索隆的招式特效清晰銳利地呈現，那種感覺真的非常棒。
畫面更流暢：過去，在 Switch 1 的 TV 模式下，雖然能跑到 60fps，但只要戰況激烈，幀數就會明顯下降。Switch 2 強大的硬體讓遊戲能更穩定地維持在接近 60fps 的高幀數，無論是面對成千上萬的小兵，還是施放華麗的終極技，遊戲過程都順暢無比，沒有那種頓挫感，打擊感也因此大幅提升。
https://vocus.cc/article/689d7c8cfd89780001f48d57
        """
        )],
    "skills_loaded": []
}

# 調用 Agent
result = agent.invoke(test_input)

print("="*60)

print(f"skills_loaded: {result.get('skills_loaded',[])}")
print("\nAI 響應:")
for msg in result.get("messages",[]):
    if msg.__class__.__name__ == "AIMessage" and msg.content:
        print(msg.content)