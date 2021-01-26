import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sip
import os
sys.path.append('..')
from Koginator import koginator
from FeatureSearch.feature_search import FeatureSearch
from Clustering.getname import GetNameJ
from Clustering.main import search_lectures

APP_TITLE = "東工大講義推薦システム"
kg = None


class MainWindow(QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.horizontal = QHBoxLayout()
        self.vertical = QVBoxLayout()

        # ボタンの追加
        self.btn_koginator = QPushButton('コギネーター', self)
        self.btn_koginator.setObjectName('btn-koginator')
        self.btn_koginator.setFont(QtGui.QFont('Meiryo', 18))
        self.btn_koginator.clicked.connect(self.exec_koginator)
        self.horizontal.addWidget(self.btn_koginator)

        self.btn_search = QPushButton('講義検索', self)
        self.btn_search.setObjectName('btn-search')
        self.btn_search.setFont(QtGui.QFont('Meiryo', 18))
        self.btn_search.clicked.connect(self.exec_search)
        self.horizontal.addWidget(self.btn_search)

        self.vertical.addLayout(self.horizontal)
        self.setLayout(self.vertical)

        self.setGeometry(300, 50, 400, 350)
        self.setWindowTitle(APP_TITLE)

    def exec_koginator(self):
        change_window("koginator")

    def exec_search(self):
        change_window("search")


class KoginatorWindow(QWidget):

    def __init__(self, parent=None):
        super(KoginatorWindow, self).__init__(parent)

        self.horizontal = QHBoxLayout()
        self.vertical = QVBoxLayout()

        self.setGeometry(300, 50, 400, 350)
        self.setWindowTitle(APP_TITLE + "｜コギネーター")


class KeywordSearchWindow(QWidget):

    def __init__(self, parent=None):
        super(KeywordSearchWindow, self).__init__(parent)

        self.horizontal = QHBoxLayout()
        self.vertical = QVBoxLayout()

        self.label = QLabel(self)
        self.label.setText("キーワードを入力してください")
        self.label.setFixedHeight(15)
        self.vertical.addWidget(self.label)

        self.textbox = QLineEdit(self)
        self.vertical.addWidget(self.textbox)

        self.btn = QPushButton('検索', self)
        self.btn.clicked.connect(self.exec_search)
        self.vertical.addWidget(self.btn)

        self.horizontal.addLayout(self.vertical)
        self.setLayout(self.horizontal)

        self.setGeometry(300, 50, 400, 350)
        self.setWindowTitle(APP_TITLE + "｜講義検索")

    def exec_search(self):
        global main_window
        result = search_lectures(self.textbox.text())
        main_window = FeatureSearchWindow(lec_code=result)
        main_window.show()


class FeatureSearchWindow(QWidget):
    fs = None

    def __init__(self, parent=None, lec_code=[]):
        super(FeatureSearchWindow, self).__init__(parent)
        self.fs = FeatureSearch(lec_code)
        self.setGeometry(300, 50, 400, 350)
        self.setWindowTitle(APP_TITLE)

        self.title = QLabel(self)
        self.title.setText('特徴量検索')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QtGui.QFont("Meiryo", 14, QtGui.QFont.Bold))
        self.title.setFixedHeight(50)

        self.course_layout = QVBoxLayout()
        self.course_title = QLabel(self)
        self.course_title.setText("開講元")
        self.course_title.setFont(QtGui.QFont("Meiryo", 14))
        self.course_title.setFixedHeight(15)
        self.course = QComboBox()
        self.course.addItem("選択しない")
        self.course.addItems(self.fs.course)
        self.course_layout.addWidget(self.course_title)
        self.course_layout.addWidget(self.course)

        self.day_layout = QVBoxLayout()
        self.day_title = QLabel(self)
        self.day_title.setText("曜日")
        self.day_title.setFixedHeight(15)
        self.day_layout2 = QHBoxLayout()
        self.day = []
        for day in self.fs.day:
            self.day.append(QCheckBox(day, self))
        for widget in self.day:
            self.day_layout2.addWidget(widget)
        self.day_layout.addWidget(self.day_title)
        self.day_layout.addLayout(self.day_layout2)

        self.period_layout = QVBoxLayout()
        self.period_title = QLabel(self)
        self.period_title.setText("開講時限")
        self.period_title.setFixedHeight(15)
        self.period_layout2 = QHBoxLayout()
        self.period = []
        for period in range(len(self.fs.period)):
            self.period.append(QCheckBox(str(period + 1) + "限", self))
        for widget in self.period:
            self.period_layout2.addWidget(widget)
        self.period_layout.addWidget(self.period_title)
        self.period_layout.addLayout(self.period_layout2)

        self.quarter_layout = QVBoxLayout()
        self.quarter_title = QLabel(self)
        self.quarter_title.setText("開講クォーター")
        self.quarter_title.setFixedHeight(15)
        self.quarter_layout2 = QHBoxLayout()
        self.quarter = []
        for quarter in self.fs.quarter:
            self.quarter.append(QCheckBox(quarter + "Q", self))
        for widget in self.quarter:
            self.quarter_layout2.addWidget(widget)
        self.quarter_layout.addWidget(self.quarter_title)
        self.quarter_layout.addLayout(self.quarter_layout2)

        self.textbook_layout = QHBoxLayout()
        self.textbook_title = QLabel(self)
        self.textbook_title.setText('教科書の有無')
        self.textbook_title.setFixedHeight(15)
        self.textbook = []
        self.textbook.append(QCheckBox("あり", self))
        self.textbook.append(QCheckBox("なし", self))
        self.textbook_group = QButtonGroup()
        for btn in self.textbook:
            self.textbook_group.addButton(btn)
        self.textbook_layout.addWidget(self.textbook_title)
        for checkbox in self.textbook:
            self.textbook_layout.addWidget(checkbox)

        self.exam_layout = QHBoxLayout()
        self.exam_title = QLabel(self)
        self.exam_title.setText('試験の有無')
        self.exam_title.setFixedHeight(15)
        self.exam = []
        self.exam.append(QCheckBox("あり", self))
        self.exam.append(QCheckBox("なし", self))
        self.exam_group = QButtonGroup()
        for btn in self.exam:
            self.exam_group.addButton(btn)
        self.exam_layout.addWidget(self.exam_title)
        for checkbox in self.exam:
            self.exam_layout.addWidget(checkbox)

        self.report_layout = QHBoxLayout()
        self.report_title = QLabel(self)
        self.report_title.setText('レポートの有無')
        self.report_title.setFixedHeight(15)
        self.report = []
        self.report.append(QCheckBox("あり", self))
        self.report.append(QCheckBox("なし", self))
        self.report_group = QButtonGroup()
        for btn in self.report:
            self.report_group.addButton(btn)
        self.report_layout.addWidget(self.report_title)
        for checkbox in self.report:
            self.report_layout.addWidget(checkbox)

        self.presentation_layout = QHBoxLayout()
        self.presentation_title = QLabel(self)
        self.presentation_title.setText('プレゼンの有無')
        self.presentation_title.setFixedHeight(15)
        self.presentation = []
        self.presentation.append(QCheckBox("あり", self))
        self.presentation.append(QCheckBox("なし", self))
        self.presentation_group = QButtonGroup()
        for btn in self.presentation:
            self.presentation_group.addButton(btn)
        self.presentation_layout.addWidget(self.presentation_title)
        for checkbox in self.presentation:
            self.presentation_layout.addWidget(checkbox)

        self.btnExit = QPushButton('決定', self)
        self.btnExit.setObjectName('btnKoginator')
        self.btnExit.setFont(QtGui.QFont('Meiryo', 14, QtGui.QFont.Bold))
        self.btnExit.clicked.connect(self.set_variables)
        self.btnLayout = QHBoxLayout()
        self.btnLayout.addWidget(self.btnExit)

        self.vertical = QVBoxLayout()
        self.vertical.addWidget(self.title)
        self.vertical.addLayout(self.course_layout)
        self.vertical.addLayout(self.day_layout)
        self.vertical.addLayout(self.period_layout)
        self.vertical.addLayout(self.quarter_layout)
        self.vertical.addLayout(self.textbook_layout)
        self.vertical.addLayout(self.exam_layout)
        self.vertical.addLayout(self.report_layout)
        self.vertical.addLayout(self.presentation_layout)
        self.vertical.addLayout(self.btnLayout)
        self.setLayout(self.vertical)

    def set_variables(self):
        self.fs.course_num = self.course.currentIndex() - 1
        self.fs.day_select = []
        for day in self.day:
            if day.isChecked():
                self.fs.day_select.append(1)
            else:
                self.fs.day_select.append(0)
        self.fs.period_select = []
        for period in self.period:
            if period.isChecked():
                self.fs.period_select.append(1)
            else:
                self.fs.period_select.append(0)
        self.fs.quarter_select = []
        for quarter in self.quarter:
            if quarter.isChecked():
                self.fs.quarter_select.append(1)
            else:
                self.fs.quarter_select.append(0)

        self.fs.is_need_textbook = -1
        if self.textbook[0].isChecked():
            self.fs.is_need_textbook = 1
        elif self.textbook[1].isChecked():
            self.fs.is_need_textbook = 0

        self.fs.is_need_assessment[0] = -1
        if self.exam[0].isChecked():
            self.fs.is_need_assessment[0] = 1
        elif self.exam[1].isChecked():
            self.fs.is_need_assessment[0] = 0

        self.fs.is_need_assessment[1] = -1
        if self.report[0].isChecked():
            self.fs.is_need_assessment[1] = 1
        elif self.report[1].isChecked():
            self.fs.is_need_assessment[1] = 0

        self.fs.is_need_assessment[2] = -1
        if self.presentation[0].isChecked():
            self.fs.is_need_assessment[2] = 1
        elif self.presentation[1].isChecked():
            self.fs.is_need_assessment[2] = 0

        self.result = self.fs.get_index_list()
        self.show_answer()

    def show_answer(self):
        global main_window
        main_window = AnswerWindow(fs=self.fs)
        main_window.show()


