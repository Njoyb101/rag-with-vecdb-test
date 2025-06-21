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
            workflow = StateGraph(GraphState)

            workflow.add_node("supervisor", SuperviserNode().supervisor)
            workflow.add_node("router", RouterNode().router)
            workflow.add_node("llm", LlmNode().llm_node)
            workflow.add_node("rag", RagNode().rag)
            workflow.add_node("web", WebSearchNode().web)
            workflow.add_node("validator", ValidatorNode().validator)
            workflow.add_node("rewrite", RewriterNode().rewrite)

            workflow.set_entry_point("supervisor")

            workflow.add_conditional_edges(
                source="supervisor",
                path=RouterNode().router,
                path_map={
                    "rag": "rag",
                    "llm": "llm",
                    "web": "web",
                },
            )

            workflow.add_conditional_edges(
                source="validator",
                path=ValidatorNode().route_to,
                path_map={
                    "Yes": END,
                    "No": "rewrite",
                },
            )

            workflow.add_edge("rag", "validator")
            workflow.add_edge("llm", "validator")
            workflow.add_edge("web", "validator")
            workflow.add_edge("rewrite", "supervisor")

            workflow.set_finish_point("validator")
            return workflow.compile()

        except Exception as e:
            logger.error("Unable to create workflow")
            logger.error(e)
            raise
