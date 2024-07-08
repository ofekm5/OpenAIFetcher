import asyncio
from flask import jsonify
from threading import Thread
from app.components.OpenAIFetcher import OpenAIFetcher
from app.components.Logger import create_logger

TOTAL_WORKERS = 5

class Scheduler:
    def __init__(self) -> None:
        self.__semaphore = asyncio.Semaphore(TOTAL_WORKERS)
        self.__openAI_fetcher = OpenAIFetcher()
        self.__logger = create_logger(__name__, 'logs/scheduler.log')
        self.__logger.info('Scheduler initialized')
        self.__loop = asyncio.new_event_loop()
        self.__loop_thread = Thread(target=self.__start_event_loop, args=(self.__loop,))
        self.__loop_thread.start()

    def __start_event_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    async def __ask_question(self, question: str, question_id: str) -> None:
        async with self.__semaphore:
            await self.__openAI_fetcher.send_query_and_store_result(question, question_id)

    def schedule_question(self, question: str, question_id: str) -> None:
        try:
            if self.__semaphore._value == 0:
                self.__logger.info('Overloaded with requests')
                return jsonify({'status': 'Too many concurrent requests'}), 429  
            else:
                self.__logger.info(f"Scheduling question {question_id}: {question}")
                asyncio.run_coroutine_threadsafe(self.__ask_question(question, question_id), self.__loop)
                return jsonify({'status': 'Task started'}), 202
        except Exception as e:
            self.__logger.error(str(e))
            return jsonify({'status': 'Error', 'message': str(e)}), 500
        
    def __del__(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.loop_thread.join()
        self.__logger.info('Scheduler cleaned up and loop stopped')
