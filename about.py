import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextBrowser, 
                            QFrame, QHBoxLayout, QPushButton)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap, QFont, QDesktopServices

class AboutWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Add title
        title = QLabel("About Blue Crab GIS")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Create content frame
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(10, 25, 41, 0.7);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 20px;
            }
        """)
        
        content_layout = QVBoxLayout(content_frame)
        
        # Header with logo and basic info
        header_layout = QHBoxLayout()
        
        # Logo
        logo_label = QLabel()
        logo_path = os.path.join('assets', 'blue_crab_logo.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            logo_label.setText("Logo")
            logo_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        
        logo_label.setFixedSize(150, 150)
        logo_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(logo_label)
        
        # Basic info
        info_layout = QVBoxLayout()
        
        app_name = QLabel("Blue Crab GIS")
        app_name.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        info_layout.addWidget(app_name)
        
        version = QLabel("Version 1.0.0")
        version.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 14px;")
        info_layout.addWidget(version)
        
        description = QLabel("Geographic Information System for Blue Crab Population Monitoring")
        description.setStyleSheet("color: white; font-size: 14px;")
        description.setWordWrap(True)
        info_layout.addWidget(description)
        
        info_layout.addStretch()
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        
        content_layout.addLayout(header_layout)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: rgba(255, 255, 255, 0.1);")
        content_layout.addWidget(separator)
        
        # Detailed information from about.txt
        self.text_browser = QTextBrowser()
        self.text_browser.setStyleSheet("""
            QTextBrowser {
                background-color: rgba(10, 25, 41, 0.5);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 5px;
                padding: 10px;
            }
            
            QTextBrowser a {
                color: #4a9cf5;
            }
        """)
        self.text_browser.setOpenExternalLinks(True)
        
        # Load content from about.txt
        self.load_about_content()
        
        content_layout.addWidget(self.text_browser)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        website_btn = QPushButton("Visit Website")
        website_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 102, 204, 0.7);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: rgba(0, 122, 244, 0.8);
            }
        """)
        website_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://example.com")))
        
        report_btn = QPushButton("Report Issue")
        report_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(204, 51, 0, 0.7);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: rgba(224, 71, 20, 0.8);
            }
        """)
        report_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://example.com/issues")))
        
        buttons_layout.addWidget(website_btn)
        buttons_layout.addWidget(report_btn)
        buttons_layout.addStretch()
        
        content_layout.addLayout(buttons_layout)
        
        layout.addWidget(content_frame)
    
    def load_about_content(self):
        """Load content from about.txt file"""
        about_path = 'about.txt'
        
        if os.path.exists(about_path):
            try:
                with open(about_path, 'r') as file:
                    content = file.read()
                    # Convert plain text to HTML
                    content = content.replace('\n', '<br>')
                    self.text_browser.setHtml(content)
            except Exception as e:
                self.text_browser.setHtml(f"<p>Error loading about.txt: {str(e)}</p>")
        else:
            # Default content if about.txt doesn't exist
            default_content = """
            <h2>Blue Crab GIS</h2>
            <p>A comprehensive Geographic Information System designed for monitoring and analyzing Blue Crab populations.</p>
            
            <h3>Features:</h3>
            <ul>
                <li>Interactive GIS mapping with multiple view options</li>
                <li>Data analytics with charts and visualizations</li>
                <li>Dataset management and filtering</li>
                <li>CSV import and manual data entry</li>
                <li>Customizable settings</li>
            </ul>
            
            <h3>Developer Information:</h3>
            <p>This application was developed as a tool for marine biologists and environmental researchers to track and analyze Blue Crab populations.</p>
            
            <p><b>Note:</b> You can customize this information by editing the about.txt file.</p>
            """
            self.text_browser.setHtml(default_content)