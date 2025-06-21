from langchain.prompts import PromptTemplate

from src.backend.config.settings import settings
from src.backend.core.state.graph_sate import GraphState
from src.backend.utils.logger import logging

logger = logging.getLogger(__file__)


class LlmNode:
    def __init__(self):
        self.llm = settings.get_llm()

    def llm_node(self, state: GraphState):
        try:
            logger.info("Running LLM Node ...")
            question = state["messages"][0]

            prompt = PromptTemplate.from_template(
                template="""
                    You are intelligent Chatbot answer the  questions Relevently
                    question:{question}
                """,
                input_variable=["question"],
            )

            chain = prompt | self.llm

            res = chain.invoke({"question": question})

            return {"messages": [res.content]}
        except Exception as e:
            logger.error("Unable to create Rag Node")
            logger.error(e)
            raise
