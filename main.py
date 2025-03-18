import json
import argparse
import time

import cv2
import pyautogui


#根据模版图片与小程序运行区域截图比对,返回逻辑像素坐标
def match_with_image(scaling,template_path,screenshot_range):
    #对小程序运行范围内进行截图
    #得到物理坐标
    x1,y1,x2,y2 = screenshot_range
    #转化逻辑坐标
    x1 /= scaling
    a = int(x1)
    y1 /= scaling
    b = int(y1)
    x2 /= scaling
    y2 /= scaling
    width = int(abs(x2 - x1))  # 宽度
    height = int(abs(y2 - y1))  # 高度
    time.sleep(0.1)
    screenshot = pyautogui.screenshot(region=(a,b,width,height))
    screenshot.save(f"static/screenshot/screenshot.png")
    screenshot = cv2.imread(f"static/screenshot/screenshot.png")
    template = cv2.imread(template_path)
    h, w = template.shape[:2]
    # 计算新的尺寸
    new_size = (int(w / scaling), int(h / scaling))  # 缩小为原来的一半
    # 按新尺寸缩放模板图像
    template = cv2.resize(template, new_size)
    #进行模版匹配
    match = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
    #计算矩形框
    x1, y1 = min_loc
    h, w = template.shape[:2]
    x2, y2 = x1 + w, y1 + h
    coordinate = [int((x1 + a +x2 + a)/2), int((y1 + b+y2 + b)/2)]
    #返回逻辑坐标值
    return coordinate

#读取配置
def load_config():
    # 读取选择模式
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default="mix_mode", choices=["image_mode", "mix_mode", "coordinate"])
    args = parser.parse_args()
    mode = args.mode
    # 读取 JSON 文件
    with open("conf/config.json", "r", encoding="utf-8") as f:
       data = json.load(f)
    system = data["system"]
    scaling = data["scaling"]
    screen_height = data["screen_height"]
    screen_width = data["screen_width"]
    screenshot_range = data["screenshot_range"]
    return mode, system, scaling, screen_height, screen_width, screenshot_range
#图像匹配模式
def image_mode(scaling, screen_height, screen_width, screenshot_range):
    x1, y1, x2, y2 = screenshot_range
    x1 = int(x1/scaling)
    y1 = int(y1/scaling)
    x2 = int(x2/scaling)
    y2 = int(y2/scaling)
    pyautogui.click((x1+x2)/2,(y2+y1)/2 - 5)
    pyautogui.scroll(-1000)
    coordinate = match_with_image(scaling,"static/template/button_more.png",screenshot_range)
    pyautogui.click((coordinate[0],coordinate[1]))
    time.sleep(0.1)
    coordinate = match_with_image(scaling, "static/template/button_sort.png", screenshot_range)
    pyautogui.click((coordinate[0],coordinate[1]))
    coordinate = match_with_image(scaling, "static/template/button_sort_right.png", screenshot_range)
    pyautogui.click((coordinate[0],coordinate[1]))
    #进入活动报名
    coordinate = match_with_image(scaling, "static/template/button_signup_able.png", screenshot_range)
    pyautogui.click((coordinate[0],coordinate[1]))
    time.sleep(0.1)
    #进入三次确认
    coordinate = match_with_image(scaling, "static/template/button_signup_first.png", screenshot_range)
    pyautogui.click((coordinate[0],coordinate[1]))
    time.sleep(0.2)
    coordinate = match_with_image(scaling, "static/template/button_signup_second.png", screenshot_range)
    pyautogui.click((coordinate[0],coordinate[1]))
    pyautogui.click((coordinate[0],coordinate[1]))
    time.sleep(0.2)
    coordinate = match_with_image(scaling, "static/template/button_signup_third.png", screenshot_range)
    pyautogui.click((coordinate[0],coordinate[1]))
    time.sleep(0.1)
    pyautogui.click((coordinate[0],coordinate[1]))
    coordinate = match_with_image(scaling, "static/template/button_signup_third.png", screenshot_range)
    time.sleep(0.1)


#坐标匹配模式
def coordinate_mode(scaling, screen_height, screen_width, screenshot_range):
    print("坐标模式待完成")

#混合模式
def mix_mode(scaling, screen_height, screen_width, screenshot_range):
    print("混合模式待完成")

#主函数
def main():
    print("正在加载配置")
    mode,system,scaling,screen_height,screen_width,screenshot_range = load_config()
    print(f"操作系统：{system}，屏幕缩放：{scaling}，屏幕分辨率：{screen_height} x {screen_width}，小程序运行范围：{screenshot_range}")
    print("配置加载完成，程序开始运行")
    if mode == "image_mode":
        image_mode(scaling, screen_height, screen_width, screenshot_range)
    elif mode == "mix_mode":
        mix_mode(scaling, screen_height, screen_width, screenshot_range)
    elif mode == "coordinate":
        coordinate_mode(scaling, screen_height, screen_width, screenshot_range)


main()