from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QGridLayout, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import numpy as np

from database import DatabaseManager

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize database manager
        self.db_manager = DatabaseManager()
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Add title
        title = QLabel("Blue Crab Population Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Create stats cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        # Total population card
        self.total_pop_card = self.create_stat_card("Total Population", "0", "assets/icons/population.png")
        stats_layout.addWidget(self.total_pop_card)
        
        # Total locations card
        self.total_loc_card = self.create_stat_card("Total Locations", "0", "assets/icons/location.png")
        stats_layout.addWidget(self.total_loc_card)
        
        # Average population card
        self.avg_pop_card = self.create_stat_card("Average Population", "0", "assets/icons/average.png")
        stats_layout.addWidget(self.avg_pop_card)
        
        # Highest population card
        self.max_pop_card = self.create_stat_card("Highest Population", "0", "assets/icons/max.png")
        stats_layout.addWidget(self.max_pop_card)
        
        layout.addLayout(stats_layout)
        
        # Create charts grid
        charts_grid = QGridLayout()
        charts_grid.setSpacing(20)
        
        # Population trend chart
        trend_frame = QFrame()
        trend_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(10, 25, 41, 0.7);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 10px;
            }
        """)
        trend_layout = QVBoxLayout(trend_frame)
        
        trend_title = QLabel("Population Trend")
        trend_title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        trend_layout.addWidget(trend_title)
        
        self.trend_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.trend_canvas.figure.patch.set_facecolor('#0a1929')
        self.trend_axes = self.trend_canvas.figure.add_subplot(111)
        self.trend_axes.set_facecolor('#0a1929')
        self.trend_axes.tick_params(colors='white')
        self.trend_axes.spines['bottom'].set_color('white')
        self.trend_axes.spines['top'].set_color('white')
        self.trend_axes.spines['left'].set_color('white')
        self.trend_axes.spines['right'].set_color('white')
        self.trend_axes.xaxis.label.set_color('white')
        self.trend_axes.yaxis.label.set_color('white')
        self.trend_axes.title.set_color('white')
        trend_layout.addWidget(self.trend_canvas)
        
        charts_grid.addWidget(trend_frame, 0, 0, 1, 2)
        
        # Population distribution chart
        dist_frame = QFrame()
        dist_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(10, 25, 41, 0.7);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 10px;
            }
        """)
        dist_layout = QVBoxLayout(dist_frame)
        
        dist_title = QLabel("Population Distribution")
        dist_title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        dist_layout.addWidget(dist_title)
        
        self.dist_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.dist_canvas.figure.patch.set_facecolor('#0a1929')
        self.dist_axes = self.dist_canvas.figure.add_subplot(111)
        self.dist_axes.set_facecolor('#0a1929')
        self.dist_axes.tick_params(colors='white')
        self.dist_axes.spines['bottom'].set_color('white')
        self.dist_axes.spines['top'].set_color('white')
        self.dist_axes.spines['left'].set_color('white')
        self.dist_axes.spines['right'].set_color('white')
        self.dist_axes.xaxis.label.set_color('white')
        self.dist_axes.yaxis.label.set_color('white')
        self.dist_axes.title.set_color('white')
        dist_layout.addWidget(self.dist_canvas)
        
        charts_grid.addWidget(dist_frame, 1, 0)
        
        # Population by location chart
        loc_frame = QFrame()
        loc_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(10, 25, 41, 0.7);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 10px;
            }
        """)
        loc_layout = QVBoxLayout(loc_frame)
        
        loc_title = QLabel("Population by Location")
        loc_title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        loc_layout.addWidget(loc_title)
        
        self.loc_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.loc_canvas.figure.patch.set_facecolor('#0a1929')
        self.loc_axes = self.loc_canvas.figure.add_subplot(111)
        self.loc_axes.set_facecolor('#0a1929')
        self.loc_axes.tick_params(colors='white')
        self.loc_axes.spines['bottom'].set_color('white')
        self.loc_axes.spines['top'].set_color('white')
        self.loc_axes.spines['left'].set_color('white')
        self.loc_axes.spines['right'].set_color('white')
        self.loc_axes.xaxis.label.set_color('white')
        self.loc_axes.yaxis.label.set_color('white')
        self.loc_axes.title.set_color('white')
        loc_layout.addWidget(self.loc_canvas)
        
        charts_grid.addWidget(loc_frame, 1, 1)
        
        layout.addLayout(charts_grid)
        
        # Set up timer for periodic updates
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_dashboard)
        self.update_timer.start(5000)  # Update every 5 seconds
        
        # Initial update
        self.update_dashboard()
    
    def create_stat_card(self, title, value, icon_path=None):
        """Create a statistics card widget"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(10, 25, 41, 0.7);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(card)
        
        # Add title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; color: rgba(255, 255, 255, 0.7);")
        layout.addWidget(title_label)
        
        # Add value
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        value_label.setObjectName(f"{title.lower().replace(' ', '_')}_value")
        layout.addWidget(value_label)
        
        # Add icon if provided
        if icon_path:
            icon_label = QLabel()
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                icon_label.setPixmap(pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                icon_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
                layout.addWidget(icon_label)
        
        return card
    
    def update_dashboard(self):
        """Update dashboard with latest data"""
        # Get crab data from database
        df = self.db_manager.get_all_crab_data()
        
        if df.empty:
            self.show_no_data_message()
            return
        
        # Update stats cards
        total_pop = df['population'].sum()
        self.total_pop_card.findChild(QLabel, "total_population_value").setText(f"{total_pop:,}")
        
        total_loc = len(df)
        self.total_loc_card.findChild(QLabel, "total_locations_value").setText(f"{total_loc:,}")
        
        avg_pop = df['population'].mean()
        self.avg_pop_card.findChild(QLabel, "average_population_value").setText(f"{avg_pop:.1f}")
        
        max_pop = df['population'].max()
        self.max_pop_card.findChild(QLabel, "highest_population_value").setText(f"{max_pop:,}")
        
        # Update trend chart
        self.trend_axes.clear()
        
        # Convert to datetime if not already
        if 'date_added' in df.columns:
            df['date_added'] = pd.to_datetime(df['date_added'])
            
            # Group by date and sum population
            trend_data = df.groupby(df['date_added'].dt.date)['population'].sum().reset_index()
            trend_data = trend_data.sort_values('date_added')
            
            if len(trend_data) > 1:
                self.trend_axes.plot(trend_data['date_added'], trend_data['population'], 
                                   marker='o', linestyle='-', color='#4a9cf5')
                self.trend_axes.set_xlabel('Date')
                self.trend_axes.set_ylabel('Total Population')
                self.trend_axes.grid(True, alpha=0.3)
                self.trend_canvas.figure.autofmt_xdate()
            else:
                self.trend_axes.text(0.5, 0.5, "Not enough time data for trend analysis",
                                   horizontalalignment='center', verticalalignment='center',
                                   color='white', fontsize=12, transform=self.trend_axes.transAxes)
                self.trend_axes.set_axis_off()
        else:
            self.trend_axes.text(0.5, 0.5, "No time data available",
                               horizontalalignment='center', verticalalignment='center',
                               color='white', fontsize=12, transform=self.trend_axes.transAxes)
            self.trend_axes.set_axis_off()
            
        self.trend_canvas.draw()
        
        # Update distribution chart
        self.dist_axes.clear()
        
        # Create histogram
        self.dist_axes.hist(df['population'], bins=20, color='#4a9cf5', alpha=0.7)
        self.dist_axes.set_xlabel('Population Size')
        self.dist_axes.set_ylabel('Frequency')
        self.dist_axes.grid(True, alpha=0.3)
        
        self.dist_canvas.draw()
        
        # Update location chart
        self.loc_axes.clear()
        
        # Get top 5 locations by population
        top_locations = df.nlargest(5, 'population')
        
        # Create bar chart
        bars = self.loc_axes.bar(range(len(top_locations)), top_locations['population'], color='#4a9cf5')
        self.loc_axes.set_xlabel('Location ID')
        self.loc_axes.set_ylabel('Population')
        self.loc_axes.set_xticks(range(len(top_locations)))
        self.loc_axes.set_xticklabels(top_locations['id'])
        self.loc_axes.grid(True, alpha=0.3)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            self.loc_axes.text(bar.get_x() + bar.get_width()/2., height + 5,
                             f'{int(height)}',
                             ha='center', va='bottom', color='white')
        
        self.loc_canvas.draw()
    
    def show_no_data_message(self):
        """Show message when no data is available"""
        # Update stats cards
        self.total_pop_card.findChild(QLabel, "total_population_value").setText("0")
        self.total_loc_card.findChild(QLabel, "total_locations_value").setText("0")
        self.avg_pop_card.findChild(QLabel, "average_population_value").setText("0")
        self.max_pop_card.findChild(QLabel, "highest_population_value").setText("0")
        
        # Update charts
        for canvas, axes in [(self.trend_canvas, self.trend_axes), 
                            (self.dist_canvas, self.dist_axes), 
                            (self.loc_canvas, self.loc_axes)]:
            axes.clear()
            axes.text(0.5, 0.5, "No data available. Please upload crab population data.",
                    horizontalalignment='center', verticalalignment='center',
                    color='white', fontsize=12)
            axes.set_axis_off()
            canvas.draw()