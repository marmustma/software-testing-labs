#!/usr/bin/env bash
# Запуск Appium-сервера и мобильных тестов на уже запущенном эмуляторе Android
set -u
mkdir -p screenshots
adb wait-for-device
{
  echo "Модель: $(adb shell getprop ro.product.model)"
  echo "Android: $(adb shell getprop ro.build.version.release) (API $(adb shell getprop ro.build.version.sdk))"
  echo "ABI: $(adb shell getprop ro.product.cpu.abi)"
  echo "Экран: $(adb shell wm size | tr -d '\r')"
} | tee screenshots/device.txt

appium --version | tee screenshots/appium_version.txt
appium --log screenshots/appium.log --log-level info &
APPIUM_PID=$!
for i in $(seq 1 30); do
  curl -s http://127.0.0.1:4723/status >/dev/null && break
  sleep 2
done
curl -s http://127.0.0.1:4723/status | tee screenshots/appium_status.json; echo

export APK_PATH="$PWD/NotesApp/app/build/outputs/apk/debug/app-debug.apk"
python -m pytest -v tests/ 2>&1 | tee screenshots/pytest_appium.txt
TEST_RC=${PIPESTATUS[0]}
python checklist_run.py 2>&1 | tee screenshots/checklist.txt
kill $APPIUM_PID || true
exit $TEST_RC
