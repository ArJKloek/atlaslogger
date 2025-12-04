import sys
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    """Main application window for Atlas Logger."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface from the UI file."""
        # Get the path to the UI file
        ui_dir = Path(__file__).parent / "ui"
        ui_file = ui_dir / "main.ui"
        
        # Compile UI file to Python module
        ui_module_path = ui_dir / "main_ui.py"
        
        try:
            # Use pyuic6 to convert .ui to .py
            subprocess.run(
                ["pyuic6", str(ui_file), "-o", str(ui_module_path)],
                check=True,
                capture_output=True
            )
        except FileNotFoundError:
            print("Error: pyuic6 not found. Install it with: pip install PyQt6-tools")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"Error compiling UI file: {e.stderr.decode()}")
            sys.exit(1)
        
        # Import the generated UI module
        import importlib.util
        spec = importlib.util.spec_from_file_location("main_ui", ui_module_path)
        ui_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ui_module)
        
        # Create a central widget and setup the UI
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Setup the UI
        self.ui = ui_module.Ui_MainWindow()
        self.ui.setupUi(self)


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
