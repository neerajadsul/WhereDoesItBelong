First wanted to understand the problem domain.
So first looked at the evaluation dataset and implemented the endpoint to 
understand the API request.
For this context, I assumed that users of this package are for developers who will experiment a lot and build a final app for cross-domain end-users.

Based on that I planned two challenge areas to solve the problem.
1. Getting correct category ids based on the input.

2. Provide a developer API for experimentation.

Initially manually created the prompt and used it in Chat mode GPT. Iterated a bit and got it working. We can go on more details later on.

Designed high-level logical modules by following single-responsibility and LISCOV substitution principal. That resulted encapuslating prediction functionality which then gets its dependencies from a LLM module, prompt processor and a datastore. 

For individual modules, I tried to keep each component testable with dependency injection. Don't like to use mocks unless absolutley essential. Also used ABC pattern to be able to implement various approaches but keeping the same API.

During implementation, I tend to write unit tests in "if-main" first and then move it to dedicated tests suite. Finished with minimal implementation to be able to experiment directly with the API.

It was fun iterative experimentation to make the LLM behave like I wanted.