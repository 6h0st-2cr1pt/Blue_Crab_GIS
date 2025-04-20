import sys
from PyQt5.QtWidgets import QApplication
from splash_screen import SplashScreen
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Show splash screen
    splash = SplashScreen()
    splash.show()
    
    # Create main window but don't show it yet
    main_window = MainWindow()
    
    # Connect splash screen finished signal to show main window
    splash.splash_finished.connect(lambda: main_window.show())
    
    # Start the splash screen timer
    splash.start_timer()
    
    sys.exit(app.exec_())