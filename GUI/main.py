# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sip
import os
sysFile = os.path.dirname(os.path.abspath(__file__))
sys.path.append(sysFile + '/..')
from Koginator import koginator
from FeatureSearch.feature_search import FeatureSearch
from Clustering.getname import GetNameJ
from Clustering.main import search_lectures


APP_TITLE = "東工大講義推薦システム"
kg = None
window_x = 500
window_y = 200
window_w = 500
window_h = 350


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

        self.setGeometry(window_x, window_y, window_w, window_h)
        self.setWindowTitle(APP_TITLE)

    def exec_koginator(self):
        change_window("koginator")

    def exec_search(self):
        change_window("search")


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
        self.btn.setObjectName('btnKoginator')
        self.btnLayout = QHBoxLayout()
        self.btnLayout.addWidget(self.btn)
        self.vertical.addLayout(self.btnLayout)
        # self.vertical.addWidget(self.btn)

        self.horizontal.addLayout(self.vertical)
        self.setLayout(self.horizontal)

        self.setGeometry(window_x, window_y, window_w, window_h)
        self.setWindowTitle(APP_TITLE + "｜講義検索")

        self.btnTop = QPushButton('TOP', self)
        self.btnTop.setObjectName('btnTop')
        self.btnTop.setFont(QtGui.QFont('Meiryo', 10, QtGui.QFont.Bold))
        self.btnTop.move(5, 5)
        self.btnTop.clicked.connect(returnTop)

    def exec_search(self):
        global main_window
        global window_x
        global window_y
        global search_result
        window_x = main_window.x()
        window_y = main_window.y() + 22
        search_result = search_lectures(self.textbox.text())
        result = []
        for results in search_result:
            for item in results:
                result.append(item)
        main_window = FeatureSearchWindow(lec_code=result)
        main_window.show()


