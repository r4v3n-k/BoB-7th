from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import *

class ListViewer(QWidget):

    def __init__(self, title, content):
        QWidget.__init__(self)
        self.ui(title, content)

    def ui(self, title, content):
        self.setWindowTitle(title)
        from modules.constant import ICON_PATH
        self.setWindowIcon(QIcon(ICON_PATH[0]))
        self.resize(self.width(), self.height())
        layout = QVBoxLayout(self)
        self.list_view = QListView(self)
        self.list_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.model = QStandardItemModel()
        for item in content:
            self.model.appendRow(QStandardItem(item))
        self.list_view.setModel(self.model)
        layout.addWidget(self.list_view)
        self.show()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        copyAction = menu.addAction("Copy")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == copyAction:
            copiedStr = ' '.join([self.model.itemFromIndex(idx).text() for idx in self.list_view.selectedIndexes()])
            import pyperclip
            pyperclip.copy(copiedStr)
