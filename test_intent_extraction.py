from dotenv import load_dotenv
from app.services.groq_provider import GroqAIProvider

load_dotenv()

provider = GroqAIProvider()

queries = [
    "Find free AI workshops",
    "Show me technology events under 500 rupees",
    "What is Fiestura?",
    "Tell me a joke about cricket"
]

for query in queries:

    print("\nUser:", query)

    intent = provider.extract_intent(query)

    print("Extracted intent:", intent.model_dump())