import logging

def setup_logger(file: str, level=logging.INFO):
  logger = logging.getLogger(file)
  if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
  return logger

