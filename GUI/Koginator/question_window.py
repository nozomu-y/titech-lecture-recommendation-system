import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sip

APP_TITLE = "コギネーター"

class MainWindow(QWidget):
    def __init__(self, parent = None, newQ = ''):
        super(MainWindow, self).__init__(parent)

        self.vertical = QVBoxLayout()
        self.setLayout(self.vertical)

        self.setGeometry(300, 50, 400, 350)
        self.setWindowTitle(APP_TITLE)

        self.question = QLabel(self)
        self.setQuestion(newQ)
        self.question.setAlignment(Qt.AlignCenter)
        self.question.setFont(QtGui.QFont("メイリオ", 14, QtGui.QFont.Bold))
        self.question.setFixedHeight(20)

        self.layoutAns = QHBoxLayout()
        self.yes = QCheckBox('はい', self)
        self.mid = QCheckBox('わからない', self)
        self.no = QCheckBox('いいえ', self)
        self.groupAns = QButtonGroup()
        self.groupAns.addButton(self.yes)
        self.groupAns.addButton(self.mid)
        self.groupAns.addButton(self.no)
        self.layoutAns.addWidget(self.yes)
        self.layoutAns.addWidget(self.mid)
        self.layoutAns.addWidget(self.no)   

        self.btnLayout = QHBoxLayout()
        self.btnNext = QPushButton('次へ', self)
        self.btnNext.setObjectName('btnNext')
        self.btnNext.setFont(QtGui.QFont('メイリオ', 14, QtGui.QFont.Bold))

        self.btnLayout.addWidget(self.btnNext)
        self.btnNext.clicked.connect(self.btnNextClicked)


        self.vertical.addWidget(self.question)
        self.vertical.addLayout(self.layoutAns)
        self.vertical.addLayout(self.btnLayout)

    
    def setQuestion(self, newQ):
        self.question.setText(newQ)

    def btnNextClicked(self):
        if(self.yes.isChecked()):
            self.ans = 5
        elif(self.mid.isChecked()):
            self.ans = 3
        elif(self.no.isChecked()):
            self.ans = 1
        else:
            return
        print('answer : ' + str(self.ans))
        change_window('質問')

def change_window(newQ):
    global main_window
    main_window = MainWindow(None, newQ)
    main_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    try:
        styleFile = os.path.join(os.path.dirname(__file__), '../style.qss')
        with open(styleFile, 'r') as f:
            style = f.read()
    except:
        style = ''
    app.setStyleSheet(style)
    main_window = MainWindow(None, '質問')
    main_window.show()
    sys.exit(app.exec_())
        