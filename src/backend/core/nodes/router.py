from src.backend.core.state.graph_sate import GraphState
from src.backend.utils.logger import logging

logger = logging.getLogger(__file__)


class RouterNode:
    def router(self, state: GraphState):
        try:
            logger.info("Running Router Node ...")
            last_msg = state["messages"][-1]

            route_path = last_msg.content

            # Handle unexpected types (e.g., list or dict)
            if isinstance(route_path, list):
                route_path = (
                    route_path[-1]
                    if isinstance(route_path[-1], str)
                    else str(route_path[-1])
                )
            elif isinstance(route_path, dict):
                route_path = str(route_path)

            logger.info(f"Routing to ...{route_path}")

            return route_path
        except Exception as e:
            logger.error("Unable to create Router Node")
            logger.error(e)
            raise
