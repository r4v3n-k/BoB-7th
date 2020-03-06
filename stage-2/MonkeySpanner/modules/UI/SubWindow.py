from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QFont, QCloseEvent
from PyQt5.QtWidgets import QWidget, QBoxLayout, QLineEdit, QTreeWidget, QTreeWidgetItem

from modules.UI.ArtifactTable import ArtifactTable, QPushButton, QIcon, QCursor, Qt
import modules.constant as CONSTANT

class SubWindow(QWidget, QObject):
    close_signal = pyqtSignal(QCloseEvent)

    def __init__(self, title, contents, is_contents_from_table=False, does_detail_exists=True):
        QWidget.__init__(self)
        QObject.__init__(self)
        top_widget_height = 35
        pointer_cursor = QCursor(Qt.PointingHandCursor)
        
        self.setWindowTitle(title)
        self.setMinimumSize(self.width(), self.height())
        self.setWindowIcon(QIcon(CONSTANT.ICON_PATH[0]))
        
        layout = QBoxLayout(QBoxLayout.TopToBottom, self)
        top_layout = QBoxLayout(QBoxLayout.LeftToRight, self)
        layout.addLayout(top_layout)
        
        if is_contents_from_table:
            contents.setParent(self)
            self.table = contents
        else:
            self.table = ArtifactTable(self, contents)
            if not does_detail_exists:
                self.table.is_detail_allowed = does_detail_exists
            self.table.artifacts_list = contents
            self.table.ui()
            layout.addWidget(self.table)
            
        self.filtering_widget = filtering_widget("Filter ({})".format(title))
        self.filtering_widget.setCheckedStatus(self.table.checked_status)
        self.filtering_widget.itemChanged.connect(self.table.filter)
        
        filter_btn = QPushButton(self)
        filter_btn.setIcon(QIcon(CONSTANT.ICON_PATH[1]))
        filter_btn.setFixedSize(top_widget_height, top_widget_height)
        filter_btn.setStyleSheet("background-color: darkslategray")
        filter_btn.setShortcut("Ctrl+D")
        filter_btn.clicked.connect(self.filtering_widget.show)
        filter_btn.setCursor(pointer_cursor)

        self.search_box = QLineEdit(self)
        self.search_box.setFixedHeight(top_widget_height)
        self.search_box.showMaximized()
        self.search_box.setFont(QFont("Arial", 12))
        self.search_box.setPlaceholderText("Search")
        self.search_box.returnPressed.connect(self.search)

        top_layout.addWidget(filter_btn)
        top_layout.addWidget(self.search_box)
        layout.addWidget(self.table)
        if self.table.isHidden():
            self.table.show()

    def search(self):
        keyword = self.search_box.text()
        if not keyword:
            self.table.search(keyword, self.filtering_widget.get_checked_items())
        else:
            self.table.search(keyword)

    def closeEvent(self, e):
        self.close_signal.emit(e)

class filtering_widget(QTreeWidget):
    def __init__(self, title):
        QTreeWidget.__init__(self)
        self.options = {
            "Artifact": CONSTANT.ARTIFACT_LIST,
            "Color": CONSTANT.COLOR_LIST.keys()
        }
        self.setWindowTitle(title)
        self.ui()

    def ui(self):
        self.parents = []
        self.items = {}
        for option in self.options.keys():
            parent = QTreeWidgetItem(self)
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

        self.setFixedWidth(200)
        self.setMinimumHeight(320)
        self.setHeaderHidden(True)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)

        self.setWhatsThis("Go to \"Help --> About\"")
        self.setAnimated(True)

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