class AnswerWindow(QWidget):
    def __init__(self, parent=None, fs=None):
        super(AnswerWindow, self).__init__(parent)
        self.setGeometry(300, 50, 400, 350)
        self.setWindowTitle(APP_TITLE)
        self.answer = QLabel(self)
        ans = ''
        for x in fs.get_index_list():
            if ans == '':
                ans = fs.d[x]['講義名']['日本語']
            else:
                ans = ans + '\n' + fs.d[x]['講義名']['日本語']
        self.answer.setText(ans)
        self.answer.setAlignment(Qt.AlignCenter)
        self.answer.setFont(QtGui.QFont("Meiryo", 14))
        #  self.answer.setFixedHeight(100)

        self.title = QLabel(self)
        self.title.setText('推薦講義')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QtGui.QFont("Meiryo", 14, QtGui.QFont.Bold))
        self.title.setFixedHeight(50)

        self.btnExit = QPushButton('終了', self)
        self.btnExit.setObjectName('btnKoginator')
        self.btnExit.setFont(QtGui.QFont('Meiryo', 14, QtGui.QFont.Bold))
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


class KoginatorQuestionWindow(QWidget):
    def __init__(self, parent=None, newQ=''):
        super(KoginatorQuestionWindow, self).__init__(parent)

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
        next_koginator_window()


class KoginatorAnswerWindow(QWidget):
    def __init__(self, parent=None):
        super(KoginatorAnswerWindow, self).__init__(parent)
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


def change_window(w):
    global main_window
    global kg
    if w == "koginator":
        kg = koginator.koginator()
        main_window = KoginatorQuestionWindow(None, kg.getQuestion())
    elif w == "search":
        main_window = KeywordSearchWindow()
    main_window.show()


def next_koginator_window():
    global main_window
    main_window = KoginatorQuestionWindow(None, kg.getQuestion())
    main_window.show()


def show_answer():
    global main_window
    main_window = KoginatorAnswerWindow()
    main_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    try:
        styleFile = os.path.join(os.path.dirname(__file__), 'style.qss')
        with open(styleFile, 'r') as f:
            style = f.read()
    except BaseException:
        style = ''

    app.setStyleSheet(style)
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
