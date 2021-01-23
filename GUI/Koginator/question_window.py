import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sip
rootFile = os.path.join(os.path.dirname(__file__), '../..')
sys.path.append(rootFile)
import Koginator.koginator as koginator

APP_TITLE = "コギネーター"
kg = koginator.koginator()

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
        self.btnNext.setObjectName('btnKoginator')
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
            self.ans = '5'
        elif(self.mid.isChecked()):
            self.ans = '3'
        elif(self.no.isChecked()):
            self.ans = '1'
        else:
            return
        print('answer : ' + self.ans)
        if(kg.getAnswer(self.ans)):
            kg.printAnswer()
            show_answer()
            return
        change_window()

class AnswerWindow(QWidget):
    def __init__(self, parent=None):
        super(AnswerWindow, self).__init__(parent)
        self.setGeometry(300, 50, 400, 350)
        self.setWindowTitle(APP_TITLE)
        self.answer = QLabel(self)
        ans = ''
        for kgans in kg.answer:
            if ans == '':
                ans = ans + kgans
            else:
                ans = ans + '\n\n' + kgans
        self.answer.setText(ans)
        self.answer.setAlignment(Qt.AlignCenter)
        self.answer.setFont(QtGui.QFont("メイリオ", 14, QtGui.QFont.Bold))
        self.answer.setFixedHeight(100)

        self.title = QLabel(self)
        self.title.setText('推薦講義')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QtGui.QFont("メイリオ", 14, QtGui.QFont.Bold))
        self.title.setFixedHeight(50)

        self.btnExit = QPushButton('終了', self)
        self.btnExit.setObjectName('btnKoginator')
        self.btnExit.setFont(QtGui.QFont('メイリオ', 14, QtGui.QFont.Bold))
        self.btnExit.clicked.connect(sys.exit)
        self.btnLayout = QHBoxLayout()
        self.btnLayout.addWidget(self.btnExit)


        self.vertical = QVBoxLayout()
        self.horizon = QHBoxLayout()
        self.horizon.addWidget(self.answer)
        self.vertical.addWidget(self.title)
        self.vertical.addLayout(self.horizon)
        self.vertical.addLayout(self.btnLayout)
        self.setLayout(self.vertical)


    

def change_window():
    global main_window
    main_window = MainWindow(None, kg.getQuestion())
    main_window.show()

def show_answer():
    global main_window
    main_window = AnswerWindow()
    main_window.show()
    
def initKoginator():
    kg = koginator.koginator()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    try:
        styleFile = os.path.join(os.path.dirname(__file__), '../style.qss')
        with open(styleFile, 'r') as f:
            style = f.read()
    except:
        style = ''
    app.setStyleSheet(style)
    main_window = MainWindow(None, kg.getQuestion())
    main_window.show()
    sys.exit(app.exec_())
        