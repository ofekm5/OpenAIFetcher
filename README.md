# OpenAIFetcher
A chatgpt simulator

## Creation Process:
1. Research about OpenAI API, SQLAlchemy and Alembic
2. Designing the SQL schema
3. Developing the flask server
    a. creating & testing OpenAIAPIHandler
    b. creating & testing Sanitizer
    c. creating & testing DBClient
4. Testing with pytest


## The incoming request:
1. POST method only!
2. Its body should be a json with the following format:
    {
        "question": "<the question>" 
    }