class FeatureSearchWindow(QWidget):
    fs = None

    def __init__(self, parent=None, lec_code=[]):
        super(FeatureSearchWindow, self).__init__(parent)
        self.fs = FeatureSearch(lec_code)
        self.setGeometry(window_x, window_y, window_w, window_h)
        self.setWindowTitle(APP_TITLE + ' | 講義検索')

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
        self.day_layout1 = QHBoxLayout()
        self.day_title = QLabel(self)
        self.day_title.setText("曜日")
        self.day_title.setFixedHeight(15)
        self.day_selectAll = QCheckBox("全選択", self)
        self.day_selectAll.stateChanged.connect(self.selectAll_day)
        self.day_layout1.addWidget(self.day_title)
        self.day_layout1.addWidget(self.day_selectAll)
        self.day_layout.addLayout(self.day_layout1)
        self.day_layout2 = QHBoxLayout()
        self.day = []
        for day in self.fs.day:
            self.day.append(QCheckBox(day, self))
        for widget in self.day:
            widget.stateChanged.connect(self.day_checked)
            self.day_layout2.addWidget(widget)
        self.day_layout.addLayout(self.day_layout2)

        self.period_layout = QVBoxLayout()
        self.period_layout1 = QHBoxLayout()
        self.period_title = QLabel(self)
        self.period_title.setText("開講時限")
        self.period_title.setFixedHeight(15)
        self.period_selectAll = QCheckBox("全選択", self)
        self.period_selectAll.stateChanged.connect(self.selectAll_period)
        self.period_layout1.addWidget(self.period_title)
        self.period_layout1.addWidget(self.period_selectAll)
        self.period_layout.addLayout(self.period_layout1)
        self.period_layout2 = QHBoxLayout()
        self.period = []
        for period in range(len(self.fs.period)):
            self.period.append(QCheckBox(str(period + 1) + "限", self))
        for widget in self.period:
            widget.stateChanged.connect(self.period_checked)
            self.period_layout2.addWidget(widget)
        self.period_layout.addLayout(self.period_layout2)

        self.quarter_layout = QVBoxLayout()
        self.quarter_layout1 = QHBoxLayout()
        self.quarter_title = QLabel(self)
        self.quarter_title.setText("開講クォーター")
        self.quarter_title.setFixedHeight(15)
        self.quarter_selectAll = QCheckBox("全選択", self)
        self.quarter_selectAll.stateChanged.connect(self.selectAll_quarter)
        self.quarter_layout1.addWidget(self.quarter_title)
        self.quarter_layout1.addWidget(self.quarter_selectAll)
        self.quarter_layout.addLayout(self.quarter_layout1)
        self.quarter_layout2 = QHBoxLayout()
        self.quarter = []
        for quarter in self.fs.quarter:
            self.quarter.append(QCheckBox(quarter + "Q", self))
        for widget in self.quarter:
            widget.stateChanged.connect(self.quarter_checked)
            self.quarter_layout2.addWidget(widget)
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

        self.btnTop = QPushButton('TOP', self)
        self.btnTop.setObjectName('btnTop')
        self.btnTop.setFont(QtGui.QFont('Meiryo', 10, QtGui.QFont.Bold))
        self.btnTop.move(5, 5)
        self.btnTop.clicked.connect(returnTop)

    def selectAll_day(self, state):
        if state == Qt.Checked:
            for checkbox in self.day:
                checkbox.stateChanged.disconnect()
                checkbox.setChecked(True)
            for checkbox in self.day:
                checkbox.stateChanged.connect(self.day_checked)
        elif state == Qt.Unchecked:
            for checkbox in self.day:
                checkbox.setChecked(False)

    def day_checked(self):
        all_checked = True
        all_unchecked = True
        for checkbox in self.day:
            if checkbox.isChecked():
                all_unchecked = False
            else:
                all_checked = False
        if all_checked:
            self.day_selectAll.setCheckState(Qt.Checked)
        elif all_unchecked:
            self.day_selectAll.setCheckState(Qt.Unchecked)
        else:
            self.day_selectAll.setCheckState(Qt.PartiallyChecked)

    def selectAll_period(self, state):
        if state == Qt.Checked:
            for checkbox in self.period:
                checkbox.stateChanged.disconnect()
                checkbox.setChecked(True)
            for checkbox in self.period:
                checkbox.stateChanged.connect(self.period_checked)
        elif state == Qt.Unchecked:
            for checkbox in self.period:
                checkbox.setChecked(False)

    def period_checked(self):
        all_checked = True
        all_unchecked = True
        for checkbox in self.period:
            if checkbox.isChecked():
                all_unchecked = False
            else:
                all_checked = False
        if all_checked:
            self.period_selectAll.setCheckState(Qt.Checked)
        elif all_unchecked:
            self.period_selectAll.setCheckState(Qt.Unchecked)
        else:
            self.period_selectAll.setCheckState(Qt.PartiallyChecked)

    def selectAll_quarter(self, state):
        if state == Qt.Checked:
            for checkbox in self.quarter:
                checkbox.stateChanged.disconnect()
                checkbox.setChecked(True)
            for checkbox in self.quarter:
                checkbox.stateChanged.connect(self.quarter_checked)
        elif state == Qt.Unchecked:
            for checkbox in self.quarter:
                checkbox.setChecked(False)

    def quarter_checked(self):
        all_checked = True
        all_unchecked = True
        for checkbox in self.quarter:
            if checkbox.isChecked():
                all_unchecked = False
            else:
                all_checked = False
        if all_checked:
            self.quarter_selectAll.setCheckState(Qt.Checked)
        elif all_unchecked:
            self.quarter_selectAll.setCheckState(Qt.Unchecked)
        else:
            self.quarter_selectAll.setCheckState(Qt.PartiallyChecked)

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
        global window_x
        global window_y
        window_x = main_window.x()
        window_y = main_window.y() + 22
        main_window = AnswerWindow(fs=self.fs)
        main_window.show()


