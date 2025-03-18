import platform
import time
import json

import pyautogui
import cv2


def get_config():
    print("开始获取相关配置")
    #获取操作系统，如果为苹果系统则默认视为开启了Retina高分辨率，即将缩放调整为2倍
    system = platform.system()
    scaling = 1
    if system == "Windows":
        print("电脑系统：Windows")
        print(f"缩放倍数设置为：{scaling}")
    if system == "Darwin":
        print("电脑系统：Darwin(MacOS)，如果您手动关闭过Retina屏幕高分辨率模式请将其打开，否则可能会导致匹配出错！")
        scaling = 2
        print(f"缩放倍数设置为：{scaling}")
    if system == "Linux":
        print("电脑系统: Linux,尚未经过测试，如出现问题请将提issue")
        print(f"缩放倍数设置为：{scaling}")
    #获取并计算出计算机屏幕的物理分辨率
    screen_height, screen_width = pyautogui.size()
    screen_height *= scaling
    screen_width *= scaling
    print(f"显示器分辨率为：{screen_height} x {screen_width}")
    print("十秒后开始获取关键位置信息，请单击指尖派小程序以确保处于被选中的前台状态")
    time.sleep(9)
    # 重启小程序
    restart_mp(scaling)
    screenshot = pyautogui.screenshot()
    screenshot.save(f"static/screenshot/screenshot.png")
    #处理为灰度图
    screenshot = cv2.imread(f"static/screenshot/screenshot.png")
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template = cv2.imread("static/template/button_face.png")
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    #进行模版匹配
    match = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
    #计算矩形框
    x1, y1 = min_loc
    h, w = template.shape[:2]
    x2, y2 = x1 + w, y1 + h
    #点击
    pyautogui.click((x1 + x2) / 2 / scaling, (y1 + y2) / 2 / scaling)

    time.sleep(1)
    screenshot = pyautogui.screenshot()
    screenshot.save(f"static/screenshot/screenshot.png")
    #处理为灰度图
    screenshot = cv2.imread(f"static/screenshot/screenshot.png")
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template = cv2.imread("static/template/button_setting.png")
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    #进行模版匹配
    match = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
    #计算矩形框
    x1, y1 = min_loc
    h, w = template.shape[:2]
    x2, y2 = x1 + w, y1 + h
    #点击
    pyautogui.click((x1 + x2) / 2 / scaling, (y1 + y2) / 2 / scaling)
    #移开鼠标以便于对比
    pyautogui.moveTo(5,5)
    time.sleep(1)
    screenshot = pyautogui.screenshot()
    screenshot.save(f"static/screenshot/screenshot.png")
    #处理为灰度图
    screenshot = cv2.imread(f"static/screenshot/screenshot.png")
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template = cv2.imread("static/template/screen_setting.png")
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    #进行模版匹配
    match = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
    #计算矩形框
    x1, y1 = min_loc
    h, w = template.shape[:2]
    x2, y2 = x1 + w, y1 + h
    #点击
    pyautogui.click((x1 + x2) / 2 / scaling, (y1 + y2) / 2 / scaling)
    screenshot_range = [x1, y1, x2, y2]
    print(f"指尖派运行范围为：{screenshot_range}")
    #写入配置
    config = {
        "system":system,
        "scaling": scaling,
        "screen_height": screen_height,
        "screen_width": screen_width,
        "screenshot_range": screenshot_range
    }

    # 将数据写入 JSON 文件
    with open("conf/config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

    print("数据已存储到 config.json")
    print("即将重启小程序，请勿移动小程序位置，也不要将其遮挡")
    restart_mp(scaling)

def restart_mp(scaling):
    time.sleep(1)
    #获取小程序位置范围以调整区域
    #重置小程序到一个稳定地扫描页面
    screenshot = pyautogui.screenshot()
    screenshot.save(f"static/screenshot/screenshot.png")
    #处理为灰度图
    screenshot = cv2.imread(f"static/screenshot/screenshot.png")
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template = cv2.imread("static/template/button_mp.png")
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    #进行模版匹配
    match = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
    #计算矩形框
    x1, y1 = min_loc
    h, w = template.shape[:2]
    x2, y2 = x1 + w, y1 + h
    #点击
    pyautogui.click((x1 + x2) / 2 / scaling, (y1 + y2) / 2 / scaling)
    #重启小程序以确定位置
    time.sleep(1)
    screenshot = pyautogui.screenshot()
    screenshot.save(f"static/screenshot/screenshot.png")
    #处理为灰度图
    screenshot = cv2.imread(f"static/screenshot/screenshot.png")
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template = cv2.imread("static/template/button_restart.png")
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    #进行模版匹配
    match = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
    #计算矩形框
    x1, y1 = min_loc
    h, w = template.shape[:2]
    x2, y2 = x1 + w, y1 + h
    #点击
    time.sleep(0.5)
    pyautogui.click((x1 + x2) / 2 / scaling, (y1 + y2) / 2 / scaling)
    time.sleep(1)

get_config()
