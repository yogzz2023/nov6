import sys
import numpy as np
import math
import csv
import matplotlib.pyplot as plt
import mplcursors
from scipy.stats import chi2
from scipy.optimize import linear_sum_assignment
from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QTextEdit,
                             QHBoxLayout, QSplitter, QCheckBox, QLineEdit, QDialog, QGridLayout, QGroupBox, QRadioButton,
                             QFrame, QSizePolicy, QToolButton, QTabWidget, QMenu, QAction, QTableWidgetItem, QScrollArea)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject
import socket
import threading
import queue

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

# Custom stream class to redirect stdout
class OutputStream:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, text):
        self.text_edit.append(text)

    def flush(self): 
        pass  # No need to implement flush for QTextEdit

# Define a queue for thread-safe communication
measurement_queue = queue.Queue()

# UDP Receiver Thread
def udp_receiver(port=5005):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port))
    print(f"Listening for UDP packets on port {port}...")
    while True:
        data, _ = sock.recvfrom(1024)
        measurement = data.decode('utf-8').strip().split(',')
        measurement_queue.put(measurement)

# Kalman Filter and other classes remain unchanged...

class KalmanFilterGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.tracks = []
        self.selected_track_ids = set()
        self.initUI()
        self.control_panel_collapsed = False  # Start with the panel expanded

        # Start the UDP receiver thread
        self.udp_thread = threading.Thread(target=udp_receiver, daemon=True)
        self.udp_thread.start()

        # Start the processing thread
        self.processing_thread = threading.Thread(target=self.process_measurements, daemon=True)
        self.processing_thread.start()

    def process_measurements(self):
        while True:
            if not measurement_queue.empty():
                measurement = measurement_queue.get()
                # Process the measurement
                # Convert measurement to appropriate format and update tracks
                # Example: self.update_tracks(measurement)
                print(f"Processing measurement: {measurement}")
                # Update the plot with new data
                self.update_plot()

    # Rest of the KalmanFilterGUI class remains unchanged...

# Main application code remains unchanged...

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = KalmanFilterGUI()
    ex.show()
    sys.exit(app.exec_())
