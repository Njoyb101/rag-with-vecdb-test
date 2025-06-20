from uuid import uuid4

from langchain_pinecone import PineconeVectorStore

from src.backend.config.data_ingestion_config import DataIngestionConfig
from src.backend.config.settings import settings
from src.backend.utils.logger import logging
from src.backend.utils.utils import load_docs

logger = logging.getLogger(__name__)


class VectorDb:
    def get_vdb_pinecone(self):
        try:
            embedding_model = settings.get_llm_embedding_model()
            vdb_pine_cone = settings.get_pine_cone()

            index = vdb_pine_cone.Index("chat")

            vdb = PineconeVectorStore(
                index=index,
                embedding=embedding_model,
            )

            path = DataIngestionConfig().data_pdf_path
            docs = load_docs(path=path)

            ids = [str(uuid4) for _ in range(len(docs))]

            vdb.add_documents(
                documents=docs,
                uuids=ids,
            )

            return vdb
        except Exception as e:
            logger.error("Unable to retrieve pinecone vector db...")
            logger.error(e)
            raise
