from PyQt6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QTextEdit, QComboBox
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
        self.setGeometry(100, 100, 400, 350)

        layout = QVBoxLayout()

        # 日志窗口
        self.log_window = QTextEdit(self)
        self.log_window.setReadOnly(True)  # 只读
        layout.addWidget(self.log_window)

        # 模式选择
        self.mode_selector = QComboBox(self)
        self.mode_selector.addItems(["纯图像识别模式（高精准低速度）", "图像坐标混合模式（均衡精准和速度）", "纯坐标模式(低精准高速度)"])
        layout.addWidget(self.mode_selector)

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

        mode = self.mode_selector.currentText()  # 获取用户选择的模式
        mode_arg = {"纯图像识别模式（高精准低速度）": "image_mode", "图像坐标混合模式（均衡精准和速度）": "mix_mode", "纯坐标模式(低精准高速度)": "coordinate"}.get(mode, "mix_mode")

        self.log_message(f"已选择模式：{mode}")

        def run():
            # 启动 main.py 并传递模式参数
            self.process = subprocess.Popen(
                ["python3", "main.py", "--mode", mode_arg],
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
            self.process.terminate()
            self.process.wait()
            self.log_message("程序已被手动停止")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def get_config(self):
        """ 获取配置并显示 """
        self.log_window.clear()

        def run():
            process = subprocess.Popen(
                ["python3", "config.py"],
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