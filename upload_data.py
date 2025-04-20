from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QFileDialog, QLineEdit, QFormLayout, QMessageBox, 
                            QTabWidget, QFrame, QSpinBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt, pyqtSlot

from database import DatabaseManager

class UploadDataWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize database manager
        self.db_manager = DatabaseManager()
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add title
        title = QLabel("Upload Blue Crab Population Data")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Create tab widget
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(255, 255, 255, 0.1);
                background-color: rgba(10, 25, 41, 0.7);
                border-radius: 10px;
            }
            
            QTabBar::tab {
                background-color: rgba(0, 51, 102, 0.7);
                color: white;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                padding: 8px 15px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background-color: rgba(0, 102, 204, 0.7);
            }
            
            QTabBar::tab:hover {
                background-color: rgba(0, 122, 244, 0.8);
            }
        """)
        
        # Create CSV upload tab
        csv_tab = QWidget()
        csv_layout = QVBoxLayout(csv_tab)
        
        # CSV upload instructions
        instructions = QLabel("Upload a CSV file with the following columns: ID, Population, Latitude, Longitude")
        instructions.setStyleSheet("color: white; margin-bottom: 15px;")
        csv_layout.addWidget(instructions)
        
        # File selection
        file_frame = QFrame()
        file_layout = QHBoxLayout(file_frame)
        
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Select a CSV file...")
        self.file_path.setReadOnly(True)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_file)
        
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(browse_btn)
        
        csv_layout.addWidget(file_frame)
        
        # Upload button
        upload_btn = QPushButton("Upload CSV")
        upload_btn.clicked.connect(self.upload_csv)
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 102, 204, 0.7);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: rgba(0, 122, 244, 0.8);
            }
        """)
        
        csv_layout.addWidget(upload_btn)
        csv_layout.addStretch()
        
        # Create manual entry tab
        manual_tab = QWidget()
        manual_layout = QVBoxLayout(manual_tab)
        
        # Form for manual entry
        form_frame = QFrame()
        form_layout = QFormLayout(form_frame)
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        # ID field
        self.id_input = QSpinBox()
        self.id_input.setRange(1, 9999999)
        self.id_input.setStyleSheet("""
            QSpinBox {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                padding: 8px;
            }
        """)
        form_layout.addRow("ID:", self.id_input)
        
        # Population field
        self.population_input = QSpinBox()
        self.population_input.setRange(1, 1000000)
        self.population_input.setStyleSheet("""
            QSpinBox {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                padding: 8px;
            }
        """)
        form_layout.addRow("Population:", self.population_input)
        
        # Latitude field
        self.latitude_input = QDoubleSpinBox()
        self.latitude_input.setRange(-90, 90)
        self.latitude_input.setDecimals(6)
        self.latitude_input.setStyleSheet("""
            QDoubleSpinBox {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                padding: 8px;
            }
        """)
        form_layout.addRow("Latitude:", self.latitude_input)
        
        # Longitude field
        self.longitude_input = QDoubleSpinBox()
        self.longitude_input.setRange(-180, 180)
        self.longitude_input.setDecimals(6)
        self.longitude_input.setStyleSheet("""
            QDoubleSpinBox {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                padding: 8px;
            }
        """)
        form_layout.addRow("Longitude:", self.longitude_input)
        
        manual_layout.addWidget(form_frame)
        
        # Submit button
        submit_btn = QPushButton("Submit Data")
        submit_btn.clicked.connect(self.submit_manual_data)
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 102, 204, 0.7);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: rgba(0, 122, 244, 0.8);
            }
        """)
        
        manual_layout.addWidget(submit_btn)
        manual_layout.addStretch()
        
        # Add tabs to tab widget
        tab_widget.addTab(csv_tab, "CSV Upload")
        tab_widget.addTab(manual_tab, "Manual Entry")
        
        layout.addWidget(tab_widget)
        
    def browse_file(self):
        """Open file dialog to select CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            self.file_path.setText(file_path)
    
    def upload_csv(self):
        """Upload CSV file to database"""
        file_path = self.file_path.text()
        
        if not file_path:
            self.show_error("Please select a CSV file first.")
            return
        
        # Import CSV
        success = self.db_manager.import_csv(file_path)
        
        if success:
            self.show_success("CSV data imported successfully!")
            self.file_path.clear()
        else:
            self.show_error("Failed to import CSV data. Check the file format.")
    
    def submit_manual_data(self):
        """Submit manually entered data"""
        crab_id = self.id_input.value()
        population = self.population_input.value()
        latitude = self.latitude_input.value()
        longitude = self.longitude_input.value()
        
        # Validate data
        if crab_id <= 0:
            self.show_error("ID must be a positive number.")
            return
        
        if population <= 0:
            self.show_error("Population must be a positive number.")
            return
        
        # Insert data
        success = self.db_manager.insert_crab_data(crab_id, population, latitude, longitude)
        
        if success:
            self.show_success("Data submitted successfully!")
            self.reset_form()
        else:
            self.show_error("Failed to submit data. Please try again.")
    
    def reset_form(self):
        """Reset form fields"""
        self.id_input.setValue(self.id_input.minimum())
        self.population_input.setValue(self.population_input.minimum())
        self.latitude_input.setValue(0)
        self.longitude_input.setValue(0)
    
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