import sys
import math
import psutil
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtCore import QTimer


class JarvisHUD(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My AI Human HUD")
        self.setGeometry(200, 200, 600, 600)
        self.setStyleSheet("background-color: black;")

        # Animation
        self.angle = 0

        # AI state display
        self.current_thought = "Idle..."
        self.current_action = "-"
        self.current_result = "-"

        # Voice waveform simulation
        self.wave = [0] * 50

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)

    # =========================
    # 🔄 UPDATE HUD DATA (called externally)
    # =========================
    def update_state(self, thought=None, action=None, result=None):
        if thought:
            self.current_thought = thought
        if action:
            self.current_action = action
        if result:
            self.current_result = result

    # =========================
    # 🔁 ANIMATION LOOP
    # =========================
    def update_animation(self):
        self.angle += 3

        # Fake waveform animation
        import random
        self.wave = self.wave[1:] + [random.randint(0, 20)]

        self.update()

    # =========================
    # 🎨 DRAW UI
    # =========================
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center_x = self.width() // 2
        center_y = self.height() // 2

        # 🔵 Neon Circle
        pen = QPen(QColor(0, 255, 255), 3)
        painter.setPen(pen)
        radius = 150
        painter.drawEllipse(center_x - radius, center_y - radius, radius*2, radius*2)

        # 🔄 Rotating Line
        x = center_x + radius * math.cos(math.radians(self.angle))
        y = center_y + radius * math.sin(math.radians(self.angle))
        painter.drawLine(center_x, center_y, int(x), int(y))

        # 📊 System Stats
        painter.setPen(QPen(QColor(0, 255, 0), 2))
        painter.setFont(QFont("Consolas", 10))

        painter.drawText(10, 20, f"CPU: {psutil.cpu_percent()}%")
        painter.drawText(10, 40, f"RAM: {psutil.virtual_memory().percent}%")

        # 🧠 AI Thought
        painter.setPen(QPen(QColor(0, 200, 255), 2))
        painter.drawText(10, 80, f"Thought: {self.current_thought[:50]}")

        # ⚙️ Action
        painter.setPen(QPen(QColor(255, 255, 0), 2))
        painter.drawText(10, 100, f"Action: {self.current_action}")

        # 📥 Result
        painter.setPen(QPen(QColor(255, 100, 100), 2))
        painter.drawText(10, 120, f"Result: {self.current_result[:50]}")

        # 🔊 Voice Waveform
        painter.setPen(QPen(QColor(0, 255, 255), 2))
        base_y = self.height() - 100

        for i, val in enumerate(self.wave):
            x = 10 + i * 10
            painter.drawLine(x, base_y, x, base_y - val)


# =========================
# 🚀 RUN HUD
# =========================
def start_hud():
    app = QApplication(sys.argv)
    hud = JarvisHUD()
    hud.show()
    return app, hud
