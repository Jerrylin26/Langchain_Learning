from sqlalchemy import Column, Integer, String, Computed, Index, Sequence
from sqlalchemy import create_engine
from sqlalchemy_utils import TSVectorType
from langchain_community.cache import SQLAlchemyCache, Base
from langchain.globals import set_llm_cache


class FullLLMCache(Base):  # type: ignore[misc,valid-type]
    """SQLite table for full LLM Cache (all generations)."""

    __tablename__ = "full_llm_cache"
    idx = Column(Integer,Sequence('cache_id'), primary_key=True)
    prompt = Column(String,nullable=False)
    llm = Column(String,nullable=False)
    response = Column(String)

    prompt_tsv = Column(
        TSVectorType(),
        Computed(
            # 「將 llm 和 prompt 欄位內容組合後，轉成一個可全文檢索的欄位」
            "to_tsvector('english', llm || ' ' || prompt)",
            persisted=True
        ),
    )

    # 定義額外資料表設定，如索引(能夠加速搜尋速度)
    __table_args__ = (
    Index(
        'idx_fulltext_prompt_tsv',  # 索引名稱
        prompt_tsv,                 # 要索引的欄位（必須是 tsvector 型別）
        postgresql_using='gin'     # 指定用 PostgreSQL 的 GIN 索引
    ),
)


engine = create_engine(
    "postgresql+psycopg2://Jerry:lccJerry1@localhost/landchain_mysql",
)

set_llm_cache(SQLAlchemyCache(engine,FullLLMCache))