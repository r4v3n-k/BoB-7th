from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QBoxLayout, QSpacerItem, QGroupBox, QGridLayout, QScrollArea, QVBoxLayout


class HomeWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent=parent)
        self.btn_img_path = ["\\img\\btn1.PNG", "\\img\\btn2.PNG"]
        self.btn_title = ["Analyzing Button: ", "Filtering Button: "]
        self.btn_desc = ["Analyze on the active system.", "Provides filtering for each analysis result."]
        self.menu_img_path = ["\\img\\menu1.PNG", "\\img\\FilteringWidget.PNG", "\\img\\menu2.PNG", "\\img\\menu3.PNG"]
        self.menu_title = [
            ["Import Directory", "Import CSV", "Export as CSV", "Import XML", "Export ALL as XML", "Export as XML", "Exit"],
            ["FilteringWidget"],
            ["\"Home\" Tab", "show NTFS Log", "show JumpList", "show RecentFileCache.bcf", "show Amcache.hve"],
            ["Environment", "About"],
        ]
        self.menu_desc = [
            ["Import and analyze the directory that holds the \nartifact copies.",
             "Loads the analysis results saved as a CSV file. \nDetails are excluded.",
             "Save the analysis results as a CSV file.\nDetails are excluded.",
             "Loads the analysis results saved as a XML file. \nDetails are included.",
             "Save the analysis results as a XML file.\nDetails are included.",
             "Only the current result is saved. \nTherefore, only the results that are visible \nwhen searching or filtering are saved.",
             "Exit the program"],
            ["Filtering Button opens when \n"
             "clicked. You can filter by \n"
             "artifact or color or by software.\n"
             "However, software-specific \n"
             "filtering is only available \n"
             "on the All Analysis tab."],
            ["Open the Home tab, which describes the \nbasic functionality.",
             "Open the NTFS Log Viewer. When you click,\nyou must upload the log file.",
             "Open the Jump List Viewer. \nHowever, the directory must be imported or \nanalysis of the active system must be \ncompleted.",
             "Analyze compatibility artifact files in \nWindows 7. (Only Importing file is available)",
             "Analyze compatibility artifact files in \nWindows 10. (Only Importing file is available)"],
            ["Displays current environmental information.\nContains registry related to artifact collection.",
             "Opens help with a description of the tool."],
        ]
        self.max_width_of_group_box = 600
        self.ui()

    def ui(self):
        central_widget = QWidget()
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        central_widget.setLayout(layout)

        first_row_layout = QBoxLayout(QBoxLayout.LeftToRight)
        second_row_layout = QBoxLayout(QBoxLayout.LeftToRight)
        third_row_layout = QBoxLayout(QBoxLayout.LeftToRight)
        btn_desc_group = QGroupBox(self)
        btn_desc_group.setLayout(first_row_layout)
        btn_desc_group.setFixedHeight(80)
        menu_desc_group1 = QGroupBox(self)
        menu_desc_group1.setFixedHeight(400)
        # menu_desc_group1.setMaximumWidth(self.max_width_of_group_box)
        menu_desc_group_layout1 = QGridLayout()
        menu_desc_group1.setLayout(menu_desc_group_layout1)
        menu_desc_group2 = QGroupBox(self)
        # menu_desc_group2.setMaximumWidth(self.max_width_of_group_box)
        menu_desc_group_layout2 = QGridLayout()
        menu_desc_group2.setLayout(menu_desc_group_layout2)
        menu_desc_group3 = QGroupBox(self)
        menu_desc_group3.setFixedHeight(300)
        # menu_desc_group3.setMaximumWidth(self.max_width_of_group_box)
        menu_desc_group_layout3 = QGridLayout()
        menu_desc_group3.setLayout(menu_desc_group_layout3)
        menu_desc_group4 = QGroupBox(self)
        # menu_desc_group4.setMaximumWidth(self.max_width_of_group_box)
        menu_desc_group_layout4 = QGridLayout()
        menu_desc_group4.setLayout(menu_desc_group_layout4)
        second_row_layout.addWidget(menu_desc_group1)
        second_row_layout.addWidget(menu_desc_group2)
        third_row_layout.addWidget(menu_desc_group3)
        third_row_layout.addWidget(menu_desc_group4)
        layout.addWidget(btn_desc_group)
        layout.addLayout(second_row_layout)
        layout.addLayout(third_row_layout)

        import os
        cwd = os.getcwd()
        title_font = QFont("Times New Roman", 10)
        title_font.setBold(True)

        btn_img_label1 = QLabel(self)
        btn_img_label1.setPixmap(QPixmap(cwd + self.btn_img_path[0]))
        btn_title_label1 = QLabel(self.btn_title[0], self)
        btn_title_label1.setFont(title_font)
        btn_desc_label1 = QLabel(self.btn_desc[0], self)
        btn_img_label2 = QLabel(self)
        btn_img_label2.setPixmap(QPixmap(cwd + self.btn_img_path[1]))
        btn_title_label2 = QLabel(self.btn_title[1], self)
        btn_title_label2.setFont(title_font)
        btn_desc_label2 = QLabel(self.btn_desc[1], self)
        first_row_layout.addWidget(btn_img_label1, alignment=Qt.AlignCenter)
        first_row_layout.addWidget(btn_title_label1)
        first_row_layout.addWidget(btn_desc_label1)
        first_row_layout.addItem(QSpacerItem(10, 5))
        first_row_layout.addWidget(btn_img_label2, alignment=Qt.AlignCenter)
        first_row_layout.addWidget(btn_title_label2)
        first_row_layout.addWidget(btn_desc_label2)

        menu_img_label1 = QLabel(self)
        menu_img_label1.setPixmap(QPixmap(cwd + self.menu_img_path[0]))
        total = len(self.menu_title[0])
        menu_desc_group_layout1.addWidget(menu_img_label1, 0, 0, total, 1, Qt.AlignCenter)
        for i in range(total):
            title_label = QLabel("  {}".format(self.menu_title[0][i]), self)
            title_label.setFixedWidth(120)
            title_label.setFont(title_font)
            desc_label = QLabel(self.menu_desc[0][i], self)
            menu_desc_group_layout1.addWidget(title_label, i, 1)
            menu_desc_group_layout1.addWidget(desc_label, i, 2)

        menu_img_label2 = QLabel(self)
        menu_img_label2.setPixmap(QPixmap(cwd + self.menu_img_path[1]))
        menu_desc_group_layout2.addWidget(menu_img_label2, 0, 0, 2, 1, Qt.AlignCenter)
        title_label = QLabel("  {}".format(self.menu_title[1][0]), self)
        title_label.setFixedWidth(150)
        title_label.setFont(title_font)
        desc_label = QLabel(self.menu_desc[1][0], self)
        menu_desc_group_layout2.addWidget(title_label, 0, 1, Qt.AlignCenter)
        menu_desc_group_layout2.addWidget(desc_label, 1, 1, Qt.AlignTop|Qt.AlignHCenter)

        menu_img_label3 = QLabel(self)
        menu_img_label3.setPixmap(QPixmap(cwd + self.menu_img_path[2]))
        total = len(self.menu_title[2])
        menu_desc_group_layout3.addWidget(menu_img_label3, 0, 0, total, 1, Qt.AlignCenter)
        for i in range(total):
            title_label = QLabel("  {}".format(self.menu_title[2][i]), self)
            title_label.setFixedWidth(150)
            title_label.setFont(title_font)
            desc_label = QLabel(self.menu_desc[2][i], self)
            menu_desc_group_layout3.addWidget(title_label, i, 1)
            menu_desc_group_layout3.addWidget(desc_label, i, 2)

        menu_img_label4 = QLabel(self)
        menu_img_label4.setPixmap(QPixmap(cwd + self.menu_img_path[3]))
        total = len(self.menu_title[3])
        menu_desc_group_layout4.addWidget(menu_img_label4, 0, 0, total, 1, Qt.AlignCenter)
        for i in range(total):
            title_label = QLabel("  {}".format(self.menu_title[3][i]), self)
            title_label.setFixedWidth(100)
            title_label.setFont(title_font)
            desc_label = QLabel(self.menu_desc[3][i], self)
            menu_desc_group_layout4.addWidget(title_label, i, 1)
            menu_desc_group_layout4.addWidget(desc_label, i, 2)

        scroll = QScrollArea()
        scroll.setWidget(central_widget)
        scroll.setWidgetResizable(True)
        central_layout = QVBoxLayout(self)
        central_layout.addWidget(scroll)
        self.show()
