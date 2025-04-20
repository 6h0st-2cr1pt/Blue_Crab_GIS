import os
import sqlite3
import pandas as pd
from PyQt5.QtCore import QObject, pyqtSignal

class DatabaseManager(QObject):
    error_occurred = pyqtSignal(str)
    
    def __init__(self, db_path='data/blue_crab.db'):
        super().__init__()
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.initialize_db()
    
    def initialize_db(self):
        """Create database and tables if they don't exist"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create crab_population table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS crab_population (
                    id INTEGER PRIMARY KEY,
                    population INTEGER NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    date_added TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            ''')
            
            # Insert default settings if not exist
            default_settings = [
                ('theme', 'dark'),
                ('map_style', 'dark'),
                ('default_view', 'dashboard')
            ]
            
            for key, value in default_settings:
                cursor.execute('''
                    INSERT OR IGNORE INTO settings (key, value)
                    VALUES (?, ?)
                ''', (key, value))
            
            conn.commit()
            conn.close()
            
        except sqlite3.Error as e:
            self.error_occurred.emit(f"Database initialization error: {str(e)}")
    
    def insert_crab_data(self, crab_id, population, latitude, longitude):
        """Insert a single crab population data point"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO crab_population (id, population, latitude, longitude)
                VALUES (?, ?, ?, ?)
            ''', (crab_id, population, latitude, longitude))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            self.error_occurred.emit(f"Error inserting data: {str(e)}")
            return False
    
    def import_csv(self, csv_path):
        """Import data from CSV file"""
        try:
            # Read CSV using pandas
            df = pd.read_csv(csv_path)
            
            # Check required columns
            required_cols = ['ID', 'Population', 'Latitude', 'Longitude']
            if not all(col in df.columns for col in required_cols):
                self.error_occurred.emit("CSV file missing required columns: ID, Population, Latitude, Longitude")
                return False
            
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            
            # Insert data
            df.to_sql('crab_population', conn, if_exists='append', index=False, 
                     dtype={
                         'ID': 'INTEGER',
                         'Population': 'INTEGER',
                         'Latitude': 'REAL',
                         'Longitude': 'REAL'
                     })
            
            conn.close()
            return True
            
        except Exception as e:
            self.error_occurred.emit(f"Error importing CSV: {str(e)}")
            return False
    
    def get_all_crab_data(self):
        """Get all crab population data"""
        try:
            conn = sqlite3.connect(self.db_path)
            query = "SELECT id, population, latitude, longitude, date_added FROM crab_population"
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
            
        except sqlite3.Error as e:
            self.error_occurred.emit(f"Error retrieving data: {str(e)}")
            return pd.DataFrame()
    
    def get_crab_by_id(self, crab_id):
        """Get crab data by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            query = "SELECT * FROM crab_population WHERE id = ?"
            df = pd.read_sql_query(query, conn, params=(crab_id,))
            conn.close()
            
            if df.empty:
                return None
            return df.iloc[0].to_dict()
            
        except sqlite3.Error as e:
            self.error_occurred.emit(f"Error retrieving crab data: {str(e)}")
            return None
    
    def get_setting(self, key, default=None):
        """Get a setting value"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            result = cursor.fetchone()
            
            conn.close()
            
            if result:
                return result[0]
            return default
            
        except sqlite3.Error as e:
            self.error_occurred.emit(f"Error retrieving setting: {str(e)}")
            return default
    
    def set_setting(self, key, value):
        """Set a setting value"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO settings (key, value)
                VALUES (?, ?)
            ''', (key, value))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            self.error_occurred.emit(f"Error saving setting: {str(e)}")
            return False