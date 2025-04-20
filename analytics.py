from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QPushButton, QFrame, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter
import matplotlib
matplotlib.use('Agg')  # Use Agg backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import io
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from database import DatabaseManager

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor('#0a1929')
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('#0a1929')
        
        # Set text color to white
        plt.rcParams.update({
            'text.color': 'white',
            'axes.labelcolor': 'white',
            'axes.edgecolor': 'white',
            'axes.facecolor': '#0a1929',
            'xtick.color': 'white',
            'ytick.color': 'white',
            'grid.color': 'gray',
            'figure.facecolor': '#0a1929',
            'figure.edgecolor': '#0a1929',
            'savefig.facecolor': '#0a1929',
            'savefig.edgecolor': '#0a1929',
        })
        
        super().__init__(self.fig)
        self.setStyleSheet("background-color: #0a1929;")

class AnalyticsWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize database manager
        self.db_manager = DatabaseManager()
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add title
        title = QLabel("Blue Crab Population Analytics")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Add controls
        controls_frame = QFrame()
        controls_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(10, 25, 41, 0.7);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 10px;
            }
        """)
        
        controls_layout = QHBoxLayout(controls_frame)
        
        # Chart type selector
        chart_label = QLabel("Chart Type:")
        chart_label.setStyleSheet("color: white;")
        self.chart_combo = QComboBox()
        self.chart_combo.addItems([
            "Population Distribution", 
            "Population Density Heatmap", 
            "Population by Location",
            "Population Trend"
        ])
        self.chart_combo.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            padding: 5px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
        """)
        self.chart_combo.currentIndexChanged.connect(self.update_chart)
        
        # Refresh button
        self.refresh_btn = QPushButton("Refresh Data")
        self.refresh_btn.clicked.connect(self.update_chart)
        
        # Add controls to layout
        controls_layout.addWidget(chart_label)
        controls_layout.addWidget(self.chart_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(self.refresh_btn)
        
        layout.addWidget(controls_frame)
        
        # Create grid for charts
        charts_grid = QGridLayout()
        charts_grid.setSpacing(20)
        
        # Create chart frames
        self.chart_frames = []
        
        for i in range(2):
            for j in range(2):
                frame = QFrame()
                frame.setStyleSheet("""
                    QFrame {
                        background-color: rgba(10, 25, 41, 0.7);
                        border-radius: 10px;
                        border: 1px solid rgba(255, 255, 255, 0.1);
                    }
                """)
                
                frame_layout = QVBoxLayout(frame)
                
                # Add canvas for matplotlib
                canvas = MatplotlibCanvas(width=5, height=4, dpi=100)
                frame_layout.addWidget(canvas)
                
                charts_grid.addWidget(frame, i, j)
                self.chart_frames.append((frame, canvas))
        
        layout.addLayout(charts_grid)
        
        # Initialize charts
        self.update_chart()
        
    def update_chart(self):
        """Update charts based on selected type"""
        # Get crab data from database
        df = self.db_manager.get_all_crab_data()
        
        if df.empty:
            self.show_no_data_message()
            return
        
        chart_type = self.chart_combo.currentText()
        
        if chart_type == "Population Distribution":
            self.plot_population_distribution(df)
        elif chart_type == "Population Density Heatmap":
            self.plot_density_heatmap(df)
        elif chart_type == "Population by Location":
            self.plot_population_by_location(df)
        elif chart_type == "Population Trend":
            self.plot_population_trend(df)
    
    def show_no_data_message(self):
        """Show message when no data is available"""
        for _, canvas in self.chart_frames:
            canvas.axes.clear()
            canvas.axes.text(0.5, 0.5, "No data available. Please upload crab population data.",
                           horizontalalignment='center', verticalalignment='center',
                           color='white', fontsize=12)
            canvas.axes.set_axis_off()
            canvas.draw()
    
    def plot_population_distribution(self, df):
        """Plot population distribution charts"""
        # Chart 1: Histogram
        canvas1 = self.chart_frames[0][1]
        canvas1.axes.clear()
        sns.histplot(df['population'], bins=20, kde=True, color='#4a9cf5', ax=canvas1.axes)
        canvas1.axes.set_title('Population Distribution', color='white')
        canvas1.axes.set_xlabel('Population Size')
        canvas1.axes.set_ylabel('Frequency')
        canvas1.axes.grid(True, alpha=0.3)
        canvas1.draw()
        
        # Chart 2: Box plot
        canvas2 = self.chart_frames[1][1]
        canvas2.axes.clear()
        sns.boxplot(y=df['population'], color='#4a9cf5', ax=canvas2.axes)
        canvas2.axes.set_title('Population Box Plot', color='white')
        canvas2.axes.set_ylabel('Population Size')
        canvas2.axes.grid(True, alpha=0.3)
        canvas2.draw()
        
        # Chart 3: Violin plot
        canvas3 = self.chart_frames[2][1]
        canvas3.axes.clear()
        sns.violinplot(y=df['population'], color='#4a9cf5', ax=canvas3.axes)
        canvas3.axes.set_title('Population Violin Plot', color='white')
        canvas3.axes.set_ylabel('Population Size')
        canvas3.axes.grid(True, alpha=0.3)
        canvas3.draw()
        
        # Chart 4: CDF
        canvas4 = self.chart_frames[3][1]
        canvas4.axes.clear()
        
        # Calculate CDF
        x = np.sort(df['population'])
        y = np.arange(1, len(x) + 1) / len(x)
        
        canvas4.axes.plot(x, y, marker='.', linestyle='none', color='#4a9cf5')
        canvas4.axes.set_title('Cumulative Distribution Function', color='white')
        canvas4.axes.set_xlabel('Population Size')
        canvas4.axes.set_ylabel('Cumulative Probability')
        canvas4.axes.grid(True, alpha=0.3)
        canvas4.draw()
    
    def plot_density_heatmap(self, df):
        """Plot density heatmap charts"""
        # Chart 1: 2D Histogram
        canvas1 = self.chart_frames[0][1]
        canvas1.axes.clear()
        
        # Create 2D histogram
        h = canvas1.axes.hist2d(df['longitude'], df['latitude'], 
                              bins=20, cmap='Blues')
        canvas1.fig.colorbar(h[3], ax=canvas1.axes, label='Count')
        canvas1.axes.set_title('Population Density Heatmap', color='white')
        canvas1.axes.set_xlabel('Longitude')
        canvas1.axes.set_ylabel('Latitude')
        canvas1.draw()
        
        # Chart 2: KDE plot
        canvas2 = self.chart_frames[1][1]
        canvas2.axes.clear()
        
        # Create KDE plot
        sns.kdeplot(x=df['longitude'], y=df['latitude'], 
                   fill=True, cmap='Blues', ax=canvas2.axes)
        canvas2.axes.set_title('Population Density KDE', color='white')
        canvas2.axes.set_xlabel('Longitude')
        canvas2.axes.set_ylabel('Latitude')
        canvas2.draw()
        
        # Chart 3: Hexbin plot
        canvas3 = self.chart_frames[2][1]
        canvas3.axes.clear()
        
        # Create hexbin plot
        hb = canvas3.axes.hexbin(df['longitude'], df['latitude'], 
                               gridsize=20, cmap='Blues')
        canvas3.fig.colorbar(hb, ax=canvas3.axes, label='Count')
        canvas3.axes.set_title('Population Hexbin Plot', color='white')
        canvas3.axes.set_xlabel('Longitude')
        canvas3.axes.set_ylabel('Latitude')
        canvas3.draw()
        
        # Chart 4: Scatter plot with size
        canvas4 = self.chart_frames[3][1]
        canvas4.axes.clear()
        
        # Create scatter plot
        scatter = canvas4.axes.scatter(df['longitude'], df['latitude'], 
                                     c=df['population'], s=df['population']/10,
                                     cmap='Blues', alpha=0.7)
        canvas4.fig.colorbar(scatter, ax=canvas4.axes, label='Population')
        canvas4.axes.set_title('Population by Location', color='white')
        canvas4.axes.set_xlabel('Longitude')
        canvas4.axes.set_ylabel('Latitude')
        canvas4.draw()
    
    def plot_population_by_location(self, df):
        """Plot population by location charts"""
        # Chart 1: Bubble chart
        canvas1 = self.chart_frames[0][1]
        canvas1.axes.clear()
        
        # Create bubble chart
        scatter = canvas1.axes.scatter(df['longitude'], df['latitude'], 
                                     s=df['population']/10, alpha=0.7,
                                     c=df['population'], cmap='Blues')
        canvas1.fig.colorbar(scatter, ax=canvas1.axes, label='Population')
        canvas1.axes.set_title('Population Bubble Chart', color='white')
        canvas1.axes.set_xlabel('Longitude')
        canvas1.axes.set_ylabel('Latitude')
        canvas1.draw()
        
        # Chart 2: 3D scatter plot
        canvas2 = self.chart_frames[1][1]
        canvas2.axes.clear()
        canvas2.axes.remove()
        canvas2.axes = canvas2.fig.add_subplot(111, projection='3d')
        
        # Create 3D scatter plot
        scatter = canvas2.axes.scatter(df['longitude'], df['latitude'], df['population'],
                                     c=df['population'], cmap='Blues', alpha=0.7)
        canvas2.fig.colorbar(scatter, ax=canvas2.axes, label='Population')
        canvas2.axes.set_title('3D Population Plot', color='white')
        canvas2.axes.set_xlabel('Longitude')
        canvas2.axes.set_ylabel('Latitude')
        canvas2.axes.set_zlabel('Population')
        canvas2.draw()
        
        # Chart 3: Contour plot
        canvas3 = self.chart_frames[2][1]
        canvas3.axes.clear()
        
        # Create grid for contour plot
        x = np.linspace(df['longitude'].min(), df['longitude'].max(), 100)
        y = np.linspace(df['latitude'].min(), df['latitude'].max(), 100)
        X, Y = np.meshgrid(x, y)
        
        # Use simple interpolation for contour
        from scipy.interpolate import griddata
        Z = griddata((df['longitude'], df['latitude']), df['population'], (X, Y), method='cubic')
        
        contour = canvas3.axes.contourf(X, Y, Z, cmap='Blues')
        canvas3.fig.colorbar(contour, ax=canvas3.axes, label='Population')
        canvas3.axes.set_title('Population Contour Plot', color='white')
        canvas3.axes.set_xlabel('Longitude')
        canvas3.axes.set_ylabel('Latitude')
        canvas3.draw()
        
        # Chart 4: Population by quadrant
        canvas4 = self.chart_frames[3][1]
        canvas4.axes.clear()
        
        # Create quadrants
        lon_mid = (df['longitude'].max() + df['longitude'].min()) / 2
        lat_mid = (df['latitude'].max() + df['latitude'].min()) / 2
        
        df['quadrant'] = 'Unknown'
        df.loc[(df['longitude'] >= lon_mid) & (df['latitude'] >= lat_mid), 'quadrant'] = 'NE'
        df.loc[(df['longitude'] < lon_mid) & (df['latitude'] >= lat_mid), 'quadrant'] = 'NW'
        df.loc[(df['longitude'] >= lon_mid) & (df['latitude'] < lat_mid), 'quadrant'] = 'SE'
        df.loc[(df['longitude'] < lon_mid) & (df['latitude'] < lat_mid), 'quadrant'] = 'SW'
        
        quadrant_data = df.groupby('quadrant')['population'].sum().reset_index()
        
        sns.barplot(x='quadrant', y='population', data=quadrant_data, palette='Blues', ax=canvas4.axes)
        canvas4.axes.set_title('Population by Quadrant', color='white')
        canvas4.axes.set_xlabel('Quadrant')
        canvas4.axes.set_ylabel('Total Population')
        canvas4.draw()
    
    def plot_population_trend(self, df):
        """Plot population trend charts"""
        # Add date column if not exists
        if 'date_added' not in df.columns:
            df['date_added'] = pd.Timestamp.now()
        
        # Convert to datetime
        df['date_added'] = pd.to_datetime(df['date_added'])
        
        # Extract date components
        df['year'] = df['date_added'].dt.year
        df['month'] = df['date_added'].dt.month
        df['day'] = df['date_added'].dt.day
        
        # Chart 1: Population over time
        canvas1 = self.chart_frames[0][1]
        canvas1.axes.clear()
        
        time_data = df.groupby('date_added')['population'].sum().reset_index()
        time_data = time_data.sort_values('date_added')
        
        canvas1.axes.plot(time_data['date_added'], time_data['population'], 
                        marker='o', linestyle='-', color='#4a9cf5')
        canvas1.axes.set_title('Population Over Time', color='white')
        canvas1.axes.set_xlabel('Date')
        canvas1.axes.set_ylabel('Total Population')
        canvas1.axes.grid(True, alpha=0.3)
        canvas1.fig.autofmt_xdate()
        canvas1.draw()
        
        # Chart 2: Monthly population
        canvas2 = self.chart_frames[1][1]
        canvas2.axes.clear()
        
        monthly_data = df.groupby('month')['population'].sum().reset_index()
        monthly_data = monthly_data.sort_values('month')
        
        sns.barplot(x='month', y='population', data=monthly_data, palette='Blues', ax=canvas2.axes)
        canvas2.axes.set_title('Population by Month', color='white')
        canvas2.axes.set_xlabel('Month')
        canvas2.axes.set_ylabel('Total Population')
        canvas2.draw()
        
        # Chart 3: Population distribution over time
        canvas3 = self.chart_frames[2][1]
        canvas3.axes.clear()
        
        # Create box plot by month
        sns.boxplot(x='month', y='population', data=df, palette='Blues', ax=canvas3.axes)
        canvas3.axes.set_title('Population Distribution by Month', color='white')
        canvas3.axes.set_xlabel('Month')
        canvas3.axes.set_ylabel('Population')
        canvas3.draw()
        
        # Chart 4: Cumulative population over time
        canvas4 = self.chart_frames[3][1]
        canvas4.axes.clear()
        
        time_data['cumulative'] = time_data['population'].cumsum()
        
        canvas4.axes.plot(time_data['date_added'], time_data['cumulative'], 
                        marker='o', linestyle='-', color='#4a9cf5')
        canvas4.axes.set_title('Cumulative Population Over Time', color='white')
        canvas4.axes.set_xlabel('Date')
        canvas4.axes.set_ylabel('Cumulative Population')
        canvas4.axes.grid(True, alpha=0.3)
        canvas4.fig.autofmt_xdate()
        canvas4.draw()