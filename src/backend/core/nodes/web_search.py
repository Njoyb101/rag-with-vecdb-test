from dataclasses import dataclass

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import BaseMessage

from src.backend.core.state.graph_sate import GraphState
from src.backend.utils.logger import logging

logger = logging.getLogger(__file__)


@dataclass
class WebSearchNode:
    def web(self, state: GraphState) -> GraphState:
        try:
            logger.info("Running Web Search Node ...")
            message: BaseMessage = state["messages"][0]
            question = message.content

            # Handle unexpected types (e.g., list or dict)
            if isinstance(question, list):
                question = (
                    question[0] if isinstance(question[0], str) else str(question[0])
                )
            elif isinstance(question, dict):
                question = str(question)

            search = DuckDuckGoSearchRun()
            response = search.run(question)

            print(response)
            return {"messages": [response]}
        except Exception as e:
            logger.error("Unable to create Web Search Node")
            logger.error(e)
            raise
