# import sys
# import requests
# from PySide6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QScrollArea, QGridLayout,
#     QPushButton, QLabel, QFrame, QHBoxLayout
# )
# from PySide6.QtCore import Qt

# API_URL = "http://localhost:8000/"

# class ItemCard(QWidget):
#     def __init__(self, item_data, parent):
#         super().__init__()
#         self.parent = parent
#         self.name = item_data[0]
#         self.quantity = item_data[5]
#         self.setFixedSize(250, 150)
#         layout = QVBoxLayout()
        
#         self.name_label = QLabel(f"Name: {self.name}")
#         type_label = QLabel(f"Type: {item_data[1]}")
#         self.quantity_label = QLabel(f"Quantity: {self.quantity}")
        
#         button_layout = QHBoxLayout()
#         self.plus_button = QPushButton("+")
#         self.minus_button = QPushButton("-")
#         self.plus_button.clicked.connect(self.increment_quantity)
#         self.minus_button.clicked.connect(self.decrement_quantity)
#         button_layout.addWidget(self.minus_button)
#         button_layout.addWidget(self.plus_button)
        
#         layout.addWidget(self.name_label)
#         layout.addWidget(type_label)
#         layout.addWidget(self.quantity_label)
#         layout.addLayout(button_layout)
        
#         self.setLayout(layout)
#         self.setStyleSheet("border: 1px solid black; border-radius: 10px; padding: 5px;")
    
#     def update_quantity(self, new_quantity):
#         if new_quantity <= 0:
#             self.remove_item()
#         else:
#             response = requests.post(f"{API_URL}update-quantity?name={self.name}&new_quantity={new_quantity}")
#             if response.status_code == 200:
#                 self.quantity = new_quantity
#                 self.quantity_label.setText(f"Quantity: {self.quantity}")
    
#     def increment_quantity(self):
#         self.update_quantity(self.quantity + 1)
    
#     def decrement_quantity(self):
#         self.update_quantity(self.quantity - 1)
    
#     def remove_item(self):
#         response = requests.delete(f"{API_URL}remove-item?name={self.name}")
#         if response.status_code == 200:
#             self.setParent(None)
#             self.parent.load_data()

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("API Data Viewer")
#         self.setGeometry(100, 100, 1300, 600)
        
#         main_layout = QVBoxLayout()
#         self.refresh_button = QPushButton("REFRESH")
#         self.refresh_button.clicked.connect(self.load_data)
#         main_layout.addWidget(self.refresh_button)
        
#         self.scroll_area = QScrollArea()
#         self.scroll_area.setWidgetResizable(True)
#         self.content_widget = QWidget()
#         self.grid_layout = QGridLayout()
#         self.grid_layout.setSpacing(10)
#         self.content_widget.setLayout(self.grid_layout)
#         self.scroll_area.setWidget(self.content_widget)
        
#         main_layout.addWidget(self.scroll_area)
#         self.setLayout(main_layout)
        
#         self.load_data()
    
#     def load_data(self):
#         try:
#             response = requests.get(API_URL, headers={"Content-Type": "application/json"})
#             data = response.json()
#             rows = data.get("rows", [])
            
#             for i in reversed(range(self.grid_layout.count())):
#                 self.grid_layout.itemAt(i).widget().setParent(None)
            
#             for index, item in enumerate(rows):
#                 row = index // 5
#                 col = index % 5
#                 self.grid_layout.addWidget(ItemCard(item, self), row, col)
#         except Exception as e:
#             print("Error fetching data:", e)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())

import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QScrollArea, QGridLayout,
    QPushButton, QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt, QThread, Signal

API_URL = "http://localhost:8000/"

class APICallThread(QThread):
    result_signal = Signal(dict)

    def __init__(self, url, method='get', parent=None):
        super().__init__(parent)
        self.url = url
        self.method = method

    def run(self):
        try:
            if self.method == 'post':
                response = requests.post(self.url)
            elif self.method == 'delete':
                response = requests.delete(self.url)
            else:
                response = requests.get(self.url, headers={"Content-Type": "application/json"})
            
            if response.status_code == 200:
                self.result_signal.emit(response.json())
        except Exception as e:
            print("Error in API request:", e)

class ItemCard(QWidget):
    def __init__(self, item_data, parent):
        super().__init__()
        self.parent = parent
        self.name = item_data[0]
        self.quantity = item_data[5]
        self.setFixedSize(250, 150)
        layout = QVBoxLayout()
        
        self.name_label = QLabel(f"Name: {self.name}")
        type_label = QLabel(f"Type: {item_data[1]}")
        self.quantity_label = QLabel(f"Quantity: {self.quantity}")
        
        button_layout = QHBoxLayout()
        self.plus_button = QPushButton("+")
        self.minus_button = QPushButton("-")
        self.plus_button.clicked.connect(self.increment_quantity)
        self.minus_button.clicked.connect(self.decrement_quantity)
        button_layout.addWidget(self.minus_button)
        button_layout.addWidget(self.plus_button)
        
        layout.addWidget(self.name_label)
        layout.addWidget(type_label)
        layout.addWidget(self.quantity_label)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("border: 1px solid black; border-radius: 10px; padding: 5px;")
        
        self.threads = []  # Store running threads
    
    def update_quantity(self, new_quantity):
        if new_quantity <= 0:
            thread = APICallThread(f"{API_URL}remove-item?name={self.name}", method='delete', parent=self)
            thread.result_signal.connect(lambda _: self.parent.load_data())
        else:
            thread = APICallThread(f"{API_URL}update-quantity?name={self.name}&new_quantity={new_quantity}", method='post', parent=self)
            thread.result_signal.connect(lambda _: self.set_quantity(new_quantity))
        
        self.threads.append(thread)
        thread.start()
    
    def set_quantity(self, new_quantity):
        self.quantity = new_quantity
        self.quantity_label.setText(f"Quantity: {self.quantity}")
    
    def increment_quantity(self):
        self.update_quantity(self.quantity + 1)
    
    def decrement_quantity(self):
        self.update_quantity(self.quantity - 1)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("API Data Viewer")
        self.setGeometry(100, 100, 1300, 600)
        
        main_layout = QVBoxLayout()
        self.refresh_button = QPushButton("REFRESH")
        self.refresh_button.clicked.connect(self.load_data)
        main_layout.addWidget(self.refresh_button)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        self.content_widget.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.content_widget)
        
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)
        
        self.threads = []  # Store running threads
        self.load_data()
    
    def load_data(self):
        thread = APICallThread(API_URL, parent=self)
        thread.result_signal.connect(self.populate_data)
        self.threads.append(thread)
        thread.start()
    
    def populate_data(self, data):
        rows = data.get("rows", [])
        
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)
        
        for index, item in enumerate(rows):
            row = index // 5
            col = index % 5
            self.grid_layout.addWidget(ItemCard(item, self), row, col)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

