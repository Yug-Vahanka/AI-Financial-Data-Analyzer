import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)


class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO

#  SUCCESS LOG 
success_handler = logging.FileHandler(os.path.join(LOG_DIR, "success.log"))
success_handler.setLevel(logging.INFO)
success_handler.setFormatter(formatter)
success_handler.addFilter(InfoFilter())

#  ERROR LOG 
error_handler = logging.FileHandler(os.path.join(LOG_DIR, "error.log"))
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(success_handler)
logger.addHandler(error_handler)