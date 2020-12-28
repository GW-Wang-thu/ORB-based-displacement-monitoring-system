from PyQt5.Qt import *
import sys

class MyW(QWidget):

    def __init__(self):
        super().__init__()
        self.move(600, 150)
        self.setWindowTitle('GetPoint')
        self.setMinimumSize(300, 200)
        self.setup_ui()

    def setup_ui(self):
        btn = QPushButton(self)
        btn.move(20, 20)
        btn.resize(100, 30)
        btn.setText('Test')
        print(QCursor.pos())

app = QApplication(sys.argv)
myw = MyW()
myw.show()
sys.exit(app.exec_())