import platform

import pyautogui


def get_config():
    print("开始获取相关配置")
    #获取操作系统，如果为苹果系统则默认视为开启了Retina高分辨率，即将缩放调整为2倍
    system = platform.system()
    scaling = 1
    if system == "Windows":
        print("电脑系统：Windows")
        print(f"缩放倍数设置为：{scaling}")
    if system == "Darwin":
        print("电脑系统：MacOS，如果您手动关闭过Retina屏幕高分辨率模式请将其打开，否则可能会导致匹配出错！")
        scaling = 2
        print(f"缩放倍数设置为：{scaling}")
    if system == "Linux":
        print("电脑系统: Linux,尚未经过测试，如出现问题请将提issue")
        print(f"缩放倍数设置为：{scaling}")
    screen_height, screen_width = pyautogui.size()
    screen_height *= scaling
    screen_width *= scaling
    print(f"显示器分辨率为：{screen_height} x {screen_width}")

get_config()