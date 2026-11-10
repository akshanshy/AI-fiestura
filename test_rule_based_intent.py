from app.services.ai_provider import RuleBasedAIProvider

provider = RuleBasedAIProvider()

queries = [
    "Find free AI workshops",
    "Show technology workshops under 500",
    "What is Fiestura?",
    "Tell me a joke about cricket",
    "Show me AI events",
]

for query in queries:
    intent = provider.extract_intent(query)
    print(f"\nQuery: {query}")
    print(intent.model_dump())