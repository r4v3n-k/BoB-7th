from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidget, QLabel, QTableWidgetItem, QFormLayout, \
    QAbstractItemView

class NTFSDetailViewer(QWidget):
    def __init__(self):
        QWidget.__init__(self)

    def ui(self, content):
        self.setWindowTitle("NTFS Detail Viewer")
        self.setMinimumWidth(750)

        layout = QFormLayout(self)

        mft_label = QLabel("- MFT Entry Detail", self)
        mft_label.setFixedWidth(320)
        usn_label = QLabel("- USN Record Detail", self)
        file_attr_label = QLabel("- File Name Attribute in MFT", self)
        file_attr_label.setFixedHeight(20)
        file_attr_label.setAlignment(Qt.AlignBottom)
        transaction_label = QLabel(self)
        transaction_label.setFixedHeight(20)
        transaction_label.setAlignment(Qt.AlignBottom)

        mft_table = QTableWidget(self)
        mft_table.setFixedSize(300, 180)
        mft_table.verticalHeader().setVisible(False)
        mft_table.verticalHeader().setDefaultSectionSize(26)
        mft_table.verticalHeader().setMaximumSectionSize(26)
        mft_table.horizontalHeader().setVisible(False)
        mft_table.setRowCount(6)
        mft_table.setColumnCount(2)
        mft_table.setItem(0, 0, QTableWidgetItem("MFT Entry Number"))
        mft_table.setItem(1, 0, QTableWidgetItem("Sequence Value"))
        mft_table.setItem(2, 0, QTableWidgetItem("Base Entry"))
        mft_table.setItem(3, 0, QTableWidgetItem("Currently In Use"))
        mft_table.setItem(4, 0, QTableWidgetItem("Most Recently USN"))
        mft_table.setItem(5, 0, QTableWidgetItem("Most Recently LSN"))
        for i in range(len(content[0])-1):
            mft_table.setItem(i, 1, QTableWidgetItem(content[0][i]))
        mft_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        mft_table.resizeColumnsToContents()
        for c in range(mft_table.columnCount()):
            mft_table.setColumnWidth(c, 130)
        mft_table.verticalHeader().setStretchLastSection(True)
        mft_table.horizontalHeader().setStretchLastSection(True)

        usn_table = QTableWidget(self)
        usn_table.setMinimumWidth(280)
        usn_table.setFixedHeight(165)
        usn_table.verticalHeader().setVisible(False)
        usn_table.verticalHeader().setDefaultSectionSize(31)
        usn_table.verticalHeader().setMaximumSectionSize(31)
        usn_table.horizontalHeader().setVisible(False)
        usn_table.setRowCount(5)
        usn_table.setColumnCount(2)
        usn_table.setItem(0, 0, QTableWidgetItem("USN"))
        usn_table.setItem(1, 0, QTableWidgetItem("File Name"))
        usn_table.setItem(2, 0, QTableWidgetItem("Timestamp"))
        usn_table.setItem(3, 0, QTableWidgetItem("Reason"))
        usn_table.setItem(4, 0, QTableWidgetItem("File Attributes   "))
        for i in range(len(content[1])):
            usn_table.setItem(i, 1, QTableWidgetItem(content[1][i]))
        usn_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        usn_table.resizeColumnsToContents()
        usn_table.verticalHeader().setStretchLastSection(True)
        usn_table.horizontalHeader().setStretchLastSection(True)

        if content[0][-1]:
            attributes = content[0][-1]
            file_attr_table = QTableWidget(self)
            file_attr_table.setFixedHeight(115)
            file_attr_table.verticalHeader().setVisible(False)
            file_attr_table.verticalHeader().setDefaultSectionSize(28)
            file_attr_table.verticalHeader().setMaximumSectionSize(28)
            file_attr_table.setRowCount(len(content[0][-1]))
            file_attr_table.setColumnCount(5)
            file_attr_table.setHorizontalHeaderLabels([
                "File Name",
                "File Created Time",
                "File Modified Time",
                "MFT Modified Time",
                "File Accessed Time"
            ])
            for row in range(len(attributes)):
                file_attr_table.setItem(row, 0, QTableWidgetItem(attributes[row][0]))
                file_attr_table.setItem(row, 1, QTableWidgetItem(attributes[row][1]))
                file_attr_table.setItem(row, 2, QTableWidgetItem(attributes[row][2]))
                file_attr_table.setItem(row, 3, QTableWidgetItem(attributes[row][3]))
                file_attr_table.setItem(row, 4, QTableWidgetItem(attributes[row][4]))
                for c in range(5):
                    file_attr_table.item(row, c).setTextAlignment(Qt.AlignCenter)
            file_attr_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            file_attr_table.resizeColumnsToContents()
            file_attr_table.verticalHeader().setStretchLastSection(True)
            file_attr_table.horizontalHeader().setStretchLastSection(True)
        else:
            file_attr_table = QLabel("None")
            file_attr_table.setFixedHeight(40)
            file_attr_table.setFixedWidth(self.width())
            file_attr_table.setAlignment(Qt.AlignCenter)

        if len(content) == 3:
            transaction_label.setText("- LogFile Transaction Number: {}".format(content[-1][0]))
            transaction_table = QTableWidget(self)
            transaction_table.verticalHeader().setVisible(False)
            transaction_table.verticalHeader().setDefaultSectionSize(25)
            transaction_table.verticalHeader().setMaximumSectionSize(25)
            transaction_table.setRowCount(len(content[2][1]))
            transaction_table.setColumnCount(3)
            transaction_table.setHorizontalHeaderLabels(["LSN", "Redo Operation", "Undo Operation"])
            transaction_table.setColumnWidth(0, 120)
            transaction_table.setColumnWidth(1, 300)
            transaction_table.setColumnWidth(2, 300)
            row = 0
            for lsn, redo_op, undo_op in content[2][1]:
                transaction_table.setItem(row, 0, QTableWidgetItem(str(lsn)))
                transaction_table.setItem(row, 1, QTableWidgetItem(redo_op))
                transaction_table.setItem(row, 2, QTableWidgetItem(undo_op))
                transaction_table.item(row, 0).setTextAlignment(Qt.AlignCenter)
                row += 1
            transaction_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            transaction_table.horizontalHeader().setStretchLastSection(True)
        else:
            transaction_label.setText("- LogFile Transaction Number:")
            transaction_table = QLabel("None")
            transaction_table.setFixedHeight(60)
            transaction_table.setFixedWidth(self.width())
            transaction_table.setAlignment(Qt.AlignCenter)

        layout.addRow(mft_label, usn_label)
        layout.addRow(mft_table, usn_table)
        layout.addRow(file_attr_label)
        layout.addRow(file_attr_table)
        layout.addRow(transaction_label)
        layout.addRow(transaction_table)

        self.show()
