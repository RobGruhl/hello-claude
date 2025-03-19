#!/usr/bin/env python3
import sys
from typing import List, Optional

from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtCore import Qt


class GradientButton(QtWidgets.QPushButton):
    def __init__(self, text: str, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(text, parent)
        self.setFixedSize(200, 60)
        font = QtGui.QFont("Arial", 12, QtGui.QFont.Bold)
        self.setFont(font)
        self.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(
            """
            QPushButton {
                border-radius: 30px;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ff5f6d, stop:1 #ffc371
                );
            }
            QPushButton:pressed {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #fc466b, stop:1 #3f5efb
                );
            }
            """
        )
        self._animation = QtCore.QVariantAnimation()
        self._animation.setStartValue(0.0)
        self._animation.setEndValue(1.0)
        self._animation.setDuration(1000)
        self._animation.valueChanged.connect(self.update)
        self._animation.start()
        
    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        progress = self._animation.currentValue()
        gradient = QtGui.QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QtGui.QColor(252, 70, 107))
        gradient.setColorAt(1, QtGui.QColor(63, 94, 251))
        
        brush = QtGui.QBrush(gradient)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 30, 30)
        
        painter.setPen(QtGui.QColor(255, 255, 255))
        painter.drawText(event.rect(), Qt.AlignCenter, self.text())


class FloatingText(QtWidgets.QLabel):
    def __init__(self, text: str, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(text, parent)
        font = QtGui.QFont("Arial", 24, QtGui.QFont.Bold)
        self.setFont(font)
        self.setStyleSheet("color: white; background-color: transparent;")
        
        self._animation = QtCore.QPropertyAnimation(self, b"pos")
        self._animation.setDuration(2000)
        self._animation.setLoopCount(-1)  # Infinite loop
        self._animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        
    def start_animation(self, start_pos: QtCore.QPoint, end_pos: QtCore.QPoint) -> None:
        self._animation.setStartValue(start_pos)
        self._animation.setEndValue(end_pos)
        self._animation.start()


class ParticleSystem(QtWidgets.QWidget):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        
        self._particles: List[dict] = []
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.update_particles)
        self._timer.start(16)  # ~60 FPS
        
    def add_particles(self, x: int, y: int, count: int = 30) -> None:
        for _ in range(count):
            angle = QtCore.QRandomGenerator.global_().bounded(360) * 3.14159 / 180
            speed = QtCore.QRandomGenerator.global_().bounded(1, 5)
            size = QtCore.QRandomGenerator.global_().bounded(5, 15)
            lifetime = QtCore.QRandomGenerator.global_().bounded(20, 60)
            color = QtGui.QColor(
                QtCore.QRandomGenerator.global_().bounded(150, 255),
                QtCore.QRandomGenerator.global_().bounded(150, 255),
                QtCore.QRandomGenerator.global_().bounded(150, 255),
            )
            
            self._particles.append({
                "x": x,
                "y": y,
                "vx": speed * QtCore.qCos(angle),
                "vy": speed * QtCore.qSin(angle),
                "size": size,
                "lifetime": lifetime,
                "max_lifetime": lifetime,
                "color": color,
            })
    
    def update_particles(self) -> None:
        if not self._particles:
            return
            
        for particle in self._particles:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["vy"] += 0.1  # Gravity
            particle["lifetime"] -= 1
        
        self._particles = [p for p in self._particles if p["lifetime"] > 0]
        self.update()
    
    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        if not self._particles:
            return
            
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        for particle in self._particles:
            opacity = particle["lifetime"] / particle["max_lifetime"]
            color = particle["color"]
            color.setAlphaF(opacity)
            
            painter.setBrush(QtGui.QBrush(color))
            painter.setPen(Qt.NoPen)
            
            size = particle["size"] * opacity
            painter.drawEllipse(
                QtCore.QRectF(
                    particle["x"] - size/2,
                    particle["y"] - size/2,
                    size,
                    size
                )
            )


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Hello Claude!")
        self.resize(800, 600)
        
        # Create the central widget and layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        
        # Create the particle system
        self.particles = ParticleSystem(self)
        self.particles.setGeometry(0, 0, 800, 600)
        
        # Create the floating text
        self.floating_text = FloatingText("Hello, Claude!")
        layout.addWidget(self.floating_text)
        layout.addSpacing(50)
        
        # Create the button
        self.button = GradientButton("Click Me!")
        self.button.clicked.connect(self.on_button_clicked)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)
        
        # Set background gradient
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #12c2e9, stop:0.5 #c471ed, stop:1 #f64f59
                );
            }
            """
        )
        
        # Start the text animation after a short delay
        QtCore.QTimer.singleShot(100, self.start_animations)
    
    def start_animations(self) -> None:
        start_pos = QtCore.QPoint(self.width() // 2 - 100, 100)
        end_pos = QtCore.QPoint(self.width() // 2 - 100, 150)
        self.floating_text.start_animation(start_pos, end_pos)
    
    def on_button_clicked(self) -> None:
        # Add particles at the button position
        btn_pos = self.button.mapTo(self, QtCore.QPoint(self.button.width() // 2, self.button.height() // 2))
        self.particles.add_particles(btn_pos.x(), btn_pos.y())
        
        # Change the text temporarily
        original_text = self.floating_text.text()
        self.floating_text.setText("Wow, That's Cool!")
        QtCore.QTimer.singleShot(2000, lambda: self.floating_text.setText(original_text))


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
