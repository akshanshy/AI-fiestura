
from app.services.intent_router import route_message
from app.services.provider_factory import get_ai_provider

provider = get_ai_provider()

queries = [
    "Find free AI workshops",
    "What is Fiestura?",
    "Tell me a joke about cricket",
]

for query in queries:
    print("\nUser:", query)

    try:
        result = route_message(query, provider)
        print("Intent:", result["intent"])
        print("Reply:", result["reply"])
        print("Events:", result["events"])

    except Exception as error:
        print("Error:", error)
