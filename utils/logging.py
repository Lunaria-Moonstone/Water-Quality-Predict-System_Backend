import logging

from utils.util import singleton

@singleton
class LoggingHandler:
  def __init__(self) -> None:
    self.handler = logging.FileHandler('app.log', encoding='utf-8')
    logging_format = logging.Formatter(
      '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s'
    )
    self.handler.setFormatter(logging_format)
  def getHandler(self):
    return self.handler