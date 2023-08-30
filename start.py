from PySide6.QtCore import Qt, Slot
import PySide6.QtWidgets as Wi
import client
import server
import sys


class FoxKVM(Wi.QWidget):
    def __init__(self):
        Wi.QWidget.__init__(self)
        
        self.setWindowTitle("FoxKVM")
        self.setGeometry(100, 100, 200, 230)
        
        self.typeClient = Wi.QRadioButton("Client")
        self.typeClient.clicked.connect(self.upd_page)
        self.typeClient.toggle()
        
        self.typeServer = Wi.QRadioButton("Server")
        self.typeServer.clicked.connect(self.upd_page)
        
        self.message = Wi.QLabel("Select connection type:")
        self.message.alignment = Qt.AlignCenter

        self.layout = Wi.QVBoxLayout(self)
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.typeClient)
        self.layout.addWidget(self.typeServer)

        # Creating a stacked widget to manage different pages
        self.stacked_widget = Wi.QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Creating separate widgets for client and server pages
        self.client_page = Wi.QWidget()
        self.client_page_layout = Wi.QVBoxLayout(self.client_page)
        self.IPEntry = Wi.QLineEdit("")
        self.IPEntry.setPlaceholderText("Server local IP")
        self.client_page_layout.addWidget(self.IPEntry)
        self.PortEntry = Wi.QLineEdit("5001")
        self.PortEntry.setPlaceholderText("PORT")
        self.client_page_layout.addWidget(self.PortEntry)
        self.ConnectButton = Wi.QPushButton("Connect to server")
        self.ConnectButton.clicked.connect(self.connect_to_server)
        self.client_page_layout.addWidget(self.ConnectButton)

        self.server_page = Wi.QWidget()
        self.server_page_layout = Wi.QVBoxLayout(self.server_page)
        
        self.hotkey_button = Wi.QPushButton("Hotkey: ")
        
        self.server_page_layout.addWidget(self.hotkey_button)
        
        self.server_page_layout.addWidget(self.hotkey_button)
        self.ServerPortEntry = Wi.QLineEdit("5001")
        self.ServerPortEntry.setPlaceholderText("PORT")
        self.server_page_layout.addWidget(self.ServerPortEntry)
        self.StartButton = Wi.QPushButton("Start server")
        self.StartButton.clicked.connect(self.start_server)
        self.server_page_layout.addWidget(self.StartButton)

        self.stacked_widget.addWidget(self.client_page)
        self.stacked_widget.addWidget(self.server_page)

        self.upd_page()  # Call this initially to set up the UI

    def on_hotkey_button_click(self):
        self.hotkey_button.setText("Press new hotkey")
        
    def upd_page(self):
        if self.typeClient.isChecked():
            print("Client")
            self.stacked_widget.setCurrentWidget(self.client_page)
        else:
            self.stacked_widget.setCurrentWidget(self.server_page)
            print("Server")

    @Slot()
    def connect_to_server(self):
        client_instance = client.ClientStart()
        client_instance.start(int(self.PortEntry.text()), self.IPEntry.text())
        
    @Slot()
    def start_server(self):
        server_instance = server.ServerStart()
        server_instance.start(int(self.ServerPortEntry.text()))


if __name__ == "__main__":
    app = Wi.QApplication(sys.argv)

    widget = FoxKVM()
    widget.show()

    sys.exit(app.exec())
