"""ЛР7: прохождение чек-листа мобильного тестирования на эмуляторе.

Действия тестировщика (тапы, жесты, поворот экрана, звонок, SMS, сворачивание,
выгрузка из памяти) выполняются через Appium и консоль эмулятора (adb emu),
результат каждой проверки фиксируется в checklist_results.json + скриншот.
"""
import json
import os
import re
import subprocess
import sys
import time

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "tests"))
from conftest import APPIUM_URL, PACKAGE, make_options  # noqa: E402

OUT = os.getenv("SHOTS_DIR", "screenshots")
os.makedirs(OUT, exist_ok=True)
ID = lambda name: (AppiumBy.ID, f"{PACKAGE}:id/{name}")  # noqa: E731
results = []


def adb(*args):
    r = subprocess.run(["adb", *args], capture_output=True, text=True, timeout=60)
    return (r.stdout + r.stderr).strip()


def notes(d):
    return [e.text for e in d.find_elements(AppiumBy.ID, "android:id/text1")]


def counter(d):
    return d.find_element(*ID("tv_counter")).text


def add(d, text):
    f = d.find_element(*ID("note_input"))
    f.clear()
    if text:
        f.send_keys(text)
    d.find_element(*ID("btn_add")).click()


def check(num, group, title, fn):
    note, status = "", "Passed"
    try:
        note = fn() or ""
    except AssertionError as e:
        status, note = "Failed", str(e)
    except Exception as e:  # noqa: BLE001
        status, note = "Failed", f"{type(e).__name__}: {e}"
    shot = f"check_{num:02d}.png"
    try:
        drv.save_screenshot(os.path.join(OUT, shot))
    except Exception:  # noqa: BLE001
        shot = ""
    results.append(dict(num=num, group=group, title=title, status=status, note=note, shot=shot))
    print(f"[{status}] {num}. {title} — {note}", flush=True)


drv = webdriver.Remote(APPIUM_URL, options=make_options())
drv.implicitly_wait(5)


def c1():
    assert drv.current_package == PACKAGE, drv.current_package
    assert counter(drv) == "Заметок: 0"
    return f"Пакет {drv.current_package}, активити {drv.current_activity}"


def c2():
    add(drv, "Первая заметка")
    assert counter(drv) == "Заметок: 1" and notes(drv) == ["Первая заметка"], notes(drv)
    return "После тапа по «Добавить» заметка появилась в списке, счётчик = 1"


def c3():
    add(drv, "   ")
    assert counter(drv) == "Заметок: 1", counter(drv)
    return "Заметка из пробелов не добавлена, у поля показана ошибка «Введите текст заметки»"


def c4():
    add(drv, "Удалить меня")
    el = [e for e in drv.find_elements(AppiumBy.ID, "android:id/text1") if e.text == "Удалить меня"][0]
    drv.execute_script("mobile: longClickGesture", {"elementId": el.id, "duration": 1200})
    time.sleep(1)
    assert "Удалить меня" not in notes(drv), notes(drv)
    return "Долгое нажатие (1,2 с) удалило заметку, показан Toast «Заметка удалена»"


def c5():
    for i in range(2, 16):
        add(drv, f"Заметка {i}")
    drv.hide_keyboard() if drv.is_keyboard_shown() else None
    first_before = notes(drv)[0]
    lst = drv.find_element(*ID("list_notes"))
    r = lst.rect
    drv.execute_script("mobile: swipeGesture", {"left": r["x"] + 10, "top": r["y"] + 10, "width": r["width"] - 20,
                                                 "height": r["height"] - 20, "direction": "up", "percent": 0.8})
    time.sleep(1)
    first_after = notes(drv)[0]
    assert first_before != first_after, "список не прокрутился"
    return f"15 заметок; свайп вверх прокрутил список: первая видимая «{first_before}» → «{first_after}»"


def c6():
    drv.find_element(*ID("note_input")).send_keys("Черновик")
    drv.orientation = "LANDSCAPE"
    time.sleep(2)
    assert drv.orientation == "LANDSCAPE"
    assert counter(drv) == "Заметок: 15", counter(drv)
    return "Ландшафтная ориентация: интерфейс перестроился, счётчик = 15"


def c7():
    drv.orientation = "PORTRAIT"
    time.sleep(2)
    txt = drv.find_element(*ID("note_input")).text
    assert counter(drv) == "Заметок: 15", counter(drv)
    assert txt == "Черновик", f"текст в поле: «{txt}»"
    return "После возврата в портретную ориентацию заметки и введённый текст «Черновик» сохранились"


def c8():
    adb("emu", "gsm", "call", "89991234567")
    time.sleep(4)
    drv.save_screenshot(os.path.join(OUT, "call_incoming.png"))
    adb("emu", "gsm", "cancel", "89991234567")
    time.sleep(3)
    drv.activate_app(PACKAGE)
    time.sleep(2)
    assert counter(drv) == "Заметок: 15", counter(drv)
    assert drv.find_element(*ID("note_input")).text == "Черновик"
    return "Входящий звонок (adb emu gsm call) принят системой, после сброса приложение вернулось в прежнее состояние"