class AnswerWindow(QWidget):
    def __init__(self, parent=None, fs=None):
        super(AnswerWindow, self).__init__(parent)
        self.setGeometry(window_x, window_y, window_w, window_h)
        self.setWindowTitle(APP_TITLE + ' | 講義検索')
        self.answer = QLabel(self)
        self.maybe = QLabel(self)
        ans = ''
        maybe = ''
        global search_result
        for x in fs.get_index_list():
            if fs.d[x]['科目コード'] in search_result[0]:
                if ans == '':
                    ans = fs.d[x]['講義名']['日本語']
                else:
                    ans = ans + '\n' + fs.d[x]['講義名']['日本語']
            else:
                if maybe == '':
                    maybe = fs.d[x]['講義名']['日本語']
                else:
                    maybe = maybe + '\n' + fs.d[x]['講義名']['日本語']
        self.answer.setText(ans)
        self.answer.setAlignment(Qt.AlignCenter)
        self.answer.setFont(QtGui.QFont("Meiryo", 14))
        self.maybe.setText(maybe)
        self.maybe.setAlignment(Qt.AlignCenter)
        self.maybe.setFont(QtGui.QFont("Meiryo", 14))

        self.title = QLabel(self)
        self.title.setText('推薦講義')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QtGui.QFont("Meiryo", 14, QtGui.QFont.Bold))
        self.title.setFixedHeight(50)

        self.maybe_title = QLabel(self)
        self.maybe_title.setText('もしかして...')
        self.maybe_title.setAlignment(Qt.AlignCenter)
        self.maybe_title.setFont(QtGui.QFont("Meiryo", 14, QtGui.QFont.Bold))
        self.maybe_title.setFixedHeight(50)

        self.btnExit = QPushButton('終了', self)
        self.btnExit.setObjectName('btnKoginator')
        self.btnExit.setFont(QtGui.QFont('Meiryo', 14, QtGui.QFont.Bold))
        self.btnExit.clicked.connect(sys.exit)
        self.btnLayout = QHBoxLayout()
        self.btnLayout.addWidget(self.btnExit)

        self.vertical = QVBoxLayout()
        self.horizon1 = QHBoxLayout()
        self.horizon2 = QHBoxLayout()
        self.horizon1.addWidget(self.answer)
        self.horizon2.addWidget(self.maybe)
        self.vertical.addWidget(self.title)
        self.vertical.addLayout(self.horizon1)
        self.vertical.addWidget(self.maybe_title)
        self.vertical.addLayout(self.horizon2)
        self.vertical.addLayout(self.btnLayout)
        self.setLayout(self.vertical)

        self.btnTop = QPushButton('TOP', self)
        self.btnTop.setObjectName('btnTop')
        self.btnTop.setFont(QtGui.QFont('Meiryo', 10, QtGui.QFont.Bold))
        self.btnTop.move(5, 5)
        self.btnTop.clicked.connect(returnTop)


