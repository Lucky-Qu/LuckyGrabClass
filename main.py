import json

from mouseinfo import screenshot

#读取配置
def load_config():
    # 读取 JSON 文件
    with open("conf/config.json", "r", encoding="utf-8") as f:
       data = json.load(f)
    return data
#根据图像匹配点击
def click_with_template(template):
    print("待完成")

#根据坐标进行点击
def click_with_coordinate(coordinate):
    print("待完成")

#主函数
def main():
    print("正在加载配置")
    data = load_config()
    system = data["system"]
    scaling = data["scaling"]
    screen_height = data["screen_height"]
    screen_width = data["screen_width"]
    screenshot_range = data["screenshot_range"]
    print(f"操作系统：{system}，屏幕缩放：{scaling}，屏幕分辨率：{screen_height} x {screen_width}，小程序运行范围：{screenshot_range}")
    print("配置加载完成，程序开始运行")

main()