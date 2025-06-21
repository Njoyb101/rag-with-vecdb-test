from src.backend.core.state.graph_sate import GraphState
from src.backend.utils.logger import logging

logger = logging.getLogger(__file__)


class RouterNode:
    def router(self, state: GraphState):
        try:
            logger.info("Running Router Node ...")
            last_msg = state["messages"][-1]

            logger.info(f"Routing to ...{last_msg}")

            return last_msg
        except Exception as e:
            logger.error("Unable to create Router Node")
            logger.error(e)
            raise
