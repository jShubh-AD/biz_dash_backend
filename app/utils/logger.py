import logging
from colorlog import ColoredFormatter

def setup_logging():
    handler = logging.StreamHandler()

    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # 🔥 important for uvicorn (prevents duplicate logs)
    if root.hasHandlers():
        root.handlers.clear()

    root.addHandler(handler)


def get_logger(name: str):
    return logging.getLogger(name)