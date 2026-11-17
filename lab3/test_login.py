"""Задание 3: вход с валидными данными и проверка появления элемента Logout."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import BASE_URL

VALID_LOGIN = "student"
VALID_PASSWORD = "Test123!"


def test_successful_login(driver):
    driver.get(f"{BASE_URL}/login")

    driver.find_element(By.ID, "username").send_keys(VALID_LOGIN)
    driver.find_element(By.NAME, "password").send_keys(VALID_PASSWORD)
    driver.find_element(By.ID, "login-btn").click()

    logout = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "logout"))
    )
    assert logout.text == "Logout"
    assert driver.current_url.endswith("/dashboard")
    assert "Добро пожаловать, student!" in driver.find_element(By.ID, "welcome").text
