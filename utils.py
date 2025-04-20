import os
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal

class ErrorHandler(QObject):
    """Utility class for handling errors and showing notifications"""
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
    def show_error(self, message, title="Error"):
        """Show error message box"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
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
        
        # Emit signal for logging
        self.error_occurred.emit(message)
    
    def show_info(self, message, title="Information"):
        """Show information message box"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
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
    
    def show_warning(self, message, title="Warning"):
        """Show warning message box"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
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
    
    def show_confirm(self, message, title="Confirm"):
        """Show confirmation message box, returns True if Yes clicked"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
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
        
        return msg_box.exec_() == QMessageBox.Yes

def validate_csv(file_path):
    """Validate CSV file format for crab population data"""
    try:
        # Read CSV
        df = pd.read_csv(file_path)
        
        # Check required columns
        required_cols = ['ID', 'Population', 'Latitude', 'Longitude']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            return False, f"Missing required columns: {', '.join(missing_cols)}"
        
        # Check data types
        if not pd.api.types.is_numeric_dtype(df['ID']):
            return False, "ID column must contain numeric values"
        
        if not pd.api.types.is_numeric_dtype(df['Population']):
            return False, "Population column must contain numeric values"
        
        if not pd.api.types.is_numeric_dtype(df['Latitude']):
            return False, "Latitude column must contain numeric values"
        
        if not pd.api.types.is_numeric_dtype(df['Longitude']):
            return False, "Longitude column must contain numeric values"
        
        # Check value ranges
        if (df['Latitude'] < -90).any() or (df['Latitude'] > 90).any():
            return False, "Latitude values must be between -90 and 90"
        
        if (df['Longitude'] < -180).any() or (df['Longitude'] > 180).any():
            return False, "Longitude values must be between -180 and 180"
        
        if (df['Population'] <= 0).any():
            return False, "Population values must be positive"
        
        # Check for duplicate IDs
        if df['ID'].duplicated().any():
            return False, "Duplicate ID values found"
        
        return True, "CSV file is valid"
        
    except Exception as e:
        return False, f"Error validating CSV: {str(e)}"

def calculate_population_density(df, grid_size=100):
    """Calculate population density grid for heatmap"""
    if df.empty:
        return None, None, None
    
    # Get bounds
    min_lat = df['latitude'].min()
    max_lat = df['latitude'].max()
    min_lon = df['longitude'].min()
    max_lon = df['longitude'].max()
    
    # Add small buffer
    lat_buffer = (max_lat - min_lat) * 0.05
    lon_buffer = (max_lon - min_lon) * 0.05
    
    min_lat -= lat_buffer
    max_lat += lat_buffer
    min_lon -= lon_buffer
    max_lon += lon_buffer
    
    # Create grid
    lat_grid = np.linspace(min_lat, max_lat, grid_size)
    lon_grid = np.linspace(min_lon, max_lon, grid_size)
    
    # Create density matrix
    density = np.zeros((grid_size, grid_size))
    
    # Calculate density
    for _, row in df.iterrows():
        lat_idx = np.argmin(np.abs(lat_grid - row['latitude']))
        lon_idx = np.argmin(np.abs(lon_grid - row['longitude']))
        density[lat_idx, lon_idx] += row['population']
    
    return lat_grid, lon_grid, density

def ensure_directory_exists(directory):
    """Ensure directory exists, create if not"""
    if not os.path.exists(directory):
        os.makedirs(directory)