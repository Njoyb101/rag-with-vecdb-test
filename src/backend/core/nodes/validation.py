from langchain.prompts import PromptTemplate
from langchain_core.messages import BaseMessage

from src.backend.config.settings import settings
from src.backend.core.parsers.node_output_parser import parser_validator
from src.backend.core.state.graph_sate import GraphState
from src.backend.utils.logger import logging

logger = logging.getLogger(__file__)


class Validation_Node:
    def __init__(self):
        self.parser = parser_validator
        self.llm = settings.get_llm()

    def validator(self, state: GraphState) -> GraphState:
        try:
            logger.info("Running Validator Node ...")
            question = state["messages"][0]
            response = state["messages"][-1]

            prompt = PromptTemplate.from_template(
                template="""
            Your task is to evaluate whether the provided response is suitable for the
            given user question.
            If it is suitable, respond with Yes; otherwise, No. Follow the instrustions
            while giving response
            just give what required in instructions dont give additional info
            Question: {question}
            Response: {response}
            instructions:{format_instructions}
                """,
                input_variable=["question", "response"],
                partial_variables={
                    "format_instructions": self.parser.get_format_instructions()
                },
            )

            # Combine the chain
            chain = prompt | self.llm | self.parser

            # Invoke with format instructions passed
            res = chain.invoke(
                {
                    "question": question,
                    "response": response,
                }
            )

            return {"messages": [res.Res], "response": [res.reason]}

        except Exception as e:
            logger.error("Unable to create Validator Node")
            logger.error(e)
            raise

    def Route_to(self, state: GraphState) -> BaseMessage:
        return state["messages"][-1]
