from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
import sys
import psutil

class HUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My AI Human HUD")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.cpu_label = QLabel("CPU:")
        self.ram_label = QLabel("RAM:")
        self.status_label = QLabel("Status: Online")

        self.layout.addWidget(self.cpu_label)
        self.layout.addWidget(self.ram_label)
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)

    def update_stats(self):
        self.cpu_label.setText(f"CPU: {psutil.cpu_percent()}%")
        self.ram_label.setText(f"RAM: {psutil.virtual_memory().percent}%")

def run_hud():
    app = QApplication(sys.argv)
    hud = HUD()
    hud.show()
    sys.exit(app.exec())
