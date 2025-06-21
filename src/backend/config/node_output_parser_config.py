from pydantic import BaseModel, Field


class SupervisorParserConfig(BaseModel):
    node_selection: str = Field(description="Must be one of 'rag', 'llm', or 'web'")
    node_selection_reason: str = Field(description="Reason for selection")


class ValidatorParserConfig(BaseModel):
    response: str = Field(description="Response Yes or No")
    reason: str = Field(description="Reason for the response")


class RewriterParserConfig(BaseModel):
    question: str = Field(description="Rewritten version of the original query")
    explanation: str = Field(
        description="Explanation of how this version differs from original question"
    )
