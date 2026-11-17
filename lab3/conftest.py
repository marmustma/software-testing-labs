import os
import threading

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from werkzeug.serving import make_server

from app import app

BASE_URL = "http://127.0.0.1:5003"


def create_driver():
    """Инициализация Chrome через WebDriver.

    По умолчанию драйвер скачивает webdriver-manager. Если задана переменная
    CHROMEDRIVER_PATH (окружение без доступа к интернету), используется она.
    """
    options = webdriver.ChromeOptions()
    if os.getenv("HEADLESS", "1") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")
    if os.getenv("CHROME_BINARY"):
        options.binary_location = os.environ["CHROME_BINARY"]

    driver_path = os.getenv("CHROMEDRIVER_PATH")
    if not driver_path:
        from webdriver_manager.chrome import ChromeDriverManager
        driver_path = ChromeDriverManager().install()
    return webdriver.Chrome(service=Service(driver_path), options=options)


@pytest.fixture(scope="session", autouse=True)
def server():
    """Поднимает тестовый стенд (Flask) на время прогона тестов."""
    srv = make_server("127.0.0.1", 5003, app, threaded=True)
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    yield BASE_URL
    srv.shutdown()


@pytest.fixture
def driver():
    drv = create_driver()
    drv.implicitly_wait(3)
    yield drv
    drv.quit()
