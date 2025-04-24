import os
from PyQt5.QtWidgets import QSplashScreen, QProgressBar
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

class SplashScreen(QSplashScreen):
    splash_finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Load splash image
        splash_img = QPixmap(os.path.join('assets', 'blue_crab_logo.jpg'))
        if splash_img.isNull():
            # Fallback if image not found
            splash_img = QPixmap(400, 300)
            splash_img.fill(QColor(0, 51, 102))  # Dark blue
            
        self.setPixmap(splash_img.scaled(600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # Add progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(20, self.height() - 50, self.width() - 40, 20)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                background-color: rgba(0, 20, 40, 0.7);
                color: white;
                text-align: center;
            }
            
            QProgressBar::chunk {
                background-color: rgba(0, 102, 204, 0.8);
                border-radius: 5px;
            }
        """)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        
        # Set window flags
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(30)  # Update every 30ms
        self.progress = 0
        
    def update_progress(self):
        self.progress += 1
        self.progress_bar.setValue(self.progress)
        
        if self.progress >= 100:
            self.timer.stop()
            self.splash_finished.emit()
            self.close()
            
    def mousePressEvent(self, event):
        # Allow click to skip splash screen
        self.timer.stop()
        self.splash_finished.emit()
        self.close()