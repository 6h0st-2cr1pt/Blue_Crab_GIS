import os
import json
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QPushButton, QSlider, QFrame)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel

from database import DatabaseManager
from styles import get_map_dark_mode_css
import folium
from folium.plugins import HeatMap, MarkerCluster
from jinja2 import Template
from branca.element import Figure

class GISWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize database manager
        self.db_manager = DatabaseManager()
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins to maximize map size
        layout.setSpacing(0)  # Remove spacing
        
        # Add controls in a horizontal bar at the top
        controls_frame = QFrame()
        controls_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(10, 25, 41, 0.7);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                padding: 10px;
            }
        """)
        
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setContentsMargins(10, 5, 10, 5)  # Compact controls
        
        # Title
        title = QLabel("Negros Occidental Blue Crab GIS")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        
        # View type selector
        view_label = QLabel("View:")
        view_label.setStyleSheet("color: white;")
        self.view_combo = QComboBox()
        self.view_combo.addItems(["Markers", "Heat Map", "Clusters"])
        self.view_combo.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            padding: 5px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
        """)
        self.view_combo.currentIndexChanged.connect(self.update_map)
        
        # Density filter
        density_label = QLabel("Population Density:")
        density_label.setStyleSheet("color: white;")
        self.density_slider = QSlider(Qt.Horizontal)
        self.density_slider.setRange(0, 100)
        self.density_slider.setValue(0)
        self.density_slider.setFixedWidth(150)  # Fixed width for slider
        self.density_slider.setStyleSheet("""
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
        self.density_slider.valueChanged.connect(self.update_map)
        
        # Refresh button
        self.refresh_btn = QPushButton("Refresh Data")
        self.refresh_btn.clicked.connect(self.update_map)
        
        # Add controls to layout
        controls_layout.addWidget(title)
        controls_layout.addStretch(1)
        controls_layout.addWidget(view_label)
        controls_layout.addWidget(self.view_combo)
        controls_layout.addSpacing(20)
        controls_layout.addWidget(density_label)
        controls_layout.addWidget(self.density_slider)
        controls_layout.addSpacing(20)
        controls_layout.addWidget(self.refresh_btn)
        
        layout.addWidget(controls_frame)
        
        # Create web view for map - this will take all remaining space
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view, 1)  # Give it a stretch factor of 1
        
        # Initialize map
        self.update_map()
        
    def update_map(self):
        """Update the map with current data and settings"""
        # Get crab data from database
        df = self.db_manager.get_all_crab_data()
        
        # Create a Figure object
        fig = Figure(width='100%', height='100%')
        
        # Create map centered on Negros Occidental
        # Coordinates for Negros Occidental, Philippines
        center_lat = 10.4
        center_lon = 123.0
        
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=9,  # Zoom level to show the province
            tiles='CartoDB dark_matter',  # Dark mode tiles
            width='100%',
            height='100%'
        )
        
        # Add map to figure
        fig.add_child(m)
        
        # Add province boundary for Negros Occidental if available
        # This would require GeoJSON data for the province boundary
        
        if not df.empty:
            # Apply density filter
            min_population = self.density_slider.value()
            if min_population > 0:
                df = df[df['population'] >= min_population]
            
            # Add data to map based on view type
            view_type = self.view_combo.currentText()
            
            if view_type == "Markers":
                # Create marker for each data point
                for _, row in df.iterrows():
                    popup_html = self.create_popup_html(row)
                    folium.Marker(
                        location=[row['latitude'], row['longitude']],
                        popup=folium.Popup(popup_html, max_width=300),
                        icon=folium.Icon(color='blue', icon='info-sign')
                    ).add_to(m)
                    
            elif view_type == "Heat Map":
                # Create heat map
                heat_data = [[row['latitude'], row['longitude'], row['population']] for _, row in df.iterrows()]
                HeatMap(heat_data, radius=15).add_to(m)
                
            elif view_type == "Clusters":
                # Create marker cluster
                marker_cluster = MarkerCluster().add_to(m)
                
                for _, row in df.iterrows():
                    popup_html = self.create_popup_html(row)
                    folium.Marker(
                        location=[row['latitude'], row['longitude']],
                        popup=folium.Popup(popup_html, max_width=300),
                        icon=folium.Icon(color='blue')
                    ).add_to(marker_cluster)
        else:
            # Add a message if no data
            folium.Marker(
                location=[center_lat, center_lon],
                popup="No data available. Please upload crab population data.",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
        
        # Add custom CSS for dark mode
        custom_css = get_map_dark_mode_css()
        folium.Element(f"<style>{custom_css}</style>").add_to(m)
        
        # Save map to HTML file
        map_html = os.path.join('assets', 'leaflet_templates', 'temp_map.html')
        os.makedirs(os.path.dirname(map_html), exist_ok=True)
        fig.save(map_html)
        
        # Load map in web view
        self.web_view.load(QUrl.fromLocalFile(os.path.abspath(map_html)))
    
    def create_popup_html(self, row):
        """Create HTML for popup"""
        template = """
        <div class="popup-content">
            <div class="info-title">Blue Crab Population</div>
            <div class="info-row">
                <span class="info-label">ID:</span> {{ id }}
            </div>
            <div class="info-row">
                <span class="info-label">Population:</span> {{ population }}
            </div>
            <div class="info-row">
                <span class="info-label">Coordinates:</span> {{ latitude }}, {{ longitude }}
            </div>
            <div class="info-row">
                <span class="info-label">Date Added:</span> {{ date_added }}
            </div>
        </div>
        """
        
        return Template(template).render(
            id=row['id'],
            population=row['population'],
            latitude=row['latitude'],
            longitude=row['longitude'],
            date_added=row['date_added']
        )