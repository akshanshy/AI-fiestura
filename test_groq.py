from dotenv import load_dotenv
from app.services.groq_provider import GroqAIProvider

load_dotenv()

provider = GroqAIProvider()

response = provider.generate_response(
    "Introduce yourself as AI-Fiestura in two sentences."
)

print("Groq Response:")
print(response)