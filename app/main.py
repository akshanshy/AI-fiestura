
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to AI-Fiestura!"}


@app.get("/events")
def get_events():
    events = [
        {"id": 1, "title": "AI Workshop", "price": 100},
        {"id": 2, "title": "Hackathon", "price": 200},
        {"id": 3, "title": "Coding Contest", "price": 0}
    ]

    return {"events": events}

@app.get("/health")
def health_check():
    health={
        "status": "healthy",
        "uptime": "24 hours"
    }
    return health