import operator
from typing import Annotated, NotRequired, Sequence, TypedDict

from langchain_core.messages import BaseMessage


class GraphState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    response: NotRequired[Annotated[Sequence[BaseMessage], operator.add]]  # optional
