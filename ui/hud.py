import sys, math, psutil, random
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import QTimer

class JarvisHUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 600, 600)
        self.setStyleSheet("background:black")

        self.angle = 0
        self.thought = "Idle"
        self.action = "-"
        self.result = "-"
        self.wave = [0]*50

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_anim)
        self.timer.start(50)

    def update_state(self, t=None, a=None, r=None):
        if t: self.thought = t
        if a: self.action = a
        if r: self.result = r

    def update_anim(self):
        self.angle += 3
        self.wave = self.wave[1:] + [random.randint(0,20)]
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        cx, cy = self.width()//2, self.height()//2
        r = 150

        p.setPen(QPen(QColor(0,255,255),3))
        p.drawEllipse(cx-r, cy-r, r*2, r*2)

        x = cx + r*math.cos(math.radians(self.angle))
        y = cy + r*math.sin(math.radians(self.angle))
        p.drawLine(cx, cy, int(x), int(y))

        p.setPen(QPen(QColor(0,255,0)))
        p.drawText(10,20,f"CPU {psutil.cpu_percent()}%")

        p.drawText(10,60,f"T: {self.thought[:40]}")
        p.drawText(10,80,f"A: {self.action}")
        p.drawText(10,100,f"R: {self.result[:40]}")

def start_hud():
    app = QApplication(sys.argv)
    hud = JarvisHUD()
    hud.show()
    return app, hud
