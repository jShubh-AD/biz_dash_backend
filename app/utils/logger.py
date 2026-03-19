import logging
from colorlog import ColoredFormatter

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },)
    )

def get_logger(name: str):
    return logging.getLogger(name)