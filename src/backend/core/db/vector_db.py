from uuid import uuid4

from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec

from src.backend.config.constants import (
    OPEN_AI_EMBEDDING_MODEL_DIMENSION,
    PINECONE_CLOUD,
    PINECONE_CLOUD_REGION,
    PINECONE_INDEX,
    PINECONE_METRIC,
)
from src.backend.config.data_ingestion_config import DataIngestionConfig
from src.backend.config.settings import settings
from src.backend.utils.logger import logging
from src.backend.utils.utils import load_docs

logger = logging.getLogger(__name__)


class VectorDb:
    def create_pinecone_index(self):
        """_summary_

        Returns:
            Bool : Returns True on successful creation
        """
        try:
            logger.info(f"Creating pinecone index {PINECONE_INDEX}...")
            vdb_pine_cone = settings.get_pine_cone()
            vdb_pine_cone.create_index(
                PINECONE_INDEX,
                spec=ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_CLOUD_REGION),
                dimension=OPEN_AI_EMBEDDING_MODEL_DIMENSION,
                metric=PINECONE_METRIC,
            )
            logger.info(f"Creating pinecone index {PINECONE_INDEX}...Completed")
            return True
        except Exception as e:
            logger.error(
                f"Unable to create pinecone index {PINECONE_INDEX} \
                    in {PINECONE_CLOUD} cloud and in {PINECONE_CLOUD_REGION} region \
                    with {OPEN_AI_EMBEDDING_MODEL_DIMENSION} dimension"
            )
            logger.error(e)
            raise

    def get_vdb_pinecone(self):
        try:
            logger.info("Getting pinecone vector db with loaded chunks...")
            embedding_model = settings.get_llm_embedding_model()
            vdb_pine_cone = settings.get_pine_cone()

            # if index does not exist create it
            if not vdb_pine_cone.has_index(PINECONE_INDEX):
                logger.info(f"Pinecone index not available {PINECONE_INDEX}...")
                self.create_pinecone_index()

            # connect to the index
            index = vdb_pine_cone.Index(PINECONE_INDEX)

            # Wrap the existing Pinecone index with LangChain's VectorStore interface
            # This allows to store and query embeddings using the given embedding model
            vdb = PineconeVectorStore(
                index=index,
                embedding=embedding_model,
            )

            path = DataIngestionConfig().save_path
            docs = load_docs(path=path)

            ids = [str(uuid4) for _ in range(len(docs))]

            # Add docs to Pinecone via Langchain wrapper
            logger.info("Loading chunks into pinecone vector db...")
            vdb.add_documents(
                documents=docs,
                uuids=ids,
            )
            logger.info("Loading chunks into pinecone vector db...completed")
            logger.info("Getting pinecone vector db with loaded chunks...completed")

            return vdb
        except Exception as e:
            logger.error("Unable to retrieve pinecone vector db...")
            logger.error(e)
            raise
