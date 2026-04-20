import logging
import os

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_logger(name):
    project_root = get_project_root()
    reports_path = os.path.join(project_root, "reports")
    log_file = os.path.join(reports_path, "test.log")

    os.makedirs(reports_path, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger