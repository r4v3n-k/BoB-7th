from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QTableWidget, QAbstractItemView, QBoxLayout, QLineEdit, QPushButton, \
    QTableWidgetItem
from libs.ParseRegistry.Amcache import FIELDS


class AmcacheViewer(QWidget):
    def __init__(self, title, contents, env):
        QWidget.__init__(self)
        import os
        if len(env) == 2:
            self.db_dir = os.getcwd() + "\\"
        else:
            self.db_dir = env[6]
        self.column_header = list(map(lambda e: e.name, FIELDS))
        self.title = title
        self.contents = contents
        self.ui()

    def ui(self):
        self.setWindowTitle(self.title)
        from modules.constant import ICON_PATH
        self.setWindowIcon(QIcon(ICON_PATH[0]))
        self.setMinimumSize(self.width(), self.height())
        layout = QBoxLayout(QBoxLayout.TopToBottom, self)
        top_layout = QBoxLayout(QBoxLayout.LeftToRight, self)

        self.search_box = QLineEdit(self)
        self.search_box.returnPressed.connect(self.search)
        self.search_box.setFixedHeight(30)
        self.search_box.setPlaceholderText("Search")

        export_btn = QPushButton("Export as CSV", self)
        export_btn.setFixedHeight(30)
        export_btn.clicked.connect(self.export)
        export_btn.setFixedWidth(150)

        self.table = QTableWidget(self)
        self.table.setColumnCount(len(self.column_header))
        self.table.setHorizontalHeaderLabels(self.column_header)
        self.table.verticalHeader().setVisible(False)

        for row in range(len(self.contents)):
            self.table.insertRow(row)
            for col in range(len(self.column_header)):
                self.table.setItem(row, col, QTableWidgetItem(self.contents[row][col]))
                self.table.item(row, col).setTextAlignment(Qt.AlignCenter)
            self.table.item(row, 1).setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        top_layout.addWidget(self.search_box)
        top_layout.addWidget(export_btn)
        layout.addLayout(top_layout)
        layout.addWidget(self.table)

        self.show()

    def search(self):
        keyword = self.search_box.text()
        if not keyword:
            for row in range(len(self.contents)):
                if self.table.isRowHidden(row):
                    self.table.showRow(row)
            return
        items = self.table.findItems(keyword, Qt.MatchContains)
        included_rows = list(set([self.table.row(item) for item in items]))
        for row in range(len(self.contents)):
            if row in included_rows:
                self.table.showRow(row)
            else:
                self.table.hideRow(row)

    def export(self):
        import csv, datetime

        output_path = self.db_dir + "amcache_{}.csv".format(datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S%f"))
        with open(output_path, 'w', encoding='utf-8', newline='') as csv_file:
            w = csv.writer(csv_file)
            w.writerow(map(lambda e: e.name, FIELDS))
            for e in self.contents:
                w.writerow(e)
        from PyQt5.QtWidgets import QMessageBox
        reply = QMessageBox.information(self, "Help", "Success !", QMessageBox.Open, QMessageBox.Close)
        if reply == QMessageBox.Open:
            import subprocess
            subprocess.call('explorer.exe {}'.format(self.db_dir), shell=True)

    def contextMenuEvent(self, event):
        from PyQt5.QtWidgets import QMenu
        menu = QMenu(self)
        copy_action = menu.addAction("Copy")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == copy_action:
            selected = self.table.selectedItems()
            if len(selected) == 1:
                copied = selected[0].text()
            else:
                copied = " ".join(currentQTableWidgetItem.text() for currentQTableWidgetItem in selected)
            import pyperclip
            pyperclip.copy(copied)
