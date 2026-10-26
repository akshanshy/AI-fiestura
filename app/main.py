
import logging
from typing import Optional

from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field

from app.data.events import events
from app.services.provider_factory import get_ai_provider
from app.tools.event_tools import search_events, get_event_by_id
app = FastAPI()
ai_provider = get_ai_provider()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def home():
    logger.info("Home endpoint accessed")
    return {"message": "Welcome to AI-Fiestura!"}


class EventResponse(BaseModel):
    id: int
    title: str
    category: str
    price: int


@app.get("/events", response_model=list[EventResponse])
def get_events(
    max_price: Optional[int] = Query(default=None, ge=0)
):
    filtered_events = events

    if max_price is not None:
        filtered_events = [
            event for event in filtered_events
            if event["price"] <= max_price
        ]

    return filtered_events

@app.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: int):
    event = get_event_by_id(event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    return event

@app.get("/health")
def health_check():
    health={
        "status": "healthy",
        "uptime": "24 hours"
    }
    return health

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)

class ChatResponse(BaseModel):
    message: str
    reply: str

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        reply = ai_provider.generate_response(request.message)

        return ChatResponse(
            message=request.message,
            reply=reply,
        )

    except Exception:
        logger.exception(
            "Unexpected error while generating chat response"
        )

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing your request.",
        )

@app.get("/test-event-search")
def test_event_search(max_price: int | None = None, category: str | None = None):
    return {"events": search_events(max_price, category)}