"""ЛР7: запуск приложения на эмуляторе и одно простое действие — тап по кнопке «Добавить»."""
import os

from appium.webdriver.common.appiumby import AppiumBy

SHOTS = os.getenv("SHOTS_DIR", "screenshots")


def test_tap_add_button(driver):
    os.makedirs(SHOTS, exist_ok=True)
    # приложение запущено Appium на эмуляторе
    assert driver.current_package == "ru.mospolytech.notes"
    counter = driver.find_element(AppiumBy.ID, "ru.mospolytech.notes:id/tv_counter")
    assert counter.text == "Заметок: 0"

    driver.find_element(AppiumBy.ID, "ru.mospolytech.notes:id/note_input").send_keys("Купить молоко")
    driver.find_element(AppiumBy.ID, "ru.mospolytech.notes:id/btn_add").click()   # тап по кнопке

    assert counter.text == "Заметок: 1"
    items = driver.find_elements(AppiumBy.ID, "android:id/text1")
    assert [i.text for i in items] == ["Купить молоко"]
    driver.save_screenshot(os.path.join(SHOTS, "appium_tap.png"))
