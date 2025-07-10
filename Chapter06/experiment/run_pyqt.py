import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap, QFont
from PyQt6.QtCore import Qt


class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.createSampleImage()

    def initUI(self):
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

    def createSampleImage(self):
        """Create a sample RGB image as numpy array"""
        # Create a colorful gradient image
        height, width = 400, 600
        self.rgb_array = np.zeros((height, width, 3), dtype=np.uint8)

        # Create a colorful pattern
        for y in range(height):
            for x in range(width):
                self.rgb_array[y, x, 0] = (x * 255) // width  # Red gradient
                self.rgb_array[y, x, 1] = (y * 255) // height  # Green gradient
                self.rgb_array[y, x, 2] = ((x + y) * 255) // (width + height)  # Blue gradient

        self.displayImage()

    def displayImage(self):
        """Convert numpy array to QPixmap and display"""
        height, width, channels = self.rgb_array.shape

        # Convert numpy array to QImage
        qimage = QImage(self.rgb_array.data, width, height, width * channels, QImage.Format.Format_RGB888)

        # Convert to QPixmap and display
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)

    def keyPressEvent(self, event):
        """Handle keyboard input"""
        key = event.key()

        if key == Qt.Key.Key_R:
            self.adjustColor(0, 20)  # Increase red
            self.info_label.setText("Red channel increased")
        elif key == Qt.Key.Key_G:
            self.adjustColor(1, 20)  # Increase green
            self.info_label.setText("Green channel increased")
        elif key == Qt.Key.Key_B:
            self.adjustColor(2, 20)  # Increase blue
            self.info_label.setText("Blue channel increased")
        elif key == Qt.Key.Key_1:
            self.adjustColor(0, -20)  # Decrease red
            self.info_label.setText("Red channel decreased")
        elif key == Qt.Key.Key_2:
            self.adjustColor(1, -20)  # Decrease green
            self.info_label.setText("Green channel decreased")
        elif key == Qt.Key.Key_3:
            self.adjustColor(2, -20)  # Decrease blue
            self.info_label.setText("Blue channel decreased")
        elif key == Qt.Key.Key_Space:
            self.createSampleImage()
            self.info_label.setText("Image reset to original")
        elif key == Qt.Key.Key_I:
            self.invertImage()
            self.info_label.setText("Image inverted")
        elif key == Qt.Key.Key_N:
            self.addNoise()
            self.info_label.setText("Noise added to image")
        elif key == Qt.Key.Key_C:
            self.clearImage()
            self.info_label.setText("Image cleared (black)")
        elif key == Qt.Key.Key_H:
            self.showHelp()
        else:
            self.info_label.setText(f"Key pressed: {event.text()} (Press H for help)")

    def adjustColor(self, channel, amount):
        """Adjust specific color channel"""
        self.rgb_array[:, :, channel] = np.clip(
            self.rgb_array[:, :, channel].astype(int) + amount, 0, 255
        ).astype(np.uint8)
        self.displayImage()

    def invertImage(self):
        """Invert the image colors"""
        self.rgb_array = 255 - self.rgb_array
        self.displayImage()

    def addNoise(self):
        """Add random noise to the image"""
        noise = np.random.randint(-30, 30, self.rgb_array.shape, dtype=int)
        self.rgb_array = np.clip(self.rgb_array.astype(int) + noise, 0, 255).astype(np.uint8)
        self.displayImage()

    def clearImage(self):
        """Clear the image to black"""
        self.rgb_array.fill(0)
        self.displayImage()

    def showHelp(self):
        """Show help information"""
        help_text = """
        Keyboard Controls:
        R - Increase red channel
        G - Increase green channel  
        B - Increase blue channel
        1 - Decrease red channel
        2 - Decrease green channel
        3 - Decrease blue channel
        SPACE - Reset image
        I - Invert colors
        N - Add noise
        C - Clear image (black)
        H - Show this help
        """
        self.info_label.setText(help_text.strip())


def main():
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()