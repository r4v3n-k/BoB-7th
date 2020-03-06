from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QLabel, QScrollArea, QVBoxLayout, \
    QApplication


class WebArtifactDetailViewer(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.category = [
            "ID", "Container Name", "Created Time", "Accessed Time", "Modified Time", "Expires Time",
            "Synced Time", "Sync Count", "Access Count", "URL", "File Name", "File Size", "Directory"
        ]

    def ui(self, title, content):
        # response header
        self.setWindowTitle(title)
        layout = QVBoxLayout(self)

        self.table = QTableWidget(self)
        self.table.setMinimumSize(self.width(), 370)
        self.table.setRowCount(len(self.category))
        self.table.setColumnCount(2)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        for i in range(len(self.category)):
            self.table.setItem(i, 0, QTableWidgetItem(self.category[i]))
        for i in range(len(content)-1):
            self.table.setItem(i, 1, QTableWidgetItem(content[i]))
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setDefaultSectionSize(28)
        self.table.verticalHeader().setMaximumSectionSize(28)
        self.table.setColumnWidth(0, 120)

        header_label = QLabel("Response Header", self)
        header_label.setFixedHeight(30)
        header_label.setAlignment(Qt.AlignBottom)

        label = QLabel()
        content = content[-1] if content[-1] else "None"
        label.setText(content)
        label.setMargin(10)
        scroll = QScrollArea(self)
        scroll.setWidget(label)

        layout.addWidget(self.table)
        layout.addWidget(header_label)
        layout.addWidget(scroll)
        self.show()

    # def contextMenuEvent(self, event):
    #     from PyQt5.QtWidgets import QMenu
    #     menu = QMenu(self)
    #     copy_action = menu.addAction("Copy")
    #     action = menu.exec_(self.mapToGlobal(event.pos()))
    #     if action == copy_action:
    #         import pyperclip
    #         pyperclip.copy(self.content)
