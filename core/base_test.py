
import pytest
from config import config
from core.logger import get_logger
from core.data_reader import read_test_data

class BaseTest:

    @pytest.fixture(autouse=True)
    def setup(self, page, request):
        self.page = page
        self.logger = get_logger(request.node.name)
        self.test_data = read_test_data(config.ENV)
        yield
        self.logger.info("Test completed")
