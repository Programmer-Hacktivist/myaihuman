import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import QTimer
import math
import psutil

class JarvisHUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My AI Human HUD")
        self.setGeometry(200, 200, 500, 500)
        self.setStyleSheet("background-color: black;")

        self.angle = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)

    def update_animation(self):
        self.angle += 5
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Neon circle
        pen = QPen(QColor(0, 255, 255), 3)
        painter.setPen(pen)

        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = 150

        painter.drawEllipse(center_x - radius, center_y - radius, radius*2, radius*2)

        # Rotating line
        x = center_x + radius * math.cos(math.radians(self.angle))
        y = center_y + radius * math.sin(math.radians(self.angle))

        painter.drawLine(center_x, center_y, int(x), int(y))

        # System stats
        painter.setPen(QPen(QColor(0, 255, 0), 2))
        painter.drawText(10, 20, f"CPU: {psutil.cpu_percent()}%")
        painter.drawText(10, 40, f"RAM: {psutil.virtual_memory().percent}%")

def run_hud():
    app = QApplication(sys.argv)
    hud = JarvisHUD()
    hud.show()
    sys.exit(app.exec())
