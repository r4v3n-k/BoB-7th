from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget, QSplitter, QBoxLayout, QCheckBox, QPushButton, \
    QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
import modules.constant as CONSTANT

class FilteringWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.options = {
            "Artifact": CONSTANT.ARTIFACT_LIST,
            "Color": CONSTANT.COLOR_LIST.keys()
        }
        self.parents = []
        self.items = {}

        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)

        self.tree = QTreeWidget(left_widget)
        self.tree.setHeaderHidden(True)
        self.tree.setAnimated(True)
        left_layout.addWidget(self.tree)

        self.simple_filter_btn = QPushButton("Filter by above", left_widget)
        self.simple_filter_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.simple_filter_btn.setFixedHeight(30)
        left_layout.addWidget(self.simple_filter_btn)

        for option in self.options.keys():
            parent = QTreeWidgetItem(self.tree)
            parent.setText(0, option)
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            parent.setExpanded(True)
            self.parents.append(parent)
            self.items[option] = []
            for value in self.options[option]:
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, value)
                child.setCheckState(0, Qt.Checked)
                self.items[option].append(child)

        self.sw_filter_widget = QWidget()
        sw_filter_widget_layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.sw_filter_widget.setLayout(sw_filter_widget_layout)

        self.alert_text = QLabel('* Only filter the results \nin the "ALL" tab', self)
        self.alert_text.setFixedHeight(35)
        font = QFont("Times New Roman", 10)
        font.setBold(True)
        self.alert_text.setFont(font)
        sw_filter_widget_layout.addWidget(self.alert_text)

        self.chk_list = []
        for key in CONSTANT.SOFTWARE.keys():
            chkBox = QCheckBox(key)
            self.chk_list.append(chkBox)
            sw_filter_widget_layout.addWidget(chkBox)

        self.sw_filter_btn = QPushButton("Filter by software", self)
        self.sw_filter_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.sw_filter_btn.setFixedHeight(30)
        sw_filter_widget_layout.addWidget(self.sw_filter_btn)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(self.sw_filter_widget)

        self.setFixedSize(450, 250)
        layout = QVBoxLayout(self)
        layout.addWidget(splitter)

        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.setWhatsThis("Go to \"Help --> About\"")
        self.setWindowTitle("Filter (Main)")

    def get_checked_items(self):
        checked_items = {
            self.parents[0].text(0): [],
            self.parents[1].text(0): [],
        }
        parent = self.parents[0].text(0)
        for child in self.items[parent]:
            if child.checkState(0) == Qt.Checked:
                checked_items[parent].append(child.text(0))

        parent = self.parents[1].text(0)
        for child in self.items[parent]:
            if child.checkState(0) == Qt.Checked:
                checked_items[parent].append(CONSTANT.COLOR_LIST[child.text(0)])
        return checked_items

    def set_checked_status(self, checked_status):
        for parent, childs in checked_status.items():
            for i in range(len(childs)):
                self.items[parent][i].setCheckState(0, childs[i])

    def get_checked_status(self):
        checked_status = {}
        for parent, childs in self.items.items():
            checked_status[parent] = []
            for child in childs:
                checked_status[parent].append(child.checkState(0))
        return checked_status

    def change_status_for_no_color_parent_table(self):
        self.setEnabled(True)

        self.parents[1].setDisabled(True)
        for item in self.items["Color"]:
            item.setDisabled(True)
        self.simple_filter_btn.setText("Filter by above")
        self.simple_filter_btn.setEnabled(True)

        self.sw_filter_widget.setEnabled(True)

    def change_status_for_color_parent_table(self):
        self.setEnabled(True)

        self.parents[1].setDisabled(False)
        for item in self.items["Color"]:
            item.setDisabled(False)
        self.simple_filter_btn.setText("Filter by above")
        self.simple_filter_btn.setEnabled(True)

        self.sw_filter_widget.setEnabled(False)

    def change_status_for_no_color_table(self):
        self.setEnabled(True)

        self.parents[1].setDisabled(True)
        for item in self.items["Color"]:
            item.setDisabled(True)
        self.simple_filter_btn.setText("Auto")
        self.simple_filter_btn.setEnabled(False)

        self.sw_filter_widget.setEnabled(False)

    def change_status_for_color_table(self):
        self.setEnabled(True)

        self.parents[1].setDisabled(False)
        for item in self.items["Color"]:
            item.setDisabled(False)
        self.simple_filter_btn.setText("Auto")
        self.simple_filter_btn.setEnabled(False)

        self.sw_filter_widget.setEnabled(False)