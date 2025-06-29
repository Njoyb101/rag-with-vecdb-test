from src.backend.config.constants import CONFIG_YAML_PATH
from src.backend.utils.logger import logging
from src.backend.utils.utils import read_yaml

logger = logging.getLogger(__name__)


class DataIngestionConfig:
    def __init__(self):
        logger.info("Loading YAML file...")
        data_config = read_yaml(CONFIG_YAML_PATH)
        self.data_pdf_path = data_config["DataIngestion"]["data_pdf_path"]
        self.save_path = data_config["DataIngestion"]["save_path"]
        logger.info(f"data_pdf_path = {self.data_pdf_path}")
        logger.info(f"save_path = {self.save_path}")
        logger.info("Loading YAML file...completed")
