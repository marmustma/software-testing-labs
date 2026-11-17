import os

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

APPIUM_URL = os.getenv("APPIUM_URL", "http://127.0.0.1:4723")
APK = os.getenv("APK_PATH", os.path.abspath("NotesApp/app/build/outputs/apk/debug/app-debug.apk"))
PACKAGE = "ru.mospolytech.notes"


def make_options(no_reset=False):
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "Android Emulator"
    options.app = APK
    options.app_package = PACKAGE
    options.app_activity = ".MainActivity"
    options.no_reset = no_reset
    options.new_command_timeout = 300
    options.set_capability("appium:uiautomator2ServerLaunchTimeout", 120000)
    options.set_capability("appium:adbExecTimeout", 120000)
    return options


@pytest.fixture
def driver():
    drv = webdriver.Remote(APPIUM_URL, options=make_options())
    drv.implicitly_wait(5)
    yield drv
    drv.quit()
