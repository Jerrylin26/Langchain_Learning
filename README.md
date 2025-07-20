# 📘 目錄總覽：LangChain / OpenAI 應用範例整理

## 📦 基本 LLM 與 Chat 模型操作
- `3-1.py`：LLM 呼叫範例（OpenAI）
- `3-2.py`：Chat 類型模型使用
- `文字補全`：使用 OpenAI 原生 API（text-completion）
- `對話補全`：使用 OpenAI 原生 API（chat-completion）

## 🧠 Token 管理與控制
- `token轉換量`：使用 `tiktoken` 進行 token 長度估算

## 🔌 插件與函式呼叫
- `plugin function`：OpenAI function-calling 應用
- `plugin_function_langchain`：LangChain 中使用工具（Tools/Function）

## 🛠 自訂模型（進階應用）
- `Custom_LLM`：自訂 LLM 模型（基於 OpenAI SDK）
- `Custom_chatModel`：自訂 Chat Model（基於 OpenAI SDK）

## ⚡ 快取策略與加速技巧
- `4種快取`：基礎快取方式總覽
- `Custom_cache`：使用 Python dictionary 自訂快取
- `SQL自訂表格_cache`：SQL 快取（使用 `.create` 建表）
- `cache_args`：透過 `cache=False` 控制快取行為
- `semantic_cache`：語意快取（相似度匹配）
- `GPTCache`：使用 GPTCache 進行高級快取（支援精確 & 相似匹配）

## 🌊 串流與非同步
- `streaming`：兩種串流方式（print 時即時回傳）
- `async_llm`：非同步呼叫 LLM（`async` 效能極佳）

## 🔧 模型設定與序列化
- `模型配置序列化`：將模型設定保存為 `.json`，便於場景切換

## 🤗 HuggingFace 模型支援
- `huggingface`：整合 HuggingFace 模型（略複雜）

## 🧩 Prompt 設計模組
- `promptTemplate`：基礎 `PromptTemplate` 模板
- `PartialPromptTemplate`：支援動態變數預填的模板
- `PipelinePromptTemplate`：串接多個 Prompt（*已棄用*）
- `FewShotPromptTemplate`：few-shot 指引式輸入，複雜情境下的範例教學模板
