import time
from PyQt6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QTextEdit
import sys
import subprocess
import threading


class Launcher(QWidget):
    def __init__(self):
        super().__init__()
        self.process = None  # 记录运行的进程
        self.initUI()

    def initUI(self):
        self.setWindowTitle("抢课程序v4--Developed by LuckyQu")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # 日志窗口
        self.log_window = QTextEdit(self)
        self.log_window.setReadOnly(True)  # 只读
        layout.addWidget(self.log_window)

        # 启动按钮
        self.start_button = QPushButton("启动程序", self)
        self.start_button.clicked.connect(self.start_program)
        layout.addWidget(self.start_button)

        # 停止按钮
        self.stop_button = QPushButton("停止程序", self)
        self.stop_button.clicked.connect(self.stop_program)
        self.stop_button.setEnabled(False)  # 初始状态不可用
        layout.addWidget(self.stop_button)

        # 获取配置按钮
        self.get_config_button = QPushButton("获取配置", self)
        self.get_config_button.clicked.connect(self.get_config)
        layout.addWidget(self.get_config_button)

        self.setLayout(layout)

    def log_message(self, message):
        """ 在日志窗口显示信息 """
        self.log_window.append(message)

    def start_program(self):
        """ 启动 main.py 并读取日志 """
        self.log_window.clear()
        self.log_message("本项目完全开源，项目地址https://github.com/Lucky-Qu/LuckyGrabClass，如遇问题可提issue")
        self.log_message("在程序运行过程中，除需要终止程序，请不要操作鼠标或键盘，以防误触")
        self.log_message("请确保课堂派在前台可视区域运行")
        self.log_message("程序正在启动")

        def run():
            # 启动 main.py
            self.process = subprocess.Popen(
                ["python3", "main.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            self.start_button.setEnabled(False)  # 禁用启动按钮
            self.stop_button.setEnabled(True)  # 启用停止按钮

            for line in self.process.stdout:
                self.log_message(line.strip())

            self.process.wait()
            self.log_message("程序已运行结束，希望你抢到了想要的课！")

            self.start_button.setEnabled(True)  # 重新启用启动按钮
            self.stop_button.setEnabled(False)  # 禁用停止按钮

        thread = threading.Thread(target=run)
        thread.start()

    def stop_program(self):
        """ 终止运行中的程序 """
        if self.process:
            self.log_message("正在停止程序...")
            self.process.terminate()  # 终止进程
            self.process.wait()  # 等待进程完全退出
            self.log_message("程序已被手动停止")
            self.start_button.setEnabled(True)  # 重新启用启动按钮
            self.stop_button.setEnabled(False)  # 禁用停止按钮

    def get_config(self):
        """ 获取配置并显示 """
        self.log_window.clear()

        # 启动 config.py
        def run():
            process = subprocess.Popen(
                ["python3", "config.py"],  # 运行 config.py
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            for line in process.stdout:
                self.log_message(line.strip())

            process.wait()
            self.log_message("关键数据已获取并存储，检查无误后即可点击开始抢课")

        thread = threading.Thread(target=run)
        thread.start()


app = QApplication(sys.argv)
window = Launcher()
window.show()
sys.exit(app.exec())