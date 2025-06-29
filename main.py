def main():
    ## Testing LLM Invocation + checking if API key is exposable
    # import os
    # from src.backend.config.settings import settings
    # llm = settings.get_llm()
    # res = llm.invoke("Hello")
    # print(res.content)
    # print(
    #     f"open ai api key from global: {os.getenv('OPENAI_API_KEY')}"
    # )  # ✅ safe : revoked  # noqa: E501
    # print(
    #     f"open ai api key from class: {settings.openai_api_key}"
    # )  # ✅ safe : can't be printed as pydantic SecretStr  # noqa: E501

    ## Testing if YAML is being read properly
    # from src.backend.core.ingestion.data_ingestion import DataIngestion

    # di = DataIngestion()
    # di.ingest()

    # Testing workflow

    from IPython.display import Image, display
    from langchain_core.messages import HumanMessage

    from src.backend.core.state.graph_sate import GraphState
    from src.backend.core.workflow.workflow import Workflow
    from src.backend.utils.logger import logging

    logger = logging.getLogger(__file__)

    state: GraphState = {
        "messages": [
            HumanMessage(content="Where should I invest in analytics for future ?")
        ]
    }
    workflow = Workflow().create_workflow(state=state)

    display(Image(workflow.get_graph().draw_mermaid_png()))

    response = workflow.invoke(state)
    final_message = response["messages"][-2]
    logger.info(final_message)


if __name__ == "__main__":
    main()
