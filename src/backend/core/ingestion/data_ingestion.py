from typing import List

from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.backend.config.data_ingestion_config import DataIngestionConfig
from src.backend.utils.logger import logging
from src.backend.utils.utils import save_chunks

logger = logging.getLogger(__name__)


class ChunkExtractor:
    """
    Extracts  chunks from a given file.

    This class loads a files from the specified file path and
    splits its content into smaller chunks.
    """

    def __init__(self, data_path: str):
        """Initialize the extractor with the path to the file.

        Args:
            data_path (str): Path to the input file.
        """
        self.data_path = data_path

    def extract_pdf_chunks(self) -> List[Document]:
        """Load the PDF and split it into text chunks
        with langchain Recursive text splitter.

        Returns:
            List[Document]: A list of Document(text) chunks extracted from the PDF
        """
        try:
            logger.info("Loading PDF data...")
            docs = PyPDFLoader(file_path=self.data_path).load()
            logger.info("Loading PDF data...completed")

            logger.info("Splitting PDF data...")
            chunks = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=100,
            ).split_documents(docs)
            logger.info("Splitting PDF data...completed")
            return chunks

        except Exception as e:
            logger.error("Unable to extract PDF chunks")
            logger.exception(e)
            raise


class ChunkSaver:
    """
    Saves text chunks to a specified path.

    This class handles the persistence of document chunks that have
    been extracted from a PDF or other source.
    """

    def __init__(self, save_path: str):
        """Initialize the saver with a destination path.

        Args:
            save_path (str): _description_
        """
        self.save_path = save_path

    def save(self, chunks: List[Document]):
        """Save the provided chunks to the specified path.

        Args:
            chunks (List[Document]): List of document chunks to save.
        """
        try:
            logger.info("Saving PDF data into chunks...")
            save_chunks(path=self.save_path, chunks=chunks)
            logger.info("Saving PDF data into chunks...completed")
        except Exception as e:
            logger.error("Unable to store chunks")
            logger.exception(e)
            raise


class DataIngestion:
    """
    Orchestrates the data ingestion pipeline from file to chunk storage.

    This class combines the functionality of ChunkExtractor and
    ChunkSaver to run a complete ingestion workflow.
    """

    def __init__(self):
        """
        Initialize the ingestion process with a configuration.

        Args:
            config (DataIngestionConfig): Configuration object containing
                paths for input PDF and output chunk storage.
        """
        self.config = DataIngestionConfig()
        self.extractor = ChunkExtractor(data_path=self.config.data_pdf_path)
        self.saver = ChunkSaver(save_path=self.config.save_path)

    def ingest(self):
        """
        Run the complete ingestion process: extract chunks and save them.
        """
        chunks = self.extractor.extract_pdf_chunks()
        self.saver.save(chunks)
