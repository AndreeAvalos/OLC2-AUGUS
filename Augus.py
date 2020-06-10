import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
from interfaz import Interfaz

class Augus(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Interfaz()
        self.ui.setupUi(self)
        self.show()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()

    ui = Interfaz()
    ui.setupUi(MainWindow)
    

    MainWindow.show()
    sys.exit(app.exec_())
