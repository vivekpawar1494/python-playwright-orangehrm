from config import config
from core.logger import get_logger


class LoginPage:

    @staticmethod
    def navigate(page):
        logger = get_logger(LoginPage.__name__)
        logger.info("Navigating to home page URL")
        page.goto(config.BASE_URL, timeout=60000, wait_until="domcontentloaded")
