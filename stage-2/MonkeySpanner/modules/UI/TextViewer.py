from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import *

class TextViewer(QWidget):

    def __init__(self):
        super(TextViewer, self).__init__()

    def ui(self, title, content):
        self.setWindowTitle(title)
        self.resize(600, 500)
        
        text_edit = QTextEdit('', self)
        text_edit.setReadOnly(True)
        text_edit.setContentsMargins(10, 5, 5, 10)

        for item in content.split('\n'):
            text_edit.append(item)

        vertical_layout = QVBoxLayout(self)
        vertical_layout.addWidget(text_edit)
        self.show()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        copy_action = menu.addAction("Copy")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == copy_action:
            import pyperclip
            pyperclip.copy(self.content)
