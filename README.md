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
5. Contructing the docker compose


## Incoming request format:
1. /question endpoint[POST]:
    Its body should be a json with the following format:
    {
        "question": "<the question>" 
    }
    the server returns a json with the appropriate questionID for future polling
2.  /answer endpoint[GET]: 
    questionID as query param(/answer?questionID=2)
    the server returns a json with the answer(when finished fetching)