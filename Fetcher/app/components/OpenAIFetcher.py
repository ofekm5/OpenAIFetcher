from openai import AsyncOpenAI
from openai.types import Completion
from dotenv import load_dotenv
import os
from app.components.Logger import create_logger
from app.models import db, Response

class OpenAIQueryError(Exception):
    pass

class OpenAIFetcher:
    def __init__(self) -> None:
        load_dotenv()
        self.__logger = create_logger(__name__, 'logs/openai_handler.log')

        self.__client = AsyncOpenAI(
            api_key=os.getenv('SECRET_KEY')
        )
        self.__logger.info("OpenAIHandler initialized")

    async def send_query_and_store_result(self, i_prompt: str, question_ID: str) -> None:
        try:
            self.__logger.info(f"Sending query for prompt: {i_prompt}, question_ID: {question_ID}")
            chat_completion = await self.__client.completions.create(
                prompt=i_prompt,
                model="gpt-3.5-turbo-instruct"
            )
            self.__logger.info(f"Query completed for prompt: {i_prompt}, question_ID: {question_ID}")
            self.__store_answer_in_db(chat_completion, question_ID)
        except Exception as e:
            self.__logger.error(f"Error in __send_query: {e}")
            raise OpenAIQueryError(f"Error in __send_query: {e}")

    def __store_answer_in_db(self, answer: Completion, question_ID: str) -> None:
        self.__logger.info(f"Storing answer in DB for question_ID: {question_ID}")
        choice = answer.choices[0]  
        new_response = Response(prompt_id=question_ID, response=choice.text)
        db.session.add(new_response)
        db.session.commit()
        self.__logger.info(f"Stored answer for question_ID: {question_ID}, content: {choice.text}")