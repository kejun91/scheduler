import logging
from logging.handlers import TimedRotatingFileHandler
import os
from pathlib import Path
import sys

from app.utils.datetime import get_local_timezone_offset
from app.utils.path import get_project_root_dir

local_timezone_offset = get_local_timezone_offset()

class CustomFormatter(logging.Formatter):
    pass

def get_logger(logger_name = None):
    logging.basicConfig(level=logging.INFO)
    entry_file_name = sys.argv[0].split(os.path.sep)[-1]

    dir_name = logger_name

    if logger_name is not None:
        pass
    elif entry_file_name == 'start.py':
        dir_name = 'web'
        logger_name = 'web'
        if len(sys.argv) > 1:
            if sys.argv[1] == 'run_scheduled':
                dir_name = 'scheduled'
                logger_name = 'scheduled'
    else:
        dir_name = 'custom_scripts'
        logger_name = entry_file_name.split('.')[0]

    logger = logging.getLogger(logger_name)
    log_dir = os.path.join(get_project_root_dir(),"logs",dir_name)
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    handler = TimedRotatingFileHandler(
        filename= os.path.join(get_project_root_dir(),"logs",dir_name,f"{logger_name}.log"),
        when="midnight",
        interval=1,
        backupCount=60
    )
    formatter = CustomFormatter(fmt=f'[%(asctime)s.%(msecs)03d{local_timezone_offset}] [%(levelname)s] %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = get_logger()