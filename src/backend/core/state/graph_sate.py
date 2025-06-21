import operator
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage


class GraphState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    response: Annotated[Sequence[BaseMessage], operator.add] | None
