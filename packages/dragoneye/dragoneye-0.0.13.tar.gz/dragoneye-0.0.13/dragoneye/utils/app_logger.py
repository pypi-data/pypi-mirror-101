import logging.handlers
import os

INITIALIZED = False
if not INITIALIZED:
    logger = logging.getLogger('dragoneye')
    logger.setLevel(logging.INFO)
    logger_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(logger_dir, exist_ok=True)
    logger_file = os.path.join(logger_dir, 'dragoneye.log')
    rotate_file = os.path.isfile(logger_file)
    file_handler = logging.handlers.RotatingFileHandler(logger_file, maxBytes=10000000, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
    if rotate_file:  # keeping log file per execution
        file_handler.doRollover()
    logger.addHandler(file_handler)
    logger.addHandler(logging.StreamHandler())

    INITIALIZED = True
