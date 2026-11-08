What is intent extraction?
Intent extraction is the process of identifying what a user wants to accomplish from their natural-language message and converting it into structured information that an application can process.

What is structured output?
Structured output means generating data in a predefined format, such as JSON, rather than unrestricted natural-language text.

Why use Pydantic?
Pydantic validates incoming data against predefined schemas and data types.

Important interview distinction:
Intent extraction and tool calling are not the same.
- Intent extraction identifies what the user wants.
- Tool calling allows the LLM to request execution of a function or tool.
We'll implement both.