import os
import time
import unittest,time


def user_launch():
    os.system("adb shell am start -a android.settings.SETTINGS")
    os.system("adb shell input tap 195 109")
    os.system("adb shell input text users")
    for i in range(0,4):
        if(i==2):
            os.system("adb shell input keyevent 20")
        os.system("adb shell input keyevent 66")
    time.sleep(5)
def kill_settings():
    os.system("adb shell am force-stop com.android.settings")

kill_settings()
user_launch()
