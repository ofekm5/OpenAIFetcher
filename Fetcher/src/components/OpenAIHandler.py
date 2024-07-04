from openai import AsyncOpenAI
from openai.types import Completion
from dotenv import load_dotenv
import os
import asyncio

class OpenAIQueryError(Exception):
    pass

class OpenAIHandler:
    def __init__(self) -> None:
        load_dotenv()
        self.__client = AsyncOpenAI(
            api_key = os.getenv('SECRET_KEY')
        )
        self.__semaphore =asyncio.Semaphore(os.getenv('TOTAL_WORKERS'))

    async def schedule_query(self, prompt, question_ID: str) -> str:
        asyncio.create_task(self.__send_query(prompt, question_ID))

    async def __send_query(self, prompt: str, question_ID:str):
        try:
            chat_completion = await self.__client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="gpt-3.5-turbo",
            )
            asyncio.create_task(self.__store_answer_in_db(chat_completion, question_ID))
        except Exception as e:
            raise OpenAIQueryError(f"Error in __send_query: {e}")

    def __store_answer_in_db(self, answer:Completion, question_ID:str) -> None:
        for choice in answer.choices:#TODO: change to a snigle choice
            print(choice.text)
    