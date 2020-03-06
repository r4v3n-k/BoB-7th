from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import modules.constant as CONSTANT

class AboutWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.index = {
            '1. Introduction': ['1-1. Background', '1-2. Motivation', '1-3. About "MonkeySapnner"'],
            '2. What is Artifact Prototype?': ['2-1. Definition of Artifact Prototype', '2-2. Methodology'],
            '3. Prototype': [
                "3-1. {}".format(CONSTANT.ADOBE_READER_KEYWORD),
                "3-2. {}".format(CONSTANT.ADOBE_FLASH_PLAYER_KEYWORD),
                "3-3. {}".format(CONSTANT.EDGE_KEYWORD),
                "3-4. {}".format(CONSTANT.HWP_KEYWORD),
                "3-5. {}".format(CONSTANT.IE_KEYWORD),
                "3-6. {}".format(CONSTANT.OFFICE_KEYWORD),
                "3-7. {}".format(CONSTANT.LPE_KEYWORD),
            ],
            '4. License': ['4-1. Apache License, Version 2.0', '4-2. MIT License']
        }
        self.ui()

    def ui(self):
        self.setWindowTitle("About")
        self.setFixedSize(self.width(), self.height()-150)
        layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        # Table of Contents
        self.indexTree = QTreeWidget(self)
        self.indexTree.setFixedWidth(265)
        self.indexTree.setHeaderLabel("Table Of Contents")
        self.indexTree.itemSelectionChanged.connect(self.itemSelectionChanged)

        tree_items = []
        for p_text in self.index.keys():
            parent = QTreeWidgetItem(self.indexTree)
            parent.setText(0, p_text)
            parent.setExpanded(True)
            tree_items.append(parent)
            for c_text in self.index[p_text]:
                child = QTreeWidgetItem(parent)
                child.setText(0, c_text)
                tree_items.append(child)

        # Contents
        self.contents = QTextEdit('', self)
        self.contents.setText(CONSTANT.aboutContents['1'])
        self.contents.setContentsMargins(10, 5, 5, 10)
        self.contents.setReadOnly(True)

        splitter.addWidget(self.indexTree)
        splitter.addWidget(self.contents)
        self.show()

    def itemSelectionChanged(self):
        for item in self.indexTree.selectedItems():
            idx = item.text(0).split('.')[0]
            self.contents.setText(CONSTANT.aboutContents[idx])
