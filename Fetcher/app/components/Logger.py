from logging import Logger
from logging.handlers import RotatingFileHandler
import os
import logging

def create_logger(name:str, path:str) -> Logger:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            RotatingFileHandler(path, maxBytes=10*1024*1024, backupCount=5),
                            logging.StreamHandler()
                        ])
    return logging.getLogger(name)