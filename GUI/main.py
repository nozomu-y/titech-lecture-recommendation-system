import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip

APP_TITLE = "東工大講義推薦システム"


class MainWindow(QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.horizontal = QHBoxLayout()
        self.vertical = QVBoxLayout()

        # ボタンの追加
        self.btn_koginator = QPushButton('コギネーター', self)
        self.btn_koginator.clicked.connect(self.exec_koginator)
        self.horizontal.addWidget(self.btn_koginator)

        self.btn_search = QPushButton('講義検索', self)
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


class SearchWindow(QWidget):

    def __init__(self, parent=None):
        super(SearchWindow, self).__init__(parent)

        self.horizontal = QHBoxLayout()
        self.vertical = QVBoxLayout()

        self.setGeometry(300, 50, 400, 350)
        self.setWindowTitle(APP_TITLE + "｜講義検索")


def change_window(w):
    global main_window
    if w == "koginator":
        main_window = KoginatorWindow()
    elif w == "search":
        main_window = SearchWindow()
    main_window.show()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()


sys.exit(app.exec_())
