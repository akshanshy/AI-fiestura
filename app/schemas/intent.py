from typing import Optional, Literal
from pydantic import BaseModel, Field


class EventIntent(BaseModel):

    intent: Literal[
    "search_events",
    "general_question",
    "out_of_scope"
]
    category: Optional[str] = None

    max_price: Optional[int] = Field(
        default=None,
        ge=0
    )  