class KoginatorQuestionWindow(QWidget):
    def __init__(self, parent=None, newQ=''):
        super(KoginatorQuestionWindow, self).__init__(parent)

        self.setWindowTitle(APP_TITLE + ' | コギネーター')

        self.vertical = QVBoxLayout()
        self.setLayout(self.vertical)

        self.setGeometry(window_x, window_y, window_w, window_h)

        self.question = QLabel(self)
        self.setQuestion(newQ)
        self.question.setAlignment(Qt.AlignCenter)
        self.question.setFont(QtGui.QFont("Meiryo", 14, QtGui.QFont.Bold))
        self.question.setFixedHeight(20)

        self.yes = QPushButton('はい', self)
        self.mid = QPushButton('わからない', self)
        self.no = QPushButton('いいえ', self)

        self.yes.setObjectName('btnSelect')
        self.mid.setObjectName('btnSelect')
        self.no.setObjectName('btnSelect')

        self.yes.setFont(QtGui.QFont('Meiryo', 20, QtGui.QFont.Bold))
        self.mid.setFont(QtGui.QFont('Meiryo', 20, QtGui.QFont.Bold))
        self.no.setFont(QtGui.QFont('Meiryo', 20, QtGui.QFont.Bold))

        self.yes.clicked.connect(self.btnYesClicked)
        self.mid.clicked.connect(self.btnMidClicked)
        self.no.clicked.connect(self.btnNoClicked)

        self.vertical.addWidget(self.question)

        self.vertical.addWidget(self.yes)
        self.vertical.addWidget(self.mid)
        self.vertical.addWidget(self.no)

        self.btnTop = QPushButton('TOP', self)
        self.btnTop.setObjectName('btnTop')
        self.btnTop.setFont(QtGui.QFont('Meiryo', 10, QtGui.QFont.Bold))
        self.btnTop.move(5, 5)
        self.btnTop.clicked.connect(returnTop)

    def setQuestion(self, newQ):
        self.question.setText(newQ)

    def btnYesClicked(self):
        self.ans = '5'
        print('answer : ' + self.ans)
        if(kg.getAnswer(self.ans)):
            kg.printAnswer()
            show_answer()
            return
        next_koginator_window()

    def btnMidClicked(self):
        self.ans = '3'
        print('answer : ' + self.ans)
        if(kg.getAnswer(self.ans)):
            kg.printAnswer()
            show_answer()
            return
        next_koginator_window()

    def btnNoClicked(self):
        self.ans = '1'
        print('answer : ' + self.ans)
        if(kg.getAnswer(self.ans)):
            kg.printAnswer()
            show_answer()
            return
        next_koginator_window()


class KoginatorAnswerWindow(QWidget):
    def __init__(self, parent=None):
        super(KoginatorAnswerWindow, self).__init__(parent)
        self.setGeometry(window_x, window_y, window_w, window_h)
        self.setWindowTitle(APP_TITLE + ' | コギネーター')
        self.answer = QLabel(self)
        ans = ''
        for kgans in kg.answer:
            if ans == '':
                ans = ans + kgans
            else:
                ans = ans + '\n\n' + kgans
        self.answer.setText(ans)
        self.answer.setAlignment(Qt.AlignCenter)
        self.answer.setFont(QtGui.QFont("Meiryo", 14, QtGui.QFont.Bold))
        self.answer.setFixedHeight(100)

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

        self.btnTop = QPushButton('TOP', self)
        self.btnTop.setObjectName('btnTop')
        self.btnTop.setFont(QtGui.QFont('Meiryo', 10, QtGui.QFont.Bold))
        self.btnTop.move(5, 5)
        self.btnTop.clicked.connect(returnTop)

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
    global window_x
    global window_y
    window_x = main_window.x()
    window_y = main_window.y() + 22
    if w == "koginator":
        kg = koginator.koginator()
        main_window = KoginatorQuestionWindow(None, kg.getQuestion())
    elif w == "search":
        main_window = KeywordSearchWindow()
    main_window.show()


def next_koginator_window():
    global main_window
    global window_x
    global window_y
    window_x = main_window.x()
    window_y = main_window.y() + 22
    main_window = KoginatorQuestionWindow(None, kg.getQuestion())
    main_window.show()


def show_answer():
    global main_window
    global window_x
    global window_y
    window_x = main_window.x()
    window_y = main_window.y() + 22
    main_window = KoginatorAnswerWindow()
    main_window.show()


def returnTop():
    global kg, main_window, window_x, window_y
    kg = None
    window_x = main_window.x()
    window_y = main_window.y() + 22
    main_window = MainWindow()
    main_window.show()
    print('return to top')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    try:
        styleFile = os.path.join(os.path.dirname(__file__), 'style.qss')
        with open(styleFile, 'r') as f:
            style = f.read()
    except BaseException:
        style = ''

    app.setStyleSheet(style)
    search_result = None
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
