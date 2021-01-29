import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import PyQt5.sip

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.upper = QCheckBox('大文字', self)
        self.upper.move(100, 30)
        self.upper.stateChanged.connect(self.uppercase)

        self.horizon = QHBoxLayout()

        self.vertical = QVBoxLayout()

        self.button = QPushButton('excute', self)
        self.button.clicked.connect(self.output)

        self.horizon.addLayout(self.vertical)
        self.setLayout(self.horizon)

        self.setGeometry(300, 50, 400, 350)
        self.setWindowTitle('QCheckBox')

    def uppercase(self):
        if(self.upper.isChecked()):
            self.a = QCheckBox('A', self)
            self.vertical.addWidget(self.a)

            self.b = QCheckBox('B', self)
            self.vertical.addWidget(self.b)
        else:
            self.vertical.removeWidget(self.a)
            self.vertical.removeWidget(self.b)
            '''
        self.group = QButtonGroup()  ###group化によって一つしか選べなくなる。
        self.group.addButton(self.a, 1)
        self.group.addButton(self.b, 2)
'''
    def output(self):
        outputs = []
        if(self.a.isChecked()):
            outputs.append("A")
        if(self.b.isChecked()):
            outputs.append("B")
 
        for output in outputs:
            print(output)
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())