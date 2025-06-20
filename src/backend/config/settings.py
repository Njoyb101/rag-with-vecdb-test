import os

from dotenv import find_dotenv, load_dotenv
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings

from src.backend.config.constants import (
    OPEN_AI_CHAT_TOOLS_MODEL,
    OPEN_AI_EMBEDDING_MODEL,
)

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    openai_api_key: SecretStr = Field(..., alias="OPENAI_API_KEY")
    pinecone_api_key: SecretStr = Field(..., alias="PINECONE_API_KEY")
    default_chat_tools_model_name: str = OPEN_AI_CHAT_TOOLS_MODEL
    default_embedding_model_name: str = OPEN_AI_EMBEDDING_MODEL

    class Config:
        env_file = ".env"  # Optional fallback
        case_sensitive = True
        populate_by_name = True  # needed when using alias in Field() tells Pydantic to allow field names and aliases to work interchangeably  # noqa: E501
        # arbitrary_types_allowed = True  # ✅ Helps with types like SecretStr

    def get_llm(self):
        from langchain_openai import ChatOpenAI

        model = ChatOpenAI(
            model=self.default_chat_tools_model_name,
            api_key=self.openai_api_key,
        )
        return model

    def get_llm_embedding_model(self):
        from langchain.embeddings import OpenAIEmbeddings

        model = OpenAIEmbeddings(
            model=self.default_embedding_model_name,
            api_key=self.openai_api_key.get_secret_value(),
        )
        return model

    def get_pine_cone(self):
        from pinecone import Pinecone

        pc = Pinecone(
            api_key=self.pinecone_api_key.get_secret_value(),
        )
        return pc


settings = Settings()  # type: ignore

# ✅ Remove key from global env to prevent accidental exposure
os.environ.pop("OPENAI_API_KEY", None)
os.environ.pop("PINECONE_API_KEY", None)
