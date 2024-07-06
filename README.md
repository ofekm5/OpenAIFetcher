# OpenAIFetcher
A chatgpt simulator handling requests in async manner with polling mechanism

## Creation Process:
1. Research about OpenAI API, SQLAlchemy and Alembic
2. Designing the SQL schema
3. Developing the flask server
    a. creating & testing OpenAIAPIHandler
    b. creating & testing Sanitizer
    c. creating & testing Scheduler(handling API calls in event loop with asyncio)
    d. creating & testing DB integration(alembic, sqlalchemy and DB migrations)
4. Testing with pytest


## Incoming request format:
1. POST method only!
2. Its body should be a json with the following format:
    {
        "question": "<the question>" 
    }