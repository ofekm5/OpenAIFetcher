from openai import AsyncOpenAI
from openai.types import Completion
from dotenv import load_dotenv
import os
import asyncio
import logging
from logging.handlers import RotatingFileHandler

class OpenAIQueryError(Exception):
    pass

class OpenAIHandler:
    def __init__(self) -> None:
        load_dotenv()
        log_file_path = 'logs/openai_handler.log'
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            handlers=[
                                RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5),
                                logging.StreamHandler()
                            ])
        self.__logger = logging.getLogger(__name__)

        self.__client = AsyncOpenAI(
            api_key=os.getenv('SECRET_KEY')
        )
        self.__semaphore = asyncio.Semaphore(int(os.getenv('TOTAL_WORKERS', 5)))
        self.__event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.__event_loop)
        self.__logger.info("OpenAIHandler initialized")

    def schedule_query(self, prompt: str, question_ID: str) -> None:
        self.__logger.info(f"Scheduling query for prompt: {prompt}, question_ID: {question_ID}")
        self.__event_loop.create_task(self.__send_query(prompt, question_ID))

    async def __send_query(self, prompt: str, question_ID: str) -> None:
        async with self.__semaphore:
            try:
                self.__logger.info(f"Sending query for prompt: {prompt}, question_ID: {question_ID}")
                chat_completion = await self.__client.chat_completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="gpt-3.5-turbo",
                )
                self.__logger.info(f"Query completed for prompt: {prompt}, question_ID: {question_ID}")
                self.__event_loop.create_task(self.__store_answer_in_db(chat_completion, question_ID))
            except Exception as e:
                self.__logger.error(f"Error in __send_query: {e}")
                raise OpenAIQueryError(f"Error in __send_query: {e}")

    async def __store_answer_in_db(self, answer: Completion, question_ID: str) -> None:
        self.__logger.info(f"Storing answer in DB for question_ID: {question_ID}")
        for choice in answer.choices:  # TODO: change to a single choice
            print(choice['message']['content'])
            self.__logger.info(f"Stored answer for question_ID: {question_ID}, content: {choice['message']['content']}")
