from langchain.prompts import PromptTemplate

from src.backend.config.settings import settings
from src.backend.core.parsers.node_output_parser import parser_supervisor
from src.backend.core.state.graph_sate import GraphState
from src.backend.utils.logger import logging

logger = logging.getLogger(__file__)


class SuperviserNode:
    def __init__(self):
        self.llm = settings.get_llm()
        self.parser_supervisor = parser_supervisor

    def supervisor(self, state: GraphState) -> GraphState:
        try:
            logger.info("Running Supervisor Node ...")
            question = state["messages"][-1]

            prompt = PromptTemplate.from_template(
                """
            You are a classification agent.
            Your task is to classify the following question into one of the
            three categories: [rag, llm, web].

            - Use **'rag'** if the question asks about economic data, statistics,
            policies, or insights specifically related
            to the **State of Analytics Engineering report**.
            - Use **'llm'** if it is a general knowledge or reasoning question
            **not related** to the **State of Analytics Engineering report**.
            - Use **'web'** if the question requires **real-time**, **recent**, or
            **online search-based** information.

            Follow this format when responding give only what required in instructions
            don't give any unnecessary Info:
            {instructions}

            Question: {question}
            """,
                partial_variables={
                    "instructions": self.parser_supervisor.get_format_instructions()
                },
            )

            chain = prompt | self.llm | self.parser_supervisor

            result = chain.invoke({"question": question})

            logger.info(f"Result received from Supervisor Node ...{result}")

            return {"messages": [result.node_selection]}
        except Exception as e:
            logger.error("Unable to create Supervisor Node")
            logger.error(e)
            raise
