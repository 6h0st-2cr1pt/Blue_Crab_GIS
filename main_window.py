from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QWidget, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from sidebar import Sidebar
from dashboard import DashboardWidget
from gis import GISWidget
from analytics import AnalyticsWidget
from datasets import DatasetsWidget
from upload_data import UploadDataWidget
from settings import SettingsWidget
from about import AboutWidget
from styles import apply_glassmorphism_style

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Blue Crab GIS")
        self.setWindowIcon(QIcon("assets/icons/app_icon.png"))
        self.setMinimumSize(1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = Sidebar()
        
        # Create stacked widget for content pages
        self.content_stack = QStackedWidget()
        
        # Create all page widgets
        self.dashboard_widget = DashboardWidget()
        self.gis_widget = GISWidget()
        self.analytics_widget = AnalyticsWidget()
        self.datasets_widget = DatasetsWidget()
        self.upload_widget = UploadDataWidget()
        self.settings_widget = SettingsWidget()
        self.about_widget = AboutWidget()
        
        # Add widgets to stack
        self.content_stack.addWidget(self.dashboard_widget)
        self.content_stack.addWidget(self.gis_widget)
        self.content_stack.addWidget(self.analytics_widget)
        self.content_stack.addWidget(self.datasets_widget)
        self.content_stack.addWidget(self.upload_widget)
        self.content_stack.addWidget(self.settings_widget)
        self.content_stack.addWidget(self.about_widget)
        
        # Create content frame with glassmorphism effect
        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for full-size content
        content_layout.setSpacing(0)  # Remove spacing
        content_layout.addWidget(self.content_stack)
        
        # Apply glassmorphism style to content frame
        apply_glassmorphism_style(content_frame)
        
        # Add widgets to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(content_frame)
        main_layout.setStretch(1, 1)  # Make content area expandable
        
        # Connect sidebar signals
        self.sidebar.page_changed.connect(self.change_page)
        
        # Set initial page
        self.sidebar.select_page(0)  # Dashboard
        
        # Apply stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a1929;
            }
        """)
        
    def change_page(self, index):
        self.content_stack.setCurrentIndex(index)