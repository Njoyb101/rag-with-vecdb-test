from langchain.prompts import PromptTemplate

from src.backend.config.settings import settings
from src.backend.core.parsers.node_output_parser import parser_rewriter
from src.backend.core.state.graph_sate import GraphState
from src.backend.utils.logger import logging

logger = logging.getLogger(__file__)


class RewriterNode:
    def __init__(self):
        self.llm = settings.get_llm()
        self.parser = parser_rewriter

    def rewrite(self, state: GraphState) -> GraphState:
        try:
            logger.info("Running Rewriter Node...")
            old_question = state["messages"][0]
            response = state["response"][-1]  # type: ignore
            prompt = PromptTemplate.from_template(
                template="""
                You are an expert at re-writing user questions to improve clarity
                and correctness.

                You will receive:
                - The **original question**: {old_question}
                - The **validation response**: {response}, which explains
                why the question is unclear or invalid.

                Based on the validation feedback, rewrite the question to make it valid
                or clearer. give the response based on given instructions just give
                what required in instructions
                dont provide any additional info

                Follow the format exactly as given below :
                {instructions}
                """,
                input_variable=["response", "old_question"],
                partial_variables={
                    "instructions": self.parser.get_format_instructions()
                },
            )

            chain = prompt | self.llm | self.parser
            result = chain.invoke(
                {
                    "response": response,
                    "old_question": old_question,
                }
            )

            return {"messages": [result.question]}
        except Exception as e:
            logger.error("Unable to create Rewriter Node")
            logger.error(e)
            raise
