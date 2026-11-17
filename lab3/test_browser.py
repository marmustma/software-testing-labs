"""Задание 2: инициализация браузера, открытие страницы, закрытие браузера."""
from conftest import BASE_URL, create_driver


def test_open_and_close_browser():
    driver = create_driver()                 # инициализация Chrome через WebDriver
    driver.get(f"{BASE_URL}/login")          # открываем страницу
    assert "Вход в систему" in driver.page_source
    print("Открыта страница:", driver.current_url)
    driver.quit()                            # закрываем браузер
