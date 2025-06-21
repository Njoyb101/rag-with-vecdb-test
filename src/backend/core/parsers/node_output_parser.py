from langchain.output_parsers import PydanticOutputParser

from src.backend.config.node_output_parser_config import (
    RewriterParserConfig,
    SupervisorParserConfig,
    ValidatorParserConfig,
)

parser_rewriter = PydanticOutputParser(pydantic_object=RewriterParserConfig)
parser_supervisor = PydanticOutputParser(pydantic_object=SupervisorParserConfig)
parser_validator = PydanticOutputParser(pydantic_object=ValidatorParserConfig)
