import asyncio
from flask import jsonify
from components.OpenAIHandler import OpenAIFetcher
from dotenv import load_dotenv
import os
from components.Logger import create_logger

class Scheduler:
    def __init__(self) -> None:
        load_dotenv()
        TOTAL_WORKERS = int(os.getenv('TOTAL_WORKERS', 5)) 
        self.__semaphore = asyncio.Semaphore(TOTAL_WORKERS)
        self.__openAI_fetcher = OpenAIFetcher()
        if not asyncio.get_event_loop().is_running():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        self.__logger = create_logger(__name__, 'logs/scheduler.log')
        self.__logger.info('Scheduler initiallized')

    async def __ask_question(self, question:str, question_id:str) -> None:
        async with self.__semaphore:
            await self.__openAI_fetcher.send_query_and_store_result(question, question_id)

    def schedule_question(self, question:str, question_id:str) -> None:
        try:
            if self.__semaphore._value == 0:
                self.__logger.info('overloaded with requests')
                return jsonify({'status': 'Too many concurrent requests'}), 429  
            else:
                self.__logger.info(f"scheduling question {question_id}: {question}")
                asyncio.ensure_future(self.__ask_question(question, question_id))
                return jsonify({'status': 'Task started'}), 202
        except Exception as e:
            self.__logger.error(str(e))
            return jsonify({'status': 'Error', 'message': str(e)}), 500
