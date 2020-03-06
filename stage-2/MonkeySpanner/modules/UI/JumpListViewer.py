from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QCursor, QIcon
from PyQt5.QtWidgets import *

class JumpListViewer(QWidget):
    def __init__(self, hash_list, env):
        QWidget.__init__(self)
        self.hash_list = hash_list
        self.db_dir = env[6]
        self.list_view_width = 180
        self.lnk_files_header_items = ["Accessed Time", "Modified Time", "Created Time", "LocalBasePath", "Size", "E.No.",
             "Drive Type", "VolumnName", "Serial No."]
        self.dest_list_header_items = ["New (Timestamp)", "Data", "E.No.", "Access Count", "NetBIOSName", "Last Recorded Access",
             "New (MAC)", "Seq No.", "Birth (Timestamp)", "Birth (MAC)"]
        self.selected = -1
        self.ui()

    def ui(self):
        self.setWindowTitle("JumpList")
        from modules.constant import ICON_PATH
        self.setWindowIcon(QIcon(ICON_PATH[0]))
        self.setMinimumSize(self.width(), self.height())

        # Layout
        window_layout = QBoxLayout(QBoxLayout.LeftToRight, self)
        left_layout = QBoxLayout(QBoxLayout.TopToBottom)
        right_layout = QBoxLayout(QBoxLayout.TopToBottom)
        window_layout.addLayout(left_layout)
        window_layout.addLayout(right_layout)
        self.setLayout(window_layout)

        # Set up Label
        hash_title_label = QLabel("AppID: ", self)
        self.hash_label = QLabel(self)
        self.hash_label.setFixedWidth(self.list_view_width)
        self.hash_label.setAlignment(Qt.AlignCenter)

        # Set up ListView
        self.hash_list_view = QListView(self)
        self.model = QStandardItemModel()
        for h in self.hash_list:
            self.model.appendRow(QStandardItem(h[0]))
        self.hash_list_view.setModel(QStandardItemModel())
        self.hash_list_view.setMaximumWidth(self.list_view_width)
        self.hash_list_view.clicked.connect(self.selected_hash)
        self.hash_list_view.setModel(self.model)

        # Set up Export Button
        export_btn = QPushButton("Export as CSV", self)
        export_btn.setFixedSize(self.list_view_width, 40)
        export_btn.clicked.connect(self.export_btn_clicked)
        export_btn.setCursor(QCursor(Qt.PointingHandCursor))

        # Set up lnk_files Table
        lnk_files_label = QLabel("Link Files:", self)
        self.lnk_files_table = QTableWidget(self)
        lnk_files_header = self.lnk_files_table.verticalHeader()
        lnk_files_header.setDefaultSectionSize(28)
        lnk_files_header.setMaximumSectionSize(28)
        self.lnk_files_table.horizontalHeader().setStretchLastSection(True)
        self.lnk_files_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lnk_files_table.verticalHeader().setVisible(False)
        self.lnk_files_table.setColumnCount(len(self.lnk_files_header_items))
        self.lnk_files_table.setHorizontalHeaderLabels(self.lnk_files_header_items)

        # Set up dest_list Table
        dest_list_label = QLabel("Dest List:", self)
        self.dest_list_table = QTableWidget(self)
        dest_list_header = self.dest_list_table.verticalHeader()
        dest_list_header.setDefaultSectionSize(28)
        dest_list_header.setMaximumSectionSize(28)
        self.dest_list_table.horizontalHeader().setStretchLastSection(True)
        self.dest_list_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dest_list_table.verticalHeader().setVisible(False)
        self.dest_list_table.setColumnCount(len(self.dest_list_header_items))
        self.dest_list_table.setHorizontalHeaderLabels(self.dest_list_header_items)

        left_layout.addWidget(hash_title_label)
        left_layout.addWidget(self.hash_label)
        left_layout.addWidget(self.hash_list_view)
        left_layout.addWidget(export_btn)
        right_layout.addWidget(lnk_files_label)
        right_layout.addWidget(self.lnk_files_table)
        right_layout.addWidget(dest_list_label)
        right_layout.addWidget(self.dest_list_table)

        self.show()

    def selected_hash(self, i):
        self.selected = self.model.itemFromIndex(i).row()
        self.hash_label.setText(self.hash_list[self.selected][1])
        self.load(self.hash_list[self.selected][2])

    def load(self, log_list):
        lnk_files = log_list["lnk_files"]
        dest_list = log_list["dest_list"]
        self.lnk_files_table.clearContents()
        self.dest_list_table.clearContents()
        self.lnk_files_table.setRowCount(0)
        self.dest_list_table.setRowCount(0)
        r = 0
        for item in lnk_files:
            self.lnk_files_table.insertRow(r)
            for c in range(self.lnk_files_table.columnCount()):
                self.lnk_files_table.setItem(r, c, QTableWidgetItem(item[c]))
            r += 1
        r = 0
        self.lnk_files_table.resizeColumnsToContents()

        for item in dest_list:
            self.dest_list_table.insertRow(r)
            for c in range(self.dest_list_table.columnCount()):
                self.dest_list_table.setItem(r, c, QTableWidgetItem(item[c]))
            r += 1
        self.dest_list_table.resizeColumnsToContents()

    def export_btn_clicked(self):
        if self.selected == -1:
            QMessageBox.question(self, "Help", "Please select in above list.", QMessageBox.Ok)
            return
        self.export()

    def export(self):
        import csv
        # Export Link File List
        msg = "Success ! - AppID: " + self.hash_label.text()
        try:
            file_name = self.hash_label.text() + "-lnk_files.csv"
            output_path = self.db_dir + file_name
            csv_file = open(output_path, 'w')
            lnk_writer = csv.DictWriter(csv_file, delimiter=',', lineterminator='\n', fieldnames=self.lnk_files_header_items)
            lnk_writer.writeheader()
            for row_data in self.hash_list[self.selected][2]["lnk_files"]:
                try:
                    _dict = { self.lnk_files_header_items[n]:row_data[n] for n in range(len(row_data)) }
                    lnk_writer.writerow(_dict)
                except Exception as e:
                    print(e)
                    pass

            # Export Dest List
            file_name = self.hash_label.text() + "-dest_list.csv"
            output_path = self.db_dir + file_name
            csv_file = open(output_path, 'w', newline='')
            destlist_writer = csv.DictWriter(csv_file, delimiter=',', lineterminator='\n', fieldnames=self.dest_list_header_items)
            destlist_writer.writeheader()
            for row_data in self.hash_list[self.selected][2]["dest_list"]:
                try:
                    _dict = {self.dest_list_header_items[n]: row_data[n] for n in range(len(row_data))}
                    destlist_writer.writerow(_dict)
                except:
                    pass
        except Exception as e:
            msg = "{}".format(e)
        reply = QMessageBox.question(self, "Help", msg, QMessageBox.Open, QMessageBox.Close)
        if reply == QMessageBox.Open:
            import subprocess
            print(self.db_dir)
            subprocess.call('explorer.exe {}'.format(self.db_dir), shell=True)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setCursor(QCursor(Qt.PointingHandCursor))
        copy_action = menu.addAction("Copy")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == copy_action:
            selected = self.lnk_files_table.selectedItems() + self.dest_list_table.selectedItems()
            if len(selected) == 1:
                copied = selected[0].text()
            else:
                copied = " ".join(currentQTableWidgetItem.text() for currentQTableWidgetItem in selected)
            import pyperclip
            pyperclip.copy(copied)