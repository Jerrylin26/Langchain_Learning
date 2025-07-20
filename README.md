# 📘 目錄總覽：LangChain / OpenAI 應用範例整理

## 📦 基本 LLM 與 Chat 模型操作
- `3-1.py`：LLM 呼叫範例（OpenAI）
- `3-2.py`：Chat 類型模型使用
- `文字補全.py`：使用 OpenAI 原生 API（text-completion）
- `對話補全.py`：使用 OpenAI 原生 API（chat-completion）

## 🧠 Token 管理與控制
- `token轉換量.py`：使用 `tiktoken` 進行 token 長度估算

## 🔌 插件與函式呼叫
- `plugin function.py`：OpenAI function-calling 應用
- `plugin_function_langchain.py`：LangChain 中使用工具（Tools/Function）

## 🛠 自訂模型（進階應用）
- `Custom_LLM.py`：自訂 LLM 模型（基於 OpenAI SDK）
- `Custom_chatModel.py`：自訂 Chat Model（基於 OpenAI SDK）

## ⚡ 快取策略與加速技巧
- `4種快取.py`：基礎快取方式總覽
- `Custom_cache.py`：使用 Python dictionary 自訂快取
- `SQL自訂表格_cache.py`：SQL 快取（使用 `.create` 建表）
- `cache_args.py`：透過 `cache=False` 控制快取行為
- `semantic_cache.py`：語意快取（相似度匹配）
- `GPTCache.py`：使用 GPTCache 進行高級快取（支援精確 & 相似匹配）

## 🌊 串流與非同步
- `streaming.py`：兩種串流方式（print 時即時回傳）
- `async_llm.py`：非同步呼叫 LLM（`async` 效能極佳）

## 🔧 模型設定與序列化
- `模型配置序列化.py`：將模型設定保存為 `.json`，便於場景切換

## 🤗 HuggingFace 模型支援
- `huggingface.py`：整合 HuggingFace 模型（略複雜）

## 🧩 Prompt 設計模組
- `promptTemplate.py`：基礎 `PromptTemplate` 模板
- `PartialPromptTemplate.py`：支援動態變數預填的模板
- `PipelinePromptTemplate.py`：串接多個 Prompt（*已棄用*）
- `FewShotPromptTemplate.py`：few-shot 指引式輸入，複雜情境下的範例教學模板
- `StringPromptTemplate.py`:自訂prompt 