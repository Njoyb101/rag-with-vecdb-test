import pickle
from typing import List

import yaml
from langchain.docstore.document import Document

from src.backend.utils.logger import logging

logger = logging.getLogger(__name__)


def read_yaml(path: str):
    try:
        logger.info(f"Reading yaml file from {path}...")
        with open(path, "r") as file:
            data = yaml.safe_load(file)
        logger.info(f"Reading yaml file from {path}...completed")
        return data

    except Exception as e:
        logger.error(f"Unable to read yaml from {path}")
        logger.error(e)
        raise


def save_chunks(path: str, chunks: List[Document]):
    try:
        logger.info(f"storing chunks at {path}...")
        with open(path, "wb") as file:
            pickle.dump(chunks, file)
        logger.info(f"storing chunks at {path}...completed")

    except Exception as e:
        logger.error(f"Unable to store chunks at {path}")
        logger.error(e)
        raise


def load_docs(path: str):
    """Loads pickle files from path

    Args:
        path (str): _description_

    Returns:
        _type_: _description_
    """
    try:
        logger.info(f"Loading chunks from {path}...")
        with open(path, "rb") as f:
            docs = pickle.load(f)
        logger.info(f"Loading chunks from {path}...completed")
        return docs
    except Exception as e:
        logger.error(f"Unable to load pickle chunks from {path}")
        logger.error(e)
        raise
