from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *

class PrefetchDetailViewer(QWidget):
    def __init__(self):
        QWidget.__init__(self)

    def ui(self, title, content):
        '''
        content = [
            [0] => FileName
            [1] => [Exec name, Run Cnt]
            [2] => [MFT seq #, MFT entry #]
            [3] => [ executed time list ]
            [4] => [vol name, create date, serial num]
            [5] => [ directory strings list ]
            [6] => [ Resources loaded ]
        ]
        '''
        self.content = content
        self.setWindowTitle(title)
        self.setMinimumHeight(self.height() + 200)

        layout = QFormLayout(self)

        # File Name
        file_name_label = QLabel(content[0], self)
        file_name_label.setFixedHeight(40)
        file_name_label.setAlignment(Qt.AlignCenter)

        # Prefetch Information
        self.pf_info_table = QTableWidget(self)
        self.pf_info_table.setMinimumSize(350, 65)
        self.pf_info_table.setMaximumSize(self.width(), 65)
        self.pf_info_table.setRowCount(2)
        self.pf_info_table.setColumnCount(2)
        self.pf_info_table.setItem(0, 0, QTableWidgetItem("Executable Name  "))
        self.pf_info_table.setItem(1, 0, QTableWidgetItem("Run Count"))
        self.pf_info_table.setItem(0, 1, QTableWidgetItem(content[1][0]))
        self.pf_info_table.setItem(1, 1, QTableWidgetItem(content[1][1]))
        self.pf_info_table.verticalHeader().setVisible(False)
        self.pf_info_table.horizontalHeader().setVisible(False)
        self.pf_info_table.resizeColumnsToContents()
        self.pf_info_table.verticalHeader().setStretchLastSection(True)
        self.pf_info_table.horizontalHeader().setStretchLastSection(True)

        # MFT Information
        self.mft_info_table = QTableWidget(self)
        self.mft_info_table.setMinimumSize(350, 65)
        self.mft_info_table.setMaximumSize(self.width(), 65)
        self.mft_info_table.setRowCount(2)
        self.mft_info_table.setColumnCount(2)
        self.mft_info_table.setItem(0, 0, QTableWidgetItem("MFT Sequence Number  "))
        self.mft_info_table.setItem(1, 0, QTableWidgetItem("MFT Entry Number"))
        self.mft_info_table.setItem(0, 1, QTableWidgetItem(content[2][0]))
        self.mft_info_table.setItem(1, 1, QTableWidgetItem(content[2][1]))
        self.mft_info_table.verticalHeader().setVisible(False)
        self.mft_info_table.horizontalHeader().setVisible(False)
        self.mft_info_table.resizeColumnsToContents()
        self.mft_info_table.verticalHeader().setStretchLastSection(True)
        self.mft_info_table.horizontalHeader().setStretchLastSection(True)

        # Execution Time
        time_label = QLabel("Executed Time", self)
        time_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)

        self.time_list = QListView(self)
        self.time_list.setFixedHeight(120)
        self.time_list_model = QStandardItemModel()
        for i in range(len(content[3])):
            item = QStandardItem(content[3][i])
            item.setTextAlignment(Qt.AlignCenter)
            self.time_list_model.appendRow(item)
        self.time_list.setModel(self.time_list_model)

        # Volumn Information
        vol_label = QLabel("Volumn Information", self)
        vol_label.setFixedHeight(30)
        vol_label.setAlignment(Qt.AlignBottom)

        self.vol_table = QTableWidget(self)
        self.vol_table.setFixedHeight(93)
        self.vol_table.setRowCount(3)
        self.vol_table.setColumnCount(2)
        self.vol_table.setItem(0, 0, QTableWidgetItem("Volumn Name  "))
        self.vol_table.setItem(0, 1, QTableWidgetItem(content[4][0]))
        self.vol_table.setItem(1, 0, QTableWidgetItem("Creation Date  "))
        self.vol_table.setItem(1, 1, QTableWidgetItem(content[4][1]))
        self.vol_table.setItem(2, 0, QTableWidgetItem("Serial Number  "))
        self.vol_table.setItem(2, 1, QTableWidgetItem(content[4][2]))
        self.vol_table.verticalHeader().setVisible(False)
        self.vol_table.horizontalHeader().setVisible(False)
        self.vol_table.setColumnWidth(0, 150)
        self.vol_table.verticalHeader().setStretchLastSection(True)
        self.vol_table.horizontalHeader().setStretchLastSection(True)

        # Directory Strings
        self.dir_strings_label = QLabel("Directory Strings", self)
        self.dir_strings_label.setFixedHeight(30)
        self.dir_strings_label.setAlignment(Qt.AlignBottom)

        self.dir_strings_list = QListView()
        self.dir_strings_list.setMinimumWidth(self.width())
        self.dirStrListModel = QStandardItemModel()
        for i in range(len(content[5])):
            self.dirStrListModel.appendRow(QStandardItem(content[5][i]))
        self.dir_strings_list.setModel(self.dirStrListModel)

        rsc_loaded_label = QLabel("Resources Loaded", self)
        rsc_loaded_label.setFixedHeight(30)
        rsc_loaded_label.setAlignment(Qt.AlignBottom)

        self.rsc_loaded_list = QListView()
        self.rscLoadedListModel = QStandardItemModel()
        self.rsc_loaded_list.setMinimumWidth(self.width())
        for i in range(len(content[6])):
            self.rscLoadedListModel.appendRow(QStandardItem(content[6][i]))
        self.rsc_loaded_list.setModel(self.rscLoadedListModel)

        # Resource DLL loading
        childLayout1 = QBoxLayout(QBoxLayout.TopToBottom)
        childLayout2 = QBoxLayout(QBoxLayout.TopToBottom)
        childLayout1.addWidget(self.pf_info_table)
        childLayout1.addWidget(self.mft_info_table)
        childLayout2.addWidget(time_label)
        childLayout2.addWidget(self.time_list)
        childLayout = QBoxLayout(QBoxLayout.LeftToRight)
        childLayout.addLayout(childLayout1)
        childLayout.addLayout(childLayout2)

        layout.addRow(file_name_label)
        layout.addRow(childLayout)
        layout.addRow(vol_label)
        layout.addRow(self.vol_table)
        layout.addRow(self.dir_strings_label)
        layout.addRow(self.dir_strings_list)
        layout.addRow(rsc_loaded_label)
        layout.addRow(self.rsc_loaded_list)
        self.show()

    # def contextMenuEvent(self, event):
    #     menu = QMenu(self)
    #     copyAction = menu.addAction("Copy")
    #     action = menu.exec_(self.mapToGlobal(event.pos()))
    #     if action == copyAction:
    #         import pyperclip
    #         pyperclip.copy(self.content)
