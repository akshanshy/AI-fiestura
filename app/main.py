
from fastapi import FastAPI, Query
from typing import Optional
from pydantic import BaseModel, Field
app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to AI-Fiestura!"}



@app.get("/events")
def get_events(max_price: Optional[int] = Query(default=None, ge=0)):
    events = [
        {"id": 1, "title": "AI Workshop", "price": 100},
        {"id": 2, "title": "Hackathon", "price": 200},
        {"id": 3, "title": "Coding Contest", "price": 0}
    ]

    if max_price is not None:
        events = [
            event for event in events
            if event["price"] <= max_price
        ]

    return {"events": events}


@app.get("/health")
def health_check():
    health={
        "status": "healthy",
        "uptime": "24 hours"
    }
    return health

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


@app.post("/chat")
def chat(request: ChatRequest):
    return {
        "message": request.message,
        "reply": f"You asked: {request.message}"
    }
