from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout

class JumpListDetailViewer(QWidget):
    LNK_FILE = 0
    DEST_LIST = 1

    def __init__(self):
        QWidget.__init__(self)
        self.basic_category = ["JumpList Name", "Software Name", "Type",]
        self.data_category = [
            [
                "Local Base Path",
                "Modified Time",
                "Accessed Time",
                "Created Time",
                "File Size",
                "Drive Type",
                "Volumn Name",
                "Serial Number",
            ],
            [
                "Entry ID (E.NO)",
                "File Path",
                "Last Recorded Time",
                "Access Count",
                "New (Timestamp)",
                "New (MAC)",
                "Birth (Timestamp)",
                "Birth (MAC)",
                "NetBIOSName",
                "Sequence No",
            ]
        ]

    def ui(self, type, contents):
        '''
        LNK: [
            [0] JumpList File Name
            [1] Software,
            [2] Type,
            [3] lnk_header
                    [0] Modified Time
                    [1] Accessed Time
                    [2] Created Time
                    [3] File Size
                lnk_after_header
                    [4] Drive Type
                    [5] Volumn Name
                    [6] Drive Serial Number
                    [7] LocalBasePath
        ]

        Dest: [
            [0] JumpList File Name
            [1] Software,
            [2] Type,
            [3] Data
                    [0] Accessed Time,
                    [1] Full Path
                    [2] Entry ID Number (E.NO)
                    [3] Access Count
                    [4] NetBIOSName
                    [5] New (timestamp)
                    [6] New (MAC)
                    [7] Sequence Number
                    [8] Birth (timestamp)
                    [9] Birth (MAC)
        ]
        '''

        if type == JumpListDetailViewer.LNK_FILE:
            self.setWindowTitle("JumpList Link-File")
        elif type == JumpListDetailViewer.DEST_LIST:
            self.setWindowTitle("JumpList Dest-List")

        layout = QVBoxLayout(self)
        basic_label = QLabel("Basic Information", self)

        self.basic_table = QTableWidget(self)
        self.basic_table.setFixedHeight(90)
        self.basic_table.setRowCount(len(self.basic_category))
        self.basic_table.setColumnCount(2)
        self.basic_table.verticalHeader().setVisible(False)
        self.basic_table.horizontalHeader().setVisible(False)
        for i in range(len(self.basic_category)):
            self.basic_table.setItem(i, 0, QTableWidgetItem(self.basic_category[i]))
        for i in range(len(self.basic_category)):
            self.basic_table.setItem(i, 1, QTableWidgetItem(contents[i]))
        self.basic_table.verticalHeader().setDefaultSectionSize(28)
        self.basic_table.verticalHeader().setMaximumSectionSize(28)
        self.basic_table.horizontalHeader().setStretchLastSection(True)
        self.basic_table.verticalHeader().setStretchLastSection(True)
        self.basic_table.setColumnWidth(0, 120)

        data_label = QLabel("JumpList Information", self)
        data_label.setFixedHeight(30)
        data_label.setAlignment(Qt.AlignBottom)

        self.data_table = QTableWidget(self)
        self.data_table.setRowCount(len(self.data_category[type]))
        self.data_table.setColumnCount(2)
        self.data_table.verticalHeader().setVisible(False)
        self.data_table.horizontalHeader().setVisible(False)
        for i in range(len(self.data_category[type])):
            self.data_table.setItem(i, 0, QTableWidgetItem(self.data_category[type][i]))
        if type == JumpListDetailViewer.LNK_FILE:
            self.data_table.setMinimumSize(self.width(), 230)
            self.data_table.setItem(0, 1, QTableWidgetItem(contents[3][-1]))
            for i in range(len(contents[3])-1):
                self.data_table.setItem(i + 1, 1, QTableWidgetItem(contents[3][i]))
        elif type == JumpListDetailViewer.DEST_LIST:
            self.data_table.setMinimumSize(self.width(), 290)
            self.data_table.setItem(0, 1, QTableWidgetItem(contents[3][2]))
            self.data_table.setItem(1, 1, QTableWidgetItem(contents[3][1]))
            self.data_table.setItem(2, 1, QTableWidgetItem(contents[3][0]))
            self.data_table.setItem(3, 1, QTableWidgetItem(contents[3][3]))
            self.data_table.setItem(4, 1, QTableWidgetItem(contents[3][5]))
            self.data_table.setItem(5, 1, QTableWidgetItem(contents[3][6]))
            self.data_table.setItem(6, 1, QTableWidgetItem(contents[3][8]))
            self.data_table.setItem(7, 1, QTableWidgetItem(contents[3][9]))
            self.data_table.setItem(8, 1, QTableWidgetItem(contents[3][4]))
            self.data_table.setItem(9, 1, QTableWidgetItem(contents[3][7]))

        self.data_table.verticalHeader().setDefaultSectionSize(28)
        self.data_table.verticalHeader().setMaximumSectionSize(28)
        self.data_table.horizontalHeader().setStretchLastSection(True)
        self.data_table.verticalHeader().setStretchLastSection(True)
        self.data_table.setColumnWidth(0, 120)

        layout.addWidget(basic_label)
        layout.addWidget(self.basic_table)
        layout.addWidget(data_label)
        layout.addWidget(self.data_table)

        self.show()

    def contextMenuEvent(self, event):
        from PyQt5.QtWidgets import QMenu
        menu = QMenu(self)
        copy_action = menu.addAction("Copy")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == copy_action:
            selected = self.basic_table.selectedItems() + self.data_table.selectedItems()
            if len(selected) == 1:
                copied = selected[0].text()
            else:
                copied = " ".join(currentQTableWidgetItem.text() for currentQTableWidgetItem in selected)
            import pyperclip
            pyperclip.copy(copied)
