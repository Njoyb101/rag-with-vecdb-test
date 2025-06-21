from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.backend.config.settings import settings
from src.backend.core.db.vector_db import VectorDb
from src.backend.core.state.graph_sate import GraphState
from src.backend.utils.logger import logging

logger = logging.getLogger(__file__)


class RagNode:
    def __init__(self):
        self.llm = settings.get_llm()
        self.pc = settings.get_pine_cone()
        self.vectordb = VectorDb().get_vdb_pinecone()

    def rag(self, state: GraphState):
        try:
            logger.info("Running Rag Node ...")
            question = state["messages"][0]
            prompt = PromptTemplate.from_template(
                """
            You are inteligent Chatbot answer questions based on available context
            provide the answer  \n question:{question} \n context:{context}
            """,
                input_variable=["question", "context"],
            )

            retriever = self.vectordb.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={"score_threshold": 0.7},
            )

            str_parser = StrOutputParser()

            rag_chain = (
                {
                    "context": retriever,
                    "question": RunnablePassthrough(),
                }
                | prompt
                | self.llm
                | str_parser
            )

            result = rag_chain.invoke(question)
            print(result)
            return {"messages": [result]}
        except Exception as e:
            logger.error("Unable to create Rag Node")
            logger.error(e)
            raise
