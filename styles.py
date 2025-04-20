from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

def apply_glassmorphism_style(widget):
    """Apply glassmorphism effect to a widget"""
    widget.setStyleSheet("""
        QFrame {
            background-color: rgba(10, 25, 41, 0.7);
            border-radius: 0px;  /* Remove border radius for full coverage */
            border: none;  /* Remove border */
        }
        
        QLabel {
            color: white;
        }
        
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
        
        QPushButton:pressed {
            background-color: rgba(0, 82, 164, 0.9);
        }
        
        QLineEdit, QComboBox, QSpinBox {
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            padding: 8px;
            color: white;
        }
        
        QTableView {
            background-color: rgba(10, 25, 41, 0.5);
            alternate-background-color: rgba(20, 35, 51, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            color: white;
            gridline-color: rgba(255, 255, 255, 0.1);
        }
        
        QTableView::item:selected {
            background-color: rgba(0, 102, 204, 0.5);
        }
        
        QHeaderView::section {
            background-color: rgba(0, 51, 102, 0.7);
            color: white;
            padding: 5px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
    """)
    
    # Add shadow effect but with reduced blur to avoid cutting off edges
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(10)  # Reduced blur radius
    shadow.setColor(QColor(0, 0, 0, 80))
    shadow.setOffset(0, 0)
    widget.setGraphicsEffect(shadow)

def get_map_dark_mode_css():
    """Return CSS for dark mode map"""
    return """
    body {
        padding: 0;
        margin: 0;
    }
    
    html, body, #map {
        height: 100%;
        width: 100%;
    }
    
    .leaflet-popup-content-wrapper {
        background-color: rgba(10, 25, 41, 0.9);
        color: white;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .leaflet-popup-tip {
        background-color: rgba(10, 25, 41, 0.9);
    }
    
    .info-title {
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 10px;
        color: #4a9cf5;
    }
    
    .info-row {
        margin: 5px 0;
    }
    
    .info-label {
        font-weight: bold;
        color: #a0c8ff;
    }
    
    /* Custom styling for map controls */
    .leaflet-control-zoom {
        border: none !important;
    }
    
    .leaflet-control-zoom a {
        background-color: rgba(10, 25, 41, 0.7) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .leaflet-control-zoom a:hover {
        background-color: rgba(0, 102, 204, 0.7) !important;
    }
    
    .leaflet-control-attribution {
        background-color: rgba(10, 25, 41, 0.7) !important;
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    /* Make map take full height */
    .leaflet-container {
        height: 100vh !important;
        width: 100% !important;
    }
    """