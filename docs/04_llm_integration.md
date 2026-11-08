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