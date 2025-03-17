import json
import argparse

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
def image_mode():
    print("待完成")

#坐标匹配模式
def coordinate_mode():
    print("待完成")

#混合模式
def mix_mode():
    print("待完成")

#主函数
def main():
    print("正在加载配置")
    mode,system,scaling,screen_height,screen_width,screenshot_range = load_config()
    print(f"操作系统：{system}，屏幕缩放：{scaling}，屏幕分辨率：{screen_height} x {screen_width}，小程序运行范围：{screenshot_range}")
    print("配置加载完成，程序开始运行")



main()