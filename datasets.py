from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableView, QHeaderView, QMessageBox,
                            QFrame, QLineEdit, QComboBox)
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, QSortFilterProxyModel
from PyQt5.QtGui import QColor

import pandas as pd
from database import DatabaseManager

class CrabDataTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self.columns = data.columns
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._data)
    
    def columnCount(self, parent=QModelIndex()):
        return len(self.columns)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            # Format based on column type
            if pd.api.types.is_numeric_dtype(self._data.dtypes[index.column()]):
                return str(value)
            else:
                return str(value)
        
        elif role == Qt.TextAlignmentRole:
            # Align numeric columns to the right
            if pd.api.types.is_numeric_dtype(self._data.dtypes[index.column()]):
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter
        
        elif role == Qt.BackgroundRole:
            # Alternate row colors
            if index.row() % 2 == 0:
                return QColor(10, 25, 41)
            else:
                return QColor(20, 35, 51)
        
        elif role == Qt.ForegroundRole:
            return QColor(255, 255, 255)
        
        return QVariant()
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.columns[section]).title()
            else:
                return str(section + 1)
        
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        
        elif role == Qt.ForegroundRole:
            return QColor(255, 255, 255)
        
        elif role == Qt.BackgroundRole:
            return QColor(0, 51, 102)
        
        return QVariant()
    
    def sort(self, column, order):
        """Sort table by given column number."""
        self.layoutAboutToBeChanged.emit()
        self._data = self._data.sort_values(self.columns[column], 
                                          ascending=order == Qt.AscendingOrder)
        self.layoutChanged.emit()

class DatasetsWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize database manager
        self.db_manager = DatabaseManager()
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add title
        title = QLabel("Blue Crab Population Datasets")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Add search and filter controls
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
        
        # Search input
        search_label = QLabel("Search:")
        search_label.setStyleSheet("color: white;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by ID or location...")
        self.search_input.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            padding: 8px;
        """)
        self.search_input.textChanged.connect(self.filter_data)
        
        # Filter by column
        filter_label = QLabel("Filter by:")
        filter_label.setStyleSheet("color: white;")
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Columns", "ID", "Population", "Latitude", "Longitude"])
        self.filter_combo.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            padding: 8px;
        """)
        self.filter_combo.currentIndexChanged.connect(self.filter_data)
        
        # Refresh button
        self.refresh_btn = QPushButton("Refresh Data")
        self.refresh_btn.clicked.connect(self.load_data)
        
        # Add controls to layout
        controls_layout.addWidget(search_label)
        controls_layout.addWidget(self.search_input)
        controls_layout.addWidget(filter_label)
        controls_layout.addWidget(self.filter_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(self.refresh_btn)
        
        layout.addWidget(controls_frame)
        
        # Create table view
        self.table_view = QTableView()
        self.table_view.setStyleSheet("""
            QTableView {
                background-color: rgba(10, 25, 41, 0.5);
                alternate-background-color: rgba(20, 35, 51, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 5px;
                color: white;
                gridline-color: rgba(255, 255, 255, 0.1);
                selection-background-color: rgba(0, 102, 204, 0.5);
            }
            
            QHeaderView::section {
                background-color: rgba(0, 51, 102, 0.7);
                color: white;
                padding: 5px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            QTableView::item:selected {
                background-color: rgba(0, 102, 204, 0.5);
            }
        """)
        
        # Configure table view
        self.table_view.setSortingEnabled(True)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setVisible(False)
        
        layout.addWidget(self.table_view)
        
        # Add action buttons
        buttons_layout = QHBoxLayout()
        
        self.export_btn = QPushButton("Export Data")
        self.export_btn.clicked.connect(self.export_data)
        
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self.delete_selected)
        
        buttons_layout.addWidget(self.export_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.delete_btn)
        
        layout.addLayout(buttons_layout)
        
        # Load initial data
        self.load_data()
    
    def load_data(self):
        """Load data from database"""
        # Get crab data from database
        df = self.db_manager.get_all_crab_data()
        
        if df.empty:
            # Create empty dataframe with correct columns
            df = pd.DataFrame(columns=['id', 'population', 'latitude', 'longitude', 'date_added'])
        
        # Create model
        self.model = CrabDataTableModel(df)
        
        # Create proxy model for filtering
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        
        # Set model to table view
        self.table_view.setModel(self.proxy_model)
    
    def filter_data(self):
        """Filter data based on search input and filter column"""
        search_text = self.search_input.text()
        filter_column = self.filter_combo.currentIndex() - 1  # -1 because "All Columns" is index 0
        
        if filter_column >= 0:
            # Filter specific column
            self.proxy_model.setFilterKeyColumn(filter_column)
        else:
            # Filter all columns
            self.proxy_model.setFilterKeyColumn(-1)
        
        self.proxy_model.setFilterFixedString(search_text)
    
    def export_data(self):
        """Export data to CSV file"""
        # Get filtered data from proxy model
        source_model = self.proxy_model.sourceModel()
        if source_model._data.empty:
            self.show_error("No data to export.")
            return
        
        # Open file dialog
        from PyQt5.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Data", "", "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            try:
                # Export to CSV
                source_model._data.to_csv(file_path, index=False)
                self.show_success(f"Data exported successfully to {file_path}")
            except Exception as e:
                self.show_error(f"Error exporting data: {str(e)}")
    
    def delete_selected(self):
        """Delete selected rows from database"""
        # Get selected rows
        selected_rows = self.table_view.selectionModel().selectedRows()
        
        if not selected_rows:
            self.show_error("No rows selected.")
            return
        
        # Confirm deletion
        confirm = QMessageBox()
        confirm.setIcon(QMessageBox.Warning)
        confirm.setWindowTitle("Confirm Deletion")
        confirm.setText(f"Are you sure you want to delete {len(selected_rows)} selected rows?")
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
                # Get source model and data
                source_model = self.proxy_model.sourceModel()
                df = source_model._data
                
                # Get indices in original dataframe
                indices_to_delete = []
                for index in selected_rows:
                    source_index = self.proxy_model.mapToSource(index)
                    indices_to_delete.append(source_index.row())
                
                # Get IDs to delete
                ids_to_delete = df.iloc[indices_to_delete]['id'].tolist()
                
                # Delete from database
                conn = self.db_manager.db_path
                import sqlite3
                conn = sqlite3.connect(conn)
                cursor = conn.cursor()
                
                for id_val in ids_to_delete:
                    cursor.execute("DELETE FROM crab_population WHERE id = ?", (id_val,))
                
                conn.commit()
                conn.close()
                
                # Reload data
                self.load_data()
                
                self.show_success(f"Successfully deleted {len(ids_to_delete)} rows.")
                
            except Exception as e:
                self.show_error(f"Error deleting data: {str(e)}")
    
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