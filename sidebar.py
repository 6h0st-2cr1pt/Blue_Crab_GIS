from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QRadioButton, 
                            QButtonGroup, QSizePolicy, QSpacerItem)
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QFont, QIcon

class SidebarButton(QRadioButton):
    def __init__(self, text, icon_path=None, parent=None):
        super().__init__(text, parent)
        
        # Hide the bullet
        self.setStyleSheet("""
            QRadioButton {
                color: rgba(255, 255, 255, 0.7);
                background-color: transparent;
                border: none;
                padding: 10px 15px;
                font-size: 14px;
                font-weight: 500;
                text-align: left;
                border-radius: 8px;
            }
            
            QRadioButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
            }
            
            QRadioButton:checked {
                background-color: rgba(0, 102, 204, 0.3);
                color: white;
                border-left: 3px solid #0066cc;
            }
            
            QRadioButton::indicator {
                width: 0px;
                height: 0px;
            }
        """)
        
        # Set icon if provided
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(20, 20))  # Fixed: Using QSize directly instead of Qt.QSize

class Sidebar(QWidget):
    page_changed = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        
        # Set fixed width
        self.setFixedWidth(220)
        
        # Apply glassmorphism style
        self.setStyleSheet("""
            QWidget#sidebar {
                background-color: rgba(10, 25, 41, 0.8);
                border-right: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            QLabel#title {
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 20px 0px;
            }
        """)
        self.setObjectName("sidebar")
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(8)
        
        # Add title
        title = QLabel("Blue Crab GIS")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Add separator
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        separator.setStyleSheet("background-color: rgba(255, 255, 255, 0.1);")
        layout.addWidget(separator)
        layout.addSpacing(20)
        
        # Create button group
        self.button_group = QButtonGroup(self)
        self.button_group.buttonClicked.connect(self.on_button_clicked)
        
        # Add navigation buttons
        self.buttons = []
        
        # Dashboard button
        dashboard_btn = SidebarButton("Dashboard", "assets/icons/dashboard.png")
        layout.addWidget(dashboard_btn)
        self.button_group.addButton(dashboard_btn, 0)
        self.buttons.append(dashboard_btn)
        
        # GIS button
        gis_btn = SidebarButton("GIS", "assets/icons/map.png")
        layout.addWidget(gis_btn)
        self.button_group.addButton(gis_btn, 1)
        self.buttons.append(gis_btn)
        
        # Analytics button
        analytics_btn = SidebarButton("Analytics", "assets/icons/analytics.png")
        layout.addWidget(analytics_btn)
        self.button_group.addButton(analytics_btn, 2)
        self.buttons.append(analytics_btn)
        
        # Datasets button
        datasets_btn = SidebarButton("Datasets", "assets/icons/database.png")
        layout.addWidget(datasets_btn)
        self.button_group.addButton(datasets_btn, 3)
        self.buttons.append(datasets_btn)
        
        # Upload Data button
        upload_btn = SidebarButton("Upload Data", "assets/icons/upload.png")
        layout.addWidget(upload_btn)
        self.button_group.addButton(upload_btn, 4)
        self.buttons.append(upload_btn)
        
        # Add spacer
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Settings button
        settings_btn = SidebarButton("Settings", "assets/icons/settings.png")
        layout.addWidget(settings_btn)
        self.button_group.addButton(settings_btn, 5)
        self.buttons.append(settings_btn)
        
        # About button
        about_btn = SidebarButton("About", "assets/icons/info.png")
        layout.addWidget(about_btn)
        self.button_group.addButton(about_btn, 6)
        self.buttons.append(about_btn)
        
    def on_button_clicked(self, button):
        index = self.button_group.id(button)
        self.page_changed.emit(index)
        
    def select_page(self, index):
        if 0 <= index < len(self.buttons):
            self.buttons[index].setChecked(True)
            self.page_changed.emit(index)