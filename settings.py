from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QComboBox, QCheckBox, QSlider,
                            QFrame, QFormLayout, QSpinBox, QMessageBox,
                            QColorDialog, QGroupBox)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QColor

from database import DatabaseManager

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize database manager
        self.db_manager = DatabaseManager()
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add title
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Create settings form
        settings_frame = QFrame()
        settings_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(10, 25, 41, 0.7);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 20px;
            }
        """)
        
        settings_layout = QVBoxLayout(settings_frame)
        
        # Appearance settings
        appearance_group = QGroupBox("Appearance")
        appearance_group.setStyleSheet("""
            QGroupBox {
                color: white;
                font-weight: bold;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        appearance_layout = QFormLayout(appearance_group)
        
        # Theme selector
        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark Blue", "Dark Green", "Dark Purple", "Dark Red"])
        self.theme_combo.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            padding: 8px;
        """)
        appearance_layout.addRow(theme_label, self.theme_combo)
        
        # Map style selector
        map_label = QLabel("Map Style:")
        self.map_combo = QComboBox()
        self.map_combo.addItems(["Dark", "Light", "Satellite", "Terrain"])
        self.map_combo.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            padding: 8px;
        """)
        appearance_layout.addRow(map_label, self.map_combo)
        
        # Font size
        font_label = QLabel("Font Size:")
        self.font_spin = QSpinBox()
        self.font_spin.setRange(8, 16)
        self.font_spin.setValue(12)
        self.font_spin.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            padding: 8px;
        """)
        appearance_layout.addRow(font_label, self.font_spin)
        
        # Accent color
        accent_label = QLabel("Accent Color:")
        self.accent_btn = QPushButton()
        self.accent_btn.setStyleSheet("""
            background-color: #0066cc;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            min-height: 30px;
        """)
        self.accent_btn.clicked.connect(self.choose_accent_color)
        appearance_layout.addRow(accent_label, self.accent_btn)
        
        settings_layout.addWidget(appearance_group)
        
        # Map settings
        map_group = QGroupBox("Map Settings")
        map_group.setStyleSheet("""
            QGroupBox {
                color: white;
                font-weight: bold;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        map_layout = QFormLayout(map_group)
        
        # Default zoom level
        zoom_label = QLabel("Default Zoom Level:")
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(1, 18)
        self.zoom_slider.setValue(10)
        self.zoom_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: #0066cc;
                border: 1px solid #0066cc;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            
            QSlider::sub-page:horizontal {
                background: rgba(0, 102, 204, 0.5);
                border-radius: 4px;
            }
        """)
        map_layout.addRow(zoom_label, self.zoom_slider)
        
        # Show population labels
        labels_label = QLabel("Show Population Labels:")
        self.labels_check = QCheckBox()
        self.labels_check.setChecked(True)
        self.labels_check.setStyleSheet("""
            QCheckBox {
                color: white;
            }
            
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 3px;
                background-color: rgba(255, 255, 255, 0.1);
            }
            
            QCheckBox::indicator:checked {
                background-color: rgba(0, 102, 204, 0.7);
                image: url(assets/icons/check.png);
            }
        """)
        map_layout.addRow(labels_label, self.labels_check)
        
        # Default view type
        view_label = QLabel("Default View Type:")
        self.view_combo = QComboBox()
        self.view_combo.addItems(["Markers", "Heat Map", "Clusters"])
        self.view_combo.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            padding: 8px;
        """)
        map_layout.addRow(view_label, self.view_combo)
        
        settings_layout.addWidget(map_group)
        
        # Application settings
        app_group = QGroupBox("Application Settings")
        app_group.setStyleSheet("""
            QGroupBox {
                color: white;
                font-weight: bold;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        app_layout = QFormLayout(app_group)
        
        # Default page
        page_label = QLabel("Default Page:")
        self.page_combo = QComboBox()
        self.page_combo.addItems(["Dashboard", "GIS", "Analytics", "Datasets", "Upload Data"])
        self.page_combo.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            padding: 8px;
        """)
        app_layout.addRow(page_label, self.page_combo)
        
        # Auto-refresh interval
        refresh_label = QLabel("Auto-refresh Interval (seconds):")
        self.refresh_spin = QSpinBox()
        self.refresh_spin.setRange(0, 60)
        self.refresh_spin.setValue(5)
        self.refresh_spin.setSpecialValueText("Off")
        self.refresh_spin.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            padding: 8px;
        """)
        app_layout.addRow(refresh_label, self.refresh_spin)
        
        # Show splash screen
        splash_label = QLabel("Show Splash Screen:")
        self.splash_check = QCheckBox()
        self.splash_check.setChecked(True)
        self.splash_check.setStyleSheet("""
            QCheckBox {
                color: white;
            }
            
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 3px;
                background-color: rgba(255, 255, 255, 0.1);
            }
            
            QCheckBox::indicator:checked {
                background-color: rgba(0, 102, 204, 0.7);
                image: url(assets/icons/check.png);
            }
        """)
        app_layout.addRow(splash_label, self.splash_check)
        
        settings_layout.addWidget(app_group)
        
        # Add buttons
        buttons_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.clicked.connect(self.save_settings)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 102, 204, 0.7);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: rgba(0, 122, 244, 0.8);
            }
        """)
        
        self.reset_btn = QPushButton("Reset to Default")
        self.reset_btn.clicked.connect(self.reset_settings)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(204, 51, 0, 0.7);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: rgba(224, 71, 20, 0.8);
            }
        """)
        
        buttons_layout.addWidget(self.reset_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_btn)
        
        settings_layout.addLayout(buttons_layout)
        
        layout.addWidget(settings_frame)
        
        # Load settings
        self.load_settings()
    
    def choose_accent_color(self):
        """Open color dialog to choose accent color"""
        current_color = self.accent_btn.palette().button().color()
        color = QColorDialog.getColor(current_color, self, "Choose Accent Color")
        
        if color.isValid():
            self.accent_btn.setStyleSheet(f"""
                background-color: {color.name()};
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                min-height: 30px;
            """)
    
    def load_settings(self):
        """Load settings from database"""
        # Theme
        theme = self.db_manager.get_setting('theme', 'dark')
        index = self.theme_combo.findText(theme.title(), Qt.MatchContains)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
        
        # Map style
        map_style = self.db_manager.get_setting('map_style', 'dark')
        index = self.map_combo.findText(map_style.title(), Qt.MatchContains)
        if index >= 0:
            self.map_combo.setCurrentIndex(index)
        
        # Font size
        font_size = int(self.db_manager.get_setting('font_size', '12'))
        self.font_spin.setValue(font_size)
        
        # Accent color
        accent_color = self.db_manager.get_setting('accent_color', '#0066cc')
        self.accent_btn.setStyleSheet(f"""
            background-color: {accent_color};
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            min-height: 30px;
        """)
        
        # Zoom level
        zoom_level = int(self.db_manager.get_setting('zoom_level', '10'))
        self.zoom_slider.setValue(zoom_level)
        
        # Show labels
        show_labels = self.db_manager.get_setting('show_labels', 'true') == 'true'
        self.labels_check.setChecked(show_labels)
        
        # Default view
        default_view = self.db_manager.get_setting('default_view', 'Markers')
        index = self.view_combo.findText(default_view, Qt.MatchExactly)
        if index >= 0:
            self.view_combo.setCurrentIndex(index)
        
        # Default page
        default_page = self.db_manager.get_setting('default_page', 'Dashboard')
        index = self.page_combo.findText(default_page, Qt.MatchExactly)
        if index >= 0:
            self.page_combo.setCurrentIndex(index)
        
        # Refresh interval
        refresh_interval = int(self.db_manager.get_setting('refresh_interval', '5'))
        self.refresh_spin.setValue(refresh_interval)
        
        # Show splash
        show_splash = self.db_manager.get_setting('show_splash', 'true') == 'true'
        self.splash_check.setChecked(show_splash)
    
    def save_settings(self):
        """Save settings to database"""
        try:
            # Theme
            self.db_manager.set_setting('theme', self.theme_combo.currentText().lower())
            
            # Map style
            self.db_manager.set_setting('map_style', self.map_combo.currentText().lower())
            
            # Font size
            self.db_manager.set_setting('font_size', str(self.font_spin.value()))
            
            # Accent color
            accent_color = self.accent_btn.palette().button().color().name()
            self.db_manager.set_setting('accent_color', accent_color)
            
            # Zoom level
            self.db_manager.set_setting('zoom_level', str(self.zoom_slider.value()))
            
            # Show labels
            self.db_manager.set_setting('show_labels', str(self.labels_check.isChecked()).lower())
            
            # Default view
            self.db_manager.set_setting('default_view', self.view_combo.currentText())
            
            # Default page
            self.db_manager.set_setting('default_page', self.page_combo.currentText())
            
            # Refresh interval
            self.db_manager.set_setting('refresh_interval', str(self.refresh_spin.value()))
            
            # Show splash
            self.db_manager.set_setting('show_splash', str(self.splash_check.isChecked()).lower())
            
            # Show success message
            self.show_success("Settings saved successfully! Restart the application for changes to take effect.")
            
        except Exception as e:
            self.show_error(f"Error saving settings: {str(e)}")
    
    def reset_settings(self):
        """Reset settings to default"""
        # Confirm reset
        confirm = QMessageBox()
        confirm.setIcon(QMessageBox.Warning)
        confirm.setWindowTitle("Confirm Reset")
        confirm.setText("Are you sure you want to reset all settings to default?")
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)
        confirm.setStyleSheet("""
            QMessageBox {
                background-color: #0a1929;
                color: white;
            }
            QPushButton {
                background-color: rgba(0, 102, 204, 0.7);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
        """)
        
        if confirm.exec_() == QMessageBox.Yes:
            try:
                # Reset to defaults
                default_settings = {
                    'theme': 'dark',
                    'map_style': 'dark',
                    'font_size': '12',
                    'accent_color': '#0066cc',
                    'zoom_level': '10',
                    'show_labels': 'true',
                    'default_view': 'Markers',
                    'default_page': 'Dashboard',
                    'refresh_interval': '5',
                    'show_splash': 'true'
                }
                
                # Save defaults to database
                for key, value in default_settings.items():
                    self.db_manager.set_setting(key, value)
                
                # Reload settings
                self.load_settings()
                
                # Show success message
                self.show_success("Settings reset to default successfully!")
                
            except Exception as e:
                self.show_error(f"Error resetting settings: {str(e)}")
    
    def show_error(self, message):
        """Show error message"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #0a1929;
                color: white;
            }
            QPushButton {
                background-color: rgba(0, 102, 204, 0.7);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
        """)
        msg_box.exec_()
    
    def show_success(self, message):
        """Show success message"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Success")
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #0a1929;
                color: white;
            }
            QPushButton {
                background-color: rgba(0, 102, 204, 0.7);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
        """)
        msg_box.exec_()