# 📘 目錄總覽：LangChain / OpenAI 應用範例整理

## basic LLM
### 📦 基本 LLM 與 Chat 模型操作
- `3-1.py`：LLM 呼叫範例（OpenAI）
- `3-2.py`：Chat 類型模型使用
- `文字補全.py`：使用 OpenAI 原生 API（text-completion）
- `對話補全.py`：使用 OpenAI 原生 API（chat-completion）

### 🧠 Token 管理與控制
- `token轉換量.py`：使用 `tiktoken` 進行 token 長度估算

### 🔌 插件與函式呼叫
- `plugin function.py`：OpenAI function-calling 應用
- `plugin_function_langchain.py`：LangChain 中使用工具（Tools/Function）

### 🛠 自訂模型（進階應用）
- `Custom_LLM.py`：自訂 LLM 模型（基於 OpenAI SDK）
- `Custom_chatModel.py`：自訂 Chat Model（基於 OpenAI SDK）

### 🌊 串流與非同步
- `streaming.py`：兩種串流方式（print 時即時回傳）
- `async_llm.py`：非同步呼叫 LLM（`async` 效能極佳）

### 🔧 模型設定與序列化
- `模型配置序列化.py`：將模型設定保存為 `.json`，便於場景切換

### 🤗 HuggingFace 模型支援
- `huggingface.py`：整合 HuggingFace 模型（略複雜）

## cache
### ⚡ 快取策略與加速技巧
- `4種快取.py`：基礎快取方式總覽
- `Custom_cache.py`：使用 Python dictionary 自訂快取
- `SQL自訂表格_cache.py`：SQL 快取（使用 `.create` 建表）
- `cache_args.py`：透過 `cache=False` 控制快取行為
- `semantic_cache.py`：語意快取（相似度匹配）
- `GPTCache.py`：使用 GPTCache 進行高級快取（支援精確 & 相似匹配）


## prompt
### 🧩 Prompt 設計模組
- `promptTemplate.py`：基礎 `PromptTemplate` 模板
- `PartialPromptTemplate.py`：支援動態變數預填的模板
- `PipelinePromptTemplate.py`：串接多個 Prompt（*已棄用*）
- `FewShotPromptTemplate.py`：few-shot 指引式輸入，複雜情境下的範例教學模板
- `StringPromptTemplate.py`:自訂 format()，可加任意邏輯
- `load_prompt.py`: 序列化 & 反序列化, 以及多種load_prompt方式
- `ChatPromptTemplate.py`: ChatOpenAI的promot
- `MessagesPlaceholder.py`: 保留了 list[BaseMessage],而非僅僅是str
- `FewShotChatMessagePromptTemplate.py`: few-shot 指引式輸入 ChatOpenAI


## exampleSelector
### 🗺️ ExampleSelector 範例選擇器
- `LengthBasedExampleSelector.py`: 控制example的token數
- `SemanticSimilarityExampleSelector.py`: 使用語義相似性
- `MaxMarginalRelevanceExampleSelector.py`: 找出「和輸入夠像，但彼此又不要太像」的examples
- `NGramOverlapExampleSelector.py`:  n-gram（字詞片段）重疊程度，來評估範例和輸入的相似度
- `自訂exampleSelector.py`: 底層操作 BaseExampleSelector

### 🧭 指南- 範例選擇器

| 任務需求         | 建議使用 |
|------------------|-----------|
| 語意精準度高     | `SemanticSelector` |
| 避免語意重複     | `MMR`              |
| 可解釋、輕量     | `NGramOverlap`     |

## outputParser
### 📟 outputParser 輸出解析器
- `CommaSeparatedListOutputParser.py`: 逗點分隔,最後成list
- `DatetimeOutputParser.py`: 最後成Datetime格式
- `EnumOutputParser.py`: 自訂enum
- `XMLOutputParser.py`: 輸出XML
- `StructuredOutputParser.py`: 輸出JSON
- `PydanticOutputParser.py`: 輸出pydantic BaseModel
- `OutputFixingParser.py`: 自行呼叫llm,修復.parse()錯誤 (格式修復)
- `RetryWithErrorOutputParser.py`: 更完整修復
- `CustomOutputParser.py`: 自訂解析器


