import sys

import cv2
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap, QFont
from PyQt6.QtCore import Qt, QTimer

import gymnasium as gym


class AtariViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()
        self.env = self.create_gym_env()
        self.action = 0

        self.timer = self.startTimer(1000 // 10)

        self.display_gym_frame()

    def init_UI(self):
        self.setWindowTitle('RGB Image Viewer - Press keys to interact')
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 2px solid gray;")
        layout.addWidget(self.image_label)

        # Create info label for keyboard feedback
        self.info_label = QLabel("Press keys to interact with the image")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setFont(QFont("Arial", 12))
        self.info_label.setStyleSheet("padding: 10px; background-color: #f0f0f0;")
        layout.addWidget(self.info_label)

        # Enable focus for keyboard events
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def create_gym_env(self):
        env_id = "PongNoFrameskip-v4"
        # env_id = "ALE/Pong-v5"
        env = gym.make(env_id, render_mode="rgb_array")
        print(f"{env.action_space=}")
        print(f"{env.observation_space=}")
        env.reset()
        return env

    def display_gym_frame(self):
        rgb_array = self.env.render()
        height, width, _ = rgb_array.shape
        rgb_array = cv2.resize(rgb_array, (width * 2, height * 2), interpolation=cv2.INTER_AREA)
        self.set_image(rgb_array)

    def set_image(self, rgb_array):
        """Convert numpy array to QPixmap and display"""
        print(f"{rgb_array.shape=}")
        height, width, channels = rgb_array.shape

        # Convert numpy array to QImage
        qimage = QImage(rgb_array.data, width, height, width * channels, QImage.Format.Format_RGB888)

        # Convert to QPixmap and display
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)

    def startTimer(self, interval):
        timer = QTimer()
        timer.timeout.connect(self.step)
        timer.start(interval)
        return timer

    def keyPressEvent(self, event):
        """Handle keyboard input"""
        key = event.key()

        print(f"Key pressed: {key}")
        self.info_label.setText(f"Key pressed: {key}")

        if key == Qt.Key.Key_1:
            self.action = 0
        elif key == Qt.Key.Key_2:
            self.action = 1
        elif key == Qt.Key.Key_3:
            self.action = 2
        elif key == Qt.Key.Key_4:
            self.action = 3
        elif key == Qt.Key.Key_5:
            self.action = 4
        elif key == Qt.Key.Key_6:
            self.action = 5

    def step(self):
        print(f"Step on action: {self.action}")
        self.env.step(self.action)
        self.action = 0

        self.display_gym_frame()

def main():
    app = QApplication(sys.argv)
    viewer = AtariViewer()
    viewer.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()