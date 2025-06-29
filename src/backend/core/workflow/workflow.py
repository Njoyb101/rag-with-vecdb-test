from langgraph.graph import END, StateGraph

from src.backend.core.nodes.llm import LlmNode
from src.backend.core.nodes.rag import RagNode
from src.backend.core.nodes.rewriter import RewriterNode
from src.backend.core.nodes.router import RouterNode
from src.backend.core.nodes.suprvisor import SuperviserNode
from src.backend.core.nodes.validation import ValidatorNode
from src.backend.core.nodes.web_search import WebSearchNode
from src.backend.core.state.graph_sate import GraphState
from src.backend.utils.logger import logging

logger = logging.getLogger(__file__)


class Workflow:
    def __init__(self):
        pass

    def create_workflow(self, state: GraphState):
        try:
            logger.info("Creating Workflow...")
            workflow = StateGraph(GraphState)

            logger.info("Creating supervisor node...")
            workflow.add_node("supervisor", SuperviserNode().supervisor)
            logger.info("Creating supervisor node...completed")

            logger.info("Creating router node...")
            workflow.add_node("router", RouterNode().router)
            logger.info("Creating router node...completed")

            logger.info("Creating llm node...")
            workflow.add_node("llm", LlmNode().llm_node)
            logger.info("Creating llm node...completed")

            logger.info("Creating rag node...")
            workflow.add_node("rag", RagNode().rag)
            logger.info("Creating rag node...completed")

            logger.info("Creating WebSearchNode node...")
            workflow.add_node("web", WebSearchNode().web)
            logger.info("Creating WebSearchNode node...completed")

            logger.info("Creating ValidatorNode node...")
            workflow.add_node("validator", ValidatorNode().validator)
            logger.info("Creating ValidatorNode node...completed")

            logger.info("Creating RewriterNode node...")
            workflow.add_node("rewrite", RewriterNode().rewrite)
            logger.info("Creating RewriterNode node...completed")

            logger.info("Setting Entry point...")
            workflow.set_entry_point("supervisor")
            logger.info("Setting Entry point...completed")

            logger.info("add_conditional_edges supervisor...")
            workflow.add_conditional_edges(
                source="supervisor",
                path=RouterNode().router,
                path_map={
                    "rag": "rag",
                    "llm": "llm",
                    "web": "web",
                },
            )
            logger.info("add_conditional_edges supervisor...completed")

            logger.info("add_conditional_edges validator...")
            workflow.add_conditional_edges(
                source="validator",
                path=ValidatorNode().route_to,
                path_map={
                    "Yes": END,
                    "No": "rewrite",
                },
            )
            logger.info("add_conditional_edges validator...completed")

            logger.info("Adding Edges...")
            workflow.add_edge("rag", "validator")
            workflow.add_edge("llm", "validator")
            workflow.add_edge("web", "validator")
            workflow.add_edge("rewrite", "supervisor")
            logger.info("Adding Edges...completed")

            logger.info("Setting Finish Point...")
            workflow.set_finish_point("validator")
            logger.info("Setting Finish Point...completed")

            logger.info("Compiling workflow...")
            app = workflow.compile()
            logger.info("Compiling workflow...completed")

            return app

        except Exception as e:
            logger.error("Unable to create workflow")
            logger.error(e)
            raise