## Data Connection
### 💾 Document Loader 文件載入器
#### 文字前置處理 1) 載入  2) 分割轉換
- `CSVLoader.py`: 載入.csv
- `DirectoryLoader.py`: 只遍歷目錄(Directory)、每個檔案叫一個 loader 處理
- `UnstructuredHTMLLoader.py`: 分段文字
- `JSONLoader.py`: 載入.json
- `MarkdownLoader.py`: 載入.md
- `WebBaseLoader.py`: 基本上是爬蟲,底層邏輯 (無js)
- `UnstructuredURLLoader.py`: 基本上也是爬蟲 ,高階 (無js)
- `SeleniumURLLoader.py`: 用 Selenium 開一個真實的無頭（headless）瀏覽器, 能夠(有js)
- `PlaywrightURLLoader.py`: 同 Selenium 聽說能快速的渲染動態網頁內容。
- `PyPDFLoader.py`: pdf提取
- `MathpixPDFLoader.py`: 數學公式轉文字
- `UnstructuredPDFLoader.py`: 針對「語意結構」進行解析 *不推薦,unstructured函式庫太大
- `PDFMinerPDFasHTMLLoader.py`:  轉成 HTML 格式的文本結構，保留字型、位置、段落結構等資訊
- `PyMuPDFLoader.py`: 速度快,適合圖文混排 PDF
- `PyPDFDirectoryLoader.py`: 適合批次處理 PDF 文件夾
- `AmazonTextractPDFLoader.py`: 使用 AWS Textract 來解析 PDF
- `自訂document_Loader.py`: 使用底層BaseLoader


### 🖨️ Document Transformer 文件轉換器
#### 文字分割
- `CharacterTextSplitter.py`: 基礎文字分割
- `RecursiveCharacterTextSplitter.py`: 建議使用, 切割成合理大小段落, [\n\n, \n, ' ', '']
- `TokenTextSplitter.py`: 按照token數區分
- `自訂Text Splitter.py`: 基礎模組

#### 文字中繼資料提取
- `DoctranPropertyExtractor.py`: 資料擷取分類 （目前doctran版本不符無法使用）(請直接使用Doctran提取)
- `DoctranTextTranslator.py`: 翻譯 （目前doctran版本不符無法使用）(請直接使用Doctran提取)
- `DoctranQATransformer.py`: 轉成問答格式,有利於提問後答案準確性 （目前doctran版本不符無法使用）(請直接使用Doctran提取)


### 🔰 Embedding & Vector Store 嵌入與向量資料庫
#### 嵌入
- `Embedding.py`: 嵌入, 找語意相近
- `Embedding_cache.py`: 加入cache
- `Chroma.py`: 能存入metadata的 DB (本地端) 佔大量記憶體
- `Chroma_docker.py`: (server端) 通常透過 Docker 運行，而且最好用 volume 映射到主機磁碟，以免資料丟失。
- `FAISS.py`: 高效相關性檢索DB, 與numpy合作

### 🔭 Retriever 檢索器
| 以chunk為搜尋單位       | Retriever |
- `Basic_retriever.py`: 模組化查詢助理
- `Multy_query_retriever.py`: 一句話,產生多種問法

#### 上下文壓縮檢索器
- `LLMChainExtractor.py`: 「壓縮器」 結果精確,成本下降 (用便宜模型壓縮 + 用貴模型回答)
- `LLMChainFilter.py`: 「過濾器」 全有全無 效果普普
- `EmbeddingsFilter.py`: 「餘弦相似度過濾器」 節省成本 控制相似度
- `DocumentCompressorPipeline.py`: 檢索文件 → 壓縮刪除不相關的部分（保證精準）, 有潛力的pipeline

#### 整合檢索器
- `EnsembleRetriever.py`: 設定權重以及多個檢索器,偏字面語意
- `ParentDocumentRetriever.py`: 檢索小片段 → 回傳大段落（保證上下文完整）避免丟失重要資訊
- `MultiVectorRetriever.py`: 同一份原始文件，對應多個不同的向量表示,『摘要向量』,metadata
- `MultiVectorRetriever2.py`: 『假設性問題』,對應各個區塊,具有代表性,非常有潛力
- `SelfQueryRetriever.py`: 讓 LLM 讀懂使用者的自然語言查詢，轉換成結構化檢索語句，再丟給向量庫
- `LongContextRecoder.py`: 研究發現LLM中,最重要的資訊應該放在最前面與後面,所以衍生出這項調整順序


## Chain
### ⛓️‍💥 Chain 鏈
- `LLMChain.py`: 基礎LLm功能
- `SimpleSequentialChain.py`: 單一輸入單一輸出, 前者輸出為後者輸入
- `SequentialChain.py`: 多個輸入多個輸出
- `RouterChain.py`: 根據問題,動態選擇 chain
- `EmbeddingRouterChain.py`: description為資料庫,invoke(input) 用embedding相似度選用問題
- `TransformChain.py`: 切分字串，甚至是簡化成要輸入的樣貌