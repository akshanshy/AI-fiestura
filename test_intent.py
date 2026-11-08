from app.schemas.intent import EventIntent

intent = EventIntent(
    intent="search_events",
    category="AI",
    max_price=0
)

print(intent.model_dump())