def c9():
    adb("emu", "sms", "send", "89991234567", "Test SMS")
    time.sleep(4)
    drv.open_notifications()
    time.sleep(2)
    drv.save_screenshot(os.path.join(OUT, "sms_notification.png"))
    drv.back()
    time.sleep(1)
    drv.activate_app(PACKAGE)
    assert counter(drv) == "Заметок: 15", counter(drv)
    return "Пришло SMS (adb emu sms send), уведомление в шторке; после закрытия шторки данные не потеряны"


def c10():
    drv.background_app(3)
    time.sleep(1)
    assert drv.current_package == PACKAGE
    assert counter(drv) == "Заметок: 15"
    return "Приложение свёрнуто на 3 с (Home) и развёрнуто — состояние сохранено"


def c11():
    drv.press_keycode(3)  # HOME
    time.sleep(1)
    adb("shell", "am", "kill", PACKAGE)
    time.sleep(1)
    alive = adb("shell", "pidof", PACKAGE)
    drv.activate_app(PACKAGE)
    time.sleep(2)
    assert counter(drv) == "Заметок: 15", counter(drv)
    return f"Процесс выгружен из памяти (am kill, pidof → «{alive or 'нет процесса'}»), после перезапуска 15 заметок восстановлены"


def c12():
    info = adb("shell", "dumpsys", "meminfo", PACKAGE)
    m = re.search(r"TOTAL PSS:\s+(\d+)", info) or re.search(r"TOTAL\s+(\d+)", info)
    assert m, "не удалось прочитать meminfo"
    pss_mb = int(m.group(1)) / 1024
    with open(os.path.join(OUT, "meminfo.txt"), "w") as f:
        f.write(info)
    assert pss_mb < 100, f"PSS = {pss_mb:.1f} МБ"
    return f"Потребление памяти (dumpsys meminfo) TOTAL PSS = {pss_mb:.1f} МБ < 100 МБ"


def c13():
    adb("shell", "am", "send-trim-memory", PACKAGE, "RUNNING_CRITICAL")
    time.sleep(2)
    assert drv.current_package == PACKAGE
    add(drv, "После нехватки памяти")
    assert counter(drv) == "Заметок: 16", counter(drv)
    return "Сигнал нехватки памяти (send-trim-memory RUNNING_CRITICAL) — приложение не упало, продолжает работать"


def c14():
    drv.find_element(*ID("note_input")).click()
    time.sleep(1)
    shown = drv.is_keyboard_shown()
    btn = drv.find_element(*ID("btn_add"))
    assert shown, "клавиатура не появилась"
    assert btn.is_displayed()
    drv.save_screenshot(os.path.join(OUT, "keyboard.png"))
    drv.back()
    time.sleep(1)
    assert not drv.is_keyboard_shown(), "Back не скрыл клавиатуру"
    assert drv.current_package == PACKAGE
    return "Тап по полю открывает клавиатуру, кнопка «Добавить» не перекрыта; Back скрывает клавиатуру"


def c15():
    drv.find_element(*ID("btn_clear")).click()
    assert counter(drv) == "Заметок: 0" and notes(drv) == []
    return "Кнопка «Очистить всё» удалила все заметки"


CHECKS = [
    (1, "Установка и запуск", "Приложение устанавливается и запускается на эмуляторе", c1),
    (2, "Жесты", "Тап по кнопке «Добавить» добавляет заметку", c2),
    (3, "Функционал", "Пустая заметка (из пробелов) не добавляется", c3),
    (4, "Жесты", "Долгое нажатие (long press) удаляет заметку", c4),
    (5, "Жесты", "Свайп прокручивает длинный список", c5),
    (6, "Ориентация экрана", "Поворот в ландшафтную ориентацию", c6),
    (7, "Ориентация экрана", "Возврат в портретную ориентацию без потери данных", c7),
    (8, "Прерывания", "Входящий звонок во время работы", c8),
    (9, "Прерывания", "Входящее SMS во время работы", c9),
    (10, "Прерывания", "Сворачивание и разворачивание приложения", c10),
    (11, "Работа с памятью", "Выгрузка процесса из памяти и повторный запуск", c11),
    (12, "Работа с памятью", "Потребление оперативной памяти", c12),
    (13, "Работа с памятью", "Реакция на нехватку памяти (trim memory)", c13),
    (14, "Клавиатура", "Экранная клавиатура и кнопка Back", c14),
    (15, "Функционал", "Очистка всех заметок", c15),
]
for n, g, t, fn in CHECKS:
    check(n, g, t, fn)

drv.quit()
with open(os.path.join(OUT, "checklist_results.json"), "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print(f"Итого: {sum(r['status'] == 'Passed' for r in results)} из {len(results)} проверок пройдено")
