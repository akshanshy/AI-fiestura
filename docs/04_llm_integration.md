                main.py
                   |
                   v
          get_ai_provider()
                   |
            provider_factory
                   |
             AIProvider
              /       \
             /         \
    RuleBasedAI      GroqAI
       Provider      Provider
                        |
                        v
                    Groq API

AI-Fiestura – LLM Integration Interview Notes
1. Why did we integrate Groq?
Interview answer:

We integrated Groq to introduce actual LLM capabilities into AI-Fiestura. Initially, our application used a rule-based system that relied on keyword matching and regular expressions to understand user queries. This approach was limited when handling variations in natural language.

We integrated Groq's hosted LLM inference API so that AI-Fiestura could understand natural-language queries and eventually support structured intent extraction, tool calling and intelligent event recommendations.

Understand it simply:

Before:
- User had to use predictable words.
- We manually extracted filters using regex.
- Responses were mostly predefined.
After:
- LLM can understand different ways of asking questions.
- It can extract meaningful information.
- It can help decide which application functionality to invoke.
Follow-up question: Why Groq instead of running an LLM locally?

Because Groq provides hosted inference, avoiding the hardware requirements of local inference. This was particularly suitable for our development environment, which has 8 GB RAM and integrated graphics.

2. What is an LLM API?
Interview answer:

An LLM API is an interface that allows an application to communicate with a Large Language Model over HTTP. Our application sends input messages and instructions to the model and receives a generated response.

In AI-Fiestura, our FastAPI service uses the Groq Python SDK to send chat completion requests and receive responses from the selected model.

Understand it simply:

Think of it like ordering food:
- Your application sends an order (prompt).
- The LLM processes the order.
- The LLM returns the result (response).
Example from your code:
completion = self.client.chat.completions.create(    model=self.model,    messages=[        {"role": "system", "content": "You are AI-Fiestura."},        {"role": "user", "content": message}    ])



The application extracts the response using:
return completion.choices[0].message.content



Follow-up: Does the LLM run inside FastAPI?

No. In our current implementation, the model runs on Groq's infrastructure. FastAPI communicates with it through an API request.

3. What does AIProvider do?
Interview answer:

AIProvider is an abstract base class that defines a common interface for different AI providers.

It declares a generate_response() method that concrete implementations must implement.

This allows us to use different AI providers without changing the application-level logic.

Your implementation:
from abc import ABC, abstractmethodclass AIProvider(ABC):    @abstractmethod    def generate_response(self, message: str) -> str:        pass



You have two implementations:
AIProvider
    |
    |---- RuleBasedAIProvider
    |
    |---- GroqAIProvider


Understand it simply:

Imagine both providers are different employees.

Both must know how to perform the task called generate_response().

But:
- One uses predefined rules.
- The other communicates with an LLM.
The calling application doesn't need to know how they produce the response.

Important concepts: Abstraction, inheritance and polymorphism.

4. What is the Factory Pattern?
Interview answer:

The Factory Pattern is a creational design pattern that centralizes object creation.

In AI-Fiestura, we use a factory function called get_ai_provider() to decide which AI provider implementation should be instantiated.

Instead of creating providers directly inside main.py, we delegate that responsibility to the factory.

Your implementation:
def get_ai_provider():    provider = os.getenv("AI_PROVIDER", "rule_based").lower()    if provider == "groq":        return GroqAIProvider()    elif provider == "rule_based":        return RuleBasedAIProvider()



Understand it simply:

Without a factory:
ai_provider = GroqAIProvider()



With a factory:
ai_provider = get_ai_provider()



The factory decides which object to return.

Follow-up: What is the benefit?

We can switch providers through configuration without rewriting our /chat endpoint.

5. How do environment variables select providers?
Interview answer:

Environment variables allow us to configure application behaviour without hardcoding configuration values into the source code.

In AI-Fiestura, we use the AI_PROVIDER environment variable to determine which provider the factory should instantiate.

Our .env:
AI_PROVIDER=groq
GROQ_API_KEY=your_api_key


Our factory reads it:
provider = os.getenv("AI_PROVIDER", "rule_based").lower()



If the value is groq, it creates GroqAIProvider.

If the value is rule_based, it creates RuleBasedAIProvider.

Why is this useful?
- Easier configuration.
- Provider switching.
- Avoids hardcoding secrets.
- Different configurations for development and production.
Remember: environment variables are configuration, not a complete security solution. We must also protect secrets and never commit .env to GitHub.

6. How does FastAPI communicate with Groq?
Interview answer:

When a user sends a message to the /chat endpoint, FastAPI validates the request using a Pydantic model.

The endpoint calls the currently configured AI provider through its common generate_response() method.

If Groq is selected, GroqAIProvider uses the Groq Python SDK to send a chat completion request to Groq's hosted inference service.

The generated response is then returned to the user through FastAPI as a JSON response.

Complete request flow:
User
Submits a chat message

FastAPI /chat
Receives request

Pydantic
Validates message

AI Provider
Selected by factory

Groq API
Processes prompt and generates response

FastAPI JSON response


Example response:
{
    "message": "Hello AI-Fiestura",
    "reply": "Hello! I'm AI-Fiestura..."
}



7. Why did we retain the rule-based provider?
Interview answer:

We retained the rule-based provider to maintain an alternative implementation that doesn't depend on an external LLM service.

It provides a simpler response mechanism for predictable queries and allows us to test provider switching.

It can also serve as a fallback if we explicitly implement fallback logic for external provider failures.

Understand it simply:

Suppose Groq is unavailable.

Your rule-based provider still exists and can handle supported event queries without calling Groq.

However, an important distinction: your current factory supports selecting either provider, but it does not automatically switch to rule-based mode when Groq fails. That fallback mechanism is something we can implement later.

8. Quick revision sheet
Save this table in docs/04_LLM_Integration.md.
Question	                    Remember these keywords
Why Groq?        	            Hosted inference, natural-language understanding
What is LLM API?	            Input, prompt, inference, response
What is AIProvider?	            Abstract class, common interface
What is Factory Pattern?	     Centralized object creation
Environment variables?      	Configuration, provider selection
FastAPI to Groq?	            Pydantic → Provider → SDK → Response
Why RuleBased?	                Alternative provider, p