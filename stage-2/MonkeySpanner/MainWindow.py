import datetime
import sys

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QCursor
from PyQt5.QtWidgets import *

from modules.UI.MenuBar import MenuBar
from modules.UI.ArtifactTable import ArtifactTable
from modules.UI.LoadingScreen import LoadingWidget
from modules.UI.FilteringWidget import FilteringWidget
import modules.constant as CONSTANT

class Main(QMainWindow):
    def __init__(self, env):
        super().__init__()
        self.env = [env, False]
        self.top_widget_height = 35
        self.pointer_cursor = QCursor(Qt.PointingHandCursor)
        self.number_of_thread = 0
        self.thread_count = 0
        self.analyzing_tab_number = -1
        self.analyzed_tab_number = -1
        self.adding_tab_number = -1
        self.window_list = []
        self.table_dict = {}
        self.ui()

    def ui(self):
        # Set up default UI
        self.setWindowTitle(CONSTANT.TITLE)
        self.setWindowIcon(QIcon(CONSTANT.ICON_PATH[0]))
        self.setStatusBar(QStatusBar())

        # Set up Layout
        top_layout = QBoxLayout(QBoxLayout.LeftToRight)
        bottom_layout = QBoxLayout(QBoxLayout.TopToBottom)
        top_widget = QWidget()
        top_widget.setLayout(top_layout)
        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_layout)
        splitter = QSplitter(Qt.Vertical, self)
        splitter.addWidget(top_widget)
        splitter.addWidget(bottom_widget)
        self.setCentralWidget(splitter)

        # Set up Table Load Button
        analyze_btn = QPushButton(top_widget)
        analyze_btn.setIcon(QIcon(CONSTANT.ICON_PATH[-1]))
        analyze_btn.setFixedSize(self.top_widget_height, self.top_widget_height)
        analyze_btn.setStyleSheet("background-color: darkslategray;")
        analyze_btn.setShortcut("Ctrl+D")
        analyze_btn.setToolTip("Ctrl+D")
        analyze_btn.clicked.connect(self.analyze)
        analyze_btn.setCursor(self.pointer_cursor)

        # Set up check box (Filtering)
        self.filtering_widget = FilteringWidget()
        self.filtering_widget.sw_filter_btn.clicked.connect(self.filter_by_software)
        self.filtering_widget.simple_filter_btn.clicked.connect(self.filter_in_parent_table)
        self.filtering_widget.tree.itemChanged.connect(self.filter_in_child_table)
        
        filter_btn = QPushButton(top_widget)
        filter_btn.setIcon(QIcon(CONSTANT.ICON_PATH[1]))
        filter_btn.setFixedSize(self.top_widget_height, self.top_widget_height)
        filter_btn.setStyleSheet("background-color: darkslategray")
        filter_btn.setShortcut("Ctrl+A")
        filter_btn.setToolTip("Ctrl+A")
        filter_btn.clicked.connect(self.filtering_widget.show)
        filter_btn.setCursor(self.pointer_cursor)

        # Set up text box for Search
        self.search_box = QLineEdit(top_widget)
        self.search_box.setFixedHeight(self.top_widget_height)
        self.search_box.showMaximized()
        self.search_box.setFont(QFont("Arial", 12))
        self.search_box.setPlaceholderText("Search")
        self.search_box.returnPressed.connect(self.search)

        self.tab = QTabWidget(self)
        from modules.UI.HomeWidget import HomeWidget
        self.home_widget = HomeWidget(self.tab)
        self.tab.addTab(self.home_widget, "Home")
        self.tab.setContentsMargins(0, 0, 0, 0)
        self.tab.setTabsClosable(True)
        self.tab.tabBar().setCursor(self.pointer_cursor)
        self.tab.currentChanged.connect(self.on_changed_tab)
        self.tab.tabCloseRequested.connect(self.on_closed_tab)
        self.tab.tabBarDoubleClicked.connect(self.convert_tab_to_window)

        self.search_thread = SearchThread()
        self.search_thread.completed.connect(self.on_finished_searching)

        self.export_xml_thread = ExportXMLThread()
        self.export_xml_thread.completed.connect(self.on_finished_exporting)
        self.export_xml_thread.performanced.connect(self.statusBar().showMessage)

        self.import_xml_thread = ImportXMLThread()
        self.import_xml_thread.completed.connect(self.on_finished_importing)
        self.import_xml_thread.performanced.connect(self.statusBar().showMessage)

        top_layout.addWidget(analyze_btn)
        top_layout.addItem(QSpacerItem(5, self.top_widget_height))
        top_layout.addWidget(filter_btn)
        top_layout.addItem(QSpacerItem(5, self.top_widget_height))
        top_layout.addWidget(self.search_box)
        bottom_layout.addWidget(self.tab)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        self.setMenuBar(MenuBar(self))
        self.setMinimumWidth(self.width())
        self.showMaximized()

    def get_tab_text(self, old_text):
        new_tab_text = old_text
        new_tab_text_len = len(new_tab_text)
        max = 0
        for i in range(self.tab.count()):
            tab_text = self.tab.tabText(i)
            if tab_text.startswith(new_tab_text):
                if len(tab_text) == new_tab_text_len:
                    max = 1
                    continue
                old_idx = int(tab_text[-2])
                if old_idx > max:
                    max = old_idx
        if not max:
            return new_tab_text
        new_tab_text += " ({})".format(max + 1)
        return new_tab_text

    def analyze(self):
        if self.analyzing_tab_number != -1:
            QMessageBox.information(self, "Help", "Currently under analysis.", QMessageBox.Ok)
            return
        self.analyzing_tab_number = -2
        
        if not self.env[1]:
            self.create_dir()

        import modules.ArtifactAnalyzer as Analyzer
        self.artifacts_list = []
        thread_list = [
            Analyzer.AppEvtxAnalyzerThread(self.env, self.artifacts_list),
            Analyzer.FaultHeapEvtxAnalyzerThread(self.env, self.artifacts_list),
            Analyzer.OAlertsEvtxAnalyzerThread(self.env, self.artifacts_list),
            Analyzer.PrefetchAnalyzerThread(self.env, self.artifacts_list),
            Analyzer.WebArtifactAnalyzerThread(self.env, self.artifacts_list),
            Analyzer.AppCompatCacheAnalyzerThread(self.env, self.artifacts_list),    # File Copy NOT
            Analyzer.JumpListAnalyzerThread(self.env, self.artifacts_list),
        ]
        if self.env[0] == CONSTANT.WIN7:
            thread_list.append(Analyzer.WERDiagEvtxAnalyzerThread(self.env, self.artifacts_list))

        self.number_of_thread = len(thread_list)

        import time
        self.start_time = time.time()
        for t in thread_list:
            t.completed.connect(self.on_finished_thread)
            t.start()

        new_tab_text = self.get_tab_text("All Results")

        loading_widget = LoadingWidget(self, self.number_of_thread)
        idx = self.tab.addTab(loading_widget, new_tab_text)
        self.analyzing_tab_number = idx
        self.tab.setCurrentIndex(idx)
        loading_widget.start()

    def on_finished_thread(self):
        self.thread_count += 1
        widget = self.tab.widget(self.analyzing_tab_number)
        if self.thread_count != self.number_of_thread:
            widget.resume()
        else:
            self.show_analysis_result_tab(widget)

    def show_analysis_result_tab(self, widget):
        import time
        from operator import itemgetter
        self.artifacts_list.sort(key=itemgetter(1))
        status_msg = "total [{}],  {} seconds".format(len(self.artifacts_list), (time.time() - self.start_time))
        self.statusBar().showMessage(status_msg)
        tab_text = self.tab.tabText(self.analyzing_tab_number)
        tab_idx = self.tab.insertTab(self.analyzing_tab_number,
                                    ArtifactTable(self.tab, self.artifacts_list, is_parent=True),
                                     tab_text)
        self.tab.removeTab(tab_idx + 1)
        logs = widget.logLabel.logs
        widget.deleteLater()
        self.tab.setCurrentIndex(tab_idx)
        self.analyzed_tab_number = self.analyzing_tab_number
        self.analyzing_tab_number = -1
        self.filtering_widget.changeStatusForNoColorParentTable()
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S%f")
        with open(self.env[-1] + "{}.log".format(timestamp), 'w') as f:
            f.write(logs)

    def filter_by_software(self):
        checked_sw = {
            chk_box.text(): CONSTANT.SOFTWARE[chk_box.text()] for chk_box in self.filtering_widget.chk_list if chk_box.isChecked()
        }
        parent_table = self.tab.currentWidget()
        new_list = []
        for item in parent_table.artifacts_list:
            if item[0][0] == CONSTANT.REGISTRY_KEYWORD: continue        # 중복 색상 구분 추가 시, 해당문장 제거
            if item[0][1] or item[0][2] in checked_sw.values():
                new_list.append(item)

        new_tab_text = self.get_tab_text("App")

        self.adding_tab_number = self.tab.addTab(ArtifactTable(self.tab, new_list, selected_sw=list(checked_sw.values())),
                                                 new_tab_text)
        
        child_table = self.tab.widget(self.adding_tab_number)
        child_table.setToolTip(", ".join(checked_sw.keys()) + "\nFrom \"{}\" Tab".format(self.tab.tabText(self.tab.currentIndex())))
        child_table.navigated.connect(self.navigate)
        self.tab.setCurrentIndex(self.adding_tab_number)
        self.filtering_widget.set_checked_status(parent_table.checked_status)
        self.filtering_widget.change_status_for_color_table()
        self.table_dict[child_table] = parent_table
        self.adding_tab_number = -1

    def filter_in_parent_table(self):
        checked = self.filtering_widget.getCheckedItems()
        tab_idx = self.tab.currentIndex()
        parent_table = self.tab.widget(tab_idx)
        artifacts_list_of_child_table = []
        if parent_table.selected_sw:
            for r in range(len(parent_table.artifacts_list)):
                row = parent_table.artifacts_list[r]
                if row[0][0] in checked["Artifact"] and row[0][3] in checked["Color"]:
                    artifacts_list_of_child_table.append(parent_table.artifacts_list[r])
            by_str = "\n".join(checked["Artifact"]) + "\nColor Number: " + ", ".join(map(str, checked["Color"]))
            self.filtering_widget.change_status_for_color_table()
        else:
            for r in range(len(parent_table.artifacts_list)):
                row = parent_table.artifacts_list[r]
                if row[0][0] in checked["Artifact"]:
                    artifacts_list_of_child_table.append(parent_table.artifacts_list[r])
            by_str = "\n".join(checked["Artifact"])
            self.filtering_widget.change_status_for_no_color_table()

        new_tab_text = self.get_tab_text("Filtered")
        self.adding_tab_number = self.tab.addTab(ArtifactTable(self.tab,
                                                               artifacts_list_of_child_table,
                                                               checked_status=self.filtering_widget.get_checked_status()),
                                                 new_tab_text)
        child_table = self.tab.widget(self.adding_tab_number)
        tool_tip = "filter_in_child_table by: \n  {}\nFrom \"{}\" Tab".format(by_str, self.tab.tabText(new_tab_text))
        child_table.setToolTip(tool_tip)
        child_table.navigated.connect(self.navigate)
        self.tab.setCurrentIndex(self.adding_tab_number)
        self.filtering_widget.setCheckedStatus(child_table.checked_status)
        self.table_dict[child_table] = parent_table
        self.adding_tab_number = -1

    def filter_in_child_table(self, checked_item, p_int):
        widget = self.tab.currentWidget()
        if widget.is_parent: return
        widget.filter_in_child_table(checked_item, p_int)

    def search(self):
        tab_idx = self.tab.currentIndex()
        if tab_idx == self.analyzing_tab_number: return
        tab_text = self.tab.tabText(tab_idx)
        if tab_text == "Home": return
        
        keyword = self.search_box.text()
        widget = self.tab.currentWidget()
        if widget.is_parent:
            if not keyword: return
            self.search_thread.set_target(widget, keyword)
            self.search_thread.start()
        else:
            if not keyword:
                widget.search(keyword, self.filtering_widget.get_checked_items())
            else:
                widget.search(keyword)

    def on_finished_searching(self, artifacts_list, parent_table):
        new_tab_text = self.get_tab_text("Search")
        child_table = ArtifactTable(self.tab, artifacts_list, selected_sw=parent_table.selected_sw)
        
        self.adding_tab_number = self.tab.addTab(child_table, new_tab_text)
        child_table.setToolTip("From \"{}\" Tab".format(self.tab.tabText(self.tab.indexOf(parent_table))))
        child_table.navigated.connect(self.navigate)
        self.tab.setCurrentIndex(self.adding_tab_number)
        if parent_table.selected_sw:
            self.filtering_widget.change_status_for_color_table()
        else:
            self.filtering_widget.change_status_for_no_color_table()
        self.table_dict[child_table] = parent_table
        self.adding_tab_number = -1

    def navigate(self, row):
        parent_table = self.table_dict[self.sender()]
        parent_table.selectRow(row)
        self.tab.setCurrentWidget(parent_table)

    def on_changed_tab(self, idx):
        tab_text = self.tab.tabText(idx)
        if idx == self.analyzing_tab_number or idx == self.adding_tab_number: return
        if tab_text.startswith("Home"):
            self.filtering_widget.setEnabled(False)
            return
        widget = self.tab.widget(idx)
        self.filtering_widget.set_checked_status(widget.checked_status)
        if widget.is_parent:
            if widget.selected_sw:
                self.filtering_widget.change_status_for_color_parent_table()
            else:
                self.filtering_widget.change_status_for_no_color_parent_table()
        else:
            if widget.selected_sw:
                self.filtering_widget.change_status_for_color_table()
            else:
                self.filtering_widget.change_status_for_no_color_table()

    def on_closed_tab(self, idx):
        if self.tab.tabText(0) == "Home":
            self.tab.removeTab(idx)
            return
        self.tab.widget(idx).deleteLater()
        self.tab.removeTab(idx)
        if idx == self.analyzing_tab_number:
            self.analyzing_tab_number = -1
            self.artifacts_list.clear()

    def convert_tab_to_window(self, tab_idx):
        if len(self.window_list) == 5:
            QMessageBox(self, "Help", "Up to 5 can be converted.", QMessageBox.Ok)
            return
        tab_text = self.tab.tabText(tab_idx)
        if tab_text == "Home":
            self.tab.removeTab(tab_idx)
            self.home_widget.setParent(None)
            self.home_widget.setWindowTitle(tab_text)
            self.home_widget.setWindowIcon(QIcon(CONSTANT.ICON_PATH[0]))
            self.home_widget.show()
            return
        widget = self.tab.widget(tab_idx)
        if widget.is_parent:
            QMessageBox.information(self, "Help", "The entire result can not be converted.", QMessageBox.Ok)
            return
        elif tab_text.startswith("CSV"):
            from modules.UI.SubWindow import SubWindow
            self.tab.removeTab(tab_idx)
            sub_window = SubWindow(tab_text, widget, is_contents_from_table=True, does_detail_exists=False)
        else:
            from modules.UI.SubWindow import SubWindow
            self.tab.removeTab(tab_idx)
            sub_window = SubWindow(tab_text, widget, is_contents_from_table=True)
        sub_window.onCloseSignal.connect(self.sub_window_closed)
        self.window_list.append(sub_window)
        self.window_list[-1].show()

    def sub_window_closed(self, event):
        reply = QMessageBox.information(self.sender(), "Help", "Replace with tab?", QMessageBox.Yes, QMessageBox.No)
        event.accept()
        if reply == QMessageBox.Yes:
            table = self.sender().table
            table.setParent(self.tab)
            self.tab.addTab(self.sender().table, self.sender().windowTitle())
            self.tab.setCurrentWidget(table)
            self.window_list.remove(self.sender())

    def show_home_tab(self):
        if self.tab.tabText(0) == "Home": return
        self.tab.insertTab(0, self.home_widget, "Home")

    def create_dir(self):
        import os
        cwd = os.getcwd()
        root_dir = cwd + "\\MonkeySpanner"
        time_str = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")
        db_dir = "{}\\{}\\".format(root_dir, time_str)
        file_system_dir = db_dir + "FileSystem\\"
        artifacts_dir = db_dir + "Artifacts\\"
        csv_dir = db_dir + "csv\\"
        log_dir = db_dir + "log\\"
        pf_dir = artifacts_dir + "PF\\"
        evtx_dir = artifacts_dir + "Evtx\\"
        reg_dir = artifacts_dir + "Reg\\"
        wer_dir = artifacts_dir + "WER\\"
        jumplist_dir = artifacts_dir + "JumpList\\"

        if not os.path.exists(root_dir):
            os.mkdir(root_dir)
        if not os.path.exists(db_dir):
            os.mkdir(db_dir)
            os.mkdir(file_system_dir)
            os.mkdir(artifacts_dir)
            os.mkdir(csv_dir)
            os.mkdir(log_dir)
            os.mkdir(pf_dir)
            os.mkdir(evtx_dir)
            os.mkdir(reg_dir)
            os.mkdir(wer_dir)
            os.mkdir(jumplist_dir)
        self.env.extend([
            db_dir,
            artifacts_dir,
            [pf_dir, evtx_dir, wer_dir, jumplist_dir, reg_dir],
            file_system_dir,
            csv_dir,
            log_dir
        ])

        '''
        self.env = [
            OS Information,
            isImported, (True/False) -- default=False
            dbDir,
            artifactsDir,
            [pfDir, evtxDir, werDir, jumpListDir, regDir],
            file_system_dir,
            csv_dir,
            log_dir
        ]
        '''

    def import_dir(self):
        import os
        file_name = os.path.normpath(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if file_name == '.': return
        dir_list = ["{}\\".format(file_name)]
        for child in os.listdir(file_name):
            if child == "Artifacts":
                artifacts_dir = "{}\\{}\\".format(file_name, child)
                dir_list.append(artifacts_dir)
                dir_list.append([
                    False if not os.path.exists(artifacts_dir + "PF\\") else artifacts_dir + "PF\\",
                    False if not os.path.exists(artifacts_dir + "Evtx\\") else artifacts_dir + "Evtx\\",
                    False if not os.path.exists(artifacts_dir + "WER\\") else artifacts_dir + "WER\\",
                    False if not os.path.exists(artifacts_dir + "JumpList\\") else artifacts_dir + "JumpList\\",
                    False if not os.path.exists(artifacts_dir + "Reg\\") else artifacts_dir + "Reg\\",
                ])
                break
        if len(dir_list) == 1:
            QMessageBox.warning(self, "Help", "Please Select Directory", QMessageBox.Ok)
            return

        file_system_dir = "{}\\{}\\".format(file_name, "FileSystem")
        csv_dir = "{}\\csv\\".format(file_name)
        log_dir = "{}\\log\\".format(file_name)
        if not os.path.exists(file_system_dir):
            os.mkdir(file_system_dir)
        if not os.path.exists(csv_dir):
            os.mkdir(csv_dir)
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        dir_list.extend([file_system_dir, csv_dir, log_dir])
        self.env.extend(dir_list)
        self.env[1] = True
        self.analyze()

    def import_csv(self):
        import os, csv
        dir_path = os.getcwd()+"\\" if len(self.env) == 2 else self.env[6]
        file_name, _ = QFileDialog.getOpenFileName(self, "Import CSV", dir_path, filter="*.csv")
        if not file_name and not _: return
        try:
            with open(file_name, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                first_row = next(reader)
                selected_sw = first_row[-1].split("=")[1]
                selected_sw = None if selected_sw == 'None' else list(map(int, selected_sw.split("/")))
                result = []
                for row in reader:
                    head = row[0].split("/")
                    head[1] = True if head[1] == "True" else False
                    head[2:] = map(int, head[2:])
                    if head[0] == CONSTANT.HISTORY_KEYWORD:
                        result.append([head] + row[1:4])
                    elif head[0] == CONSTANT.PREFETCH_KEYWORD:
                        result.append([head] + row[1:5])
                    else:
                        result.append([head] + row[1:6])
        except Exception as e:
            QMessageBox.warning(self, "Error", "{}".format(e), QMessageBox.Ok)
            return
        parent_table = ArtifactTable(self.tab, result, is_parent=True, selected_sw=selected_sw)
        idx = self.tab.addTab(parent_table, self.get_tab_text("CSV"))
        self.adding_tab_number = idx
        parent_table.is_detail_allowed = False
        parent_table.setToolTip(file_name)
        self.tab.setCurrentIndex(idx)
        if selected_sw:
            self.filtering_widget.change_status_for_color_parent_table()
        else:
            self.filtering_widget.change_status_for_no_color_parent_table()
        self.adding_tab_number = -1

    def export_as_csv(self):
        tab_idx = self.checkTab()
        if tab_idx < 0 or self.tab.tabText(tab_idx).startswith("Home"):
            QMessageBox.information(self, "Help", "Select a Tab of analysis result.", QMessageBox.Ok)
            return
        import os
        dir_path = os.getcwd()+"\\" if len(self.env) == 2 else self.env[6]
        try:
            time_str = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")
            tmp_file_name = "{}_{}".format(time_str, self.tab.tabText(tab_idx).replace(" ", "-"))
            file_name, ext = QFileDialog.getSaveFileName(self, "Save as CSV", dir_path + tmp_file_name, filter=".csv")
            if not file_name.endswith(ext):
                file_name += ext
            import csv
            with open(file_name, 'w', newline='', encoding="utf-8") as f:
                widget = self.tab.widget(tab_idx)
                sw = "/".join(map(str, widget.selected_sw)) if widget.selected_sw else None
                fieldnames = [
                    "Head Data(Type/...)", "Column 1", "Column 2", "Column 3", "Column 4", "Column 5",
                    "checkedSW={}".format(sw)
                ]
                w = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
                w.writeheader()
                for row in widget.artifacts_list:
                    csv_row = ["/".join(map(str, row[0]))]
                    if row[0][0] == CONSTANT.HISTORY_KEYWORD:
                        csv_row.extend(row[1:4])
                    elif row[0][0] == CONSTANT.PREFETCH_KEYWORD:
                        csv_row.extend(row[1:5])
                    else:
                        csv_row.extend(row[1:6])
                    _dict = {fieldnames[n]: csv_row[n] for n in range(len(csv_row))}
                    w.writerow(_dict)
        except Exception as e:
            QMessageBox.critical(self, "Error", "{}".format(e), QMessageBox.Ok)
            return
        reply = QMessageBox.information(self, "Help", "Success !", QMessageBox.Open, QMessageBox.Close)
        if reply == QMessageBox.Open:
            import subprocess
            subprocess.call('explorer.exe {}'.format(os.path.normpath(file_name).rsplit("\\", 1)[0]), shell=True)

    def import_xml(self):
        tab_idx = self.check_export_status()
        if not tab_idx: return
        import os
        dir_path = os.getcwd() + "\\" if len(self.env) == 2 else self.env[2]
        file_name, _ = QFileDialog.getOpenFileName(self, "Import XML", dir_path, filter="*.xml")
        if not file_name and not _: return
        self.import_xml_thread.set_target(file_name)
        self.import_xml_thread.start()

    def export_as_xml(self):
        tab_idx = self.check_export_status()
        if not tab_idx: return
        import os
        dir_path = os.getcwd()+"\\" if len(self.env) == 2 else self.env[2]
        time_str = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")
        tmp_file_name = "{}_{}_lite".format(time_str, self.tab.tabText(tab_idx).replace(" ", "-"))
        file_name, ext = QFileDialog.getSaveFileName(self, "Export current results as XML", dir_path + tmp_file_name, filter=".xml")
        if not file_name and not ext: return
        if not file_name.endswith(ext):
            file_name += ext
        self.export_xml_thread.set_target(self.tab.widget(tab_idx), time_str, os.path.normpath(file_name), True)
        self.export_xml_thread.start()

    def export_all_as_xml(self):
        tab_idx = self.check_export_status()
        if not tab_idx: return
        import os
        dir_path = os.getcwd()+"\\" if len(self.env) == 2 else self.env[2]
        time_str = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")
        tmp_file_name = "{}_{}".format(time_str, self.tab.tabText(tab_idx).replace(" ", "-"))
        file_name, ext = QFileDialog.getSaveFileName(self, "Export all results as XML", dir_path + tmp_file_name, filter=".xml")
        if not file_name and not ext: return
        if not file_name.endswith(ext):
            file_name += ext
        self.export_xml_thread.set_target(self.tab.widget(tab_idx), time_str, os.path.normpath(file_name), False)
        self.export_xml_thread.start()

    def check_export_status(self):
        if self.export_xml_thread.is_exporting:
            QMessageBox.information(self, "Help", "Being exported, please take a moment.", QMessageBox.Ok)
            return False
        elif self.import_xml_thread.is_importing:
            QMessageBox.information(self, "Help", "Being imported, please take a moment.", QMessageBox.Ok)
            return False
        tab_idx = self.tab.currentIndex()
        if tab_idx == self.analyzing_tab_number:
            QMessageBox.information(self, "Help", "Currently under analysis.", QMessageBox.Ok)
            return False
        if self.tab.currentWidget() is self.home_widget:
            QMessageBox.information(self, "Help", "Please select another tab.", QMessageBox.Ok)
            return False
        return tab_idx
    
    def on_finished_importing(self, attr, result):
        parent_table = ArtifactTable(self.tab, result, is_parent=True, selected_sw=attr[2])
        parent_table.setToolTip("{} - {}".format(attr[0], attr[1]))
        idx = self.tab.addTab(parent_table, self.get_tab_text("XML"))
        self.adding_tab_number = idx
        self.tab.setCurrentIndex(idx)
        if attr[2]:
            self.filtering_widget.change_status_for_color_parent_table()
        else:
            self.filtering_widget.change_status_for_no_color_parent_table()
        self.adding_tab_number = -1

    def on_finished_exporting(self, dir_path):
        reply = QMessageBox.information(self, "Help", "Success !", QMessageBox.Open, QMessageBox.Close)
        if reply == QMessageBox.Open:
            import subprocess
            subprocess.call('explorer.exe {}'.format(dir_path), shell=True)
    
class SearchThread(QThread):
    completed = pyqtSignal(list, ArtifactTable)

    def __init__(self):
        QThread.__init__(self)

    def set_target(self, table, keyword):
        self.table = table
        self.keyword = keyword

    def run(self):
        items = self.table.findItems(self.keyword, Qt.MatchContains)
        included_rows = list(set([self.table.row(item) for item in items]))
        if not included_rows:
            QMessageBox.information(self, "Help", "Not found.", QMessageBox.Ok)
            return
        _list = []
        for row in included_rows:
            _list.append(self.table.artifacts_list[row])
        self.completed.emit(_list, self.table)

class ImportXMLThread(QThread):
    completed = pyqtSignal(list, list)
    performanced = pyqtSignal(str)
    
    def __init__(self):
        QThread.__init__(self)
        self.is_importing = False

    def set_target(self, file_name):
        self.file_name = file_name

    def run(self):
        self.is_importing = True
        from xml.etree.ElementTree import parse
        try:
            with open(self.file_name, encoding='utf-8') as f:
                tree = parse(f)
                root = tree.getroot()
                result = []

                selected_sw = root.get("selectedSW")
                selected_sw = None if selected_sw == 'None' else list(map(int, selected_sw.split("/")))
                row_count = int(root.get("rowCount"))
                r = 0
                for row_tag in root.getchildren():
                    head = row_tag.get("type").split("/")
                    head[1] = True if head[1] == "True" else False
                    head[2:] = map(int, head[2:])
                    row = [head]
                    row.extend([col.text for col in row_tag.findall("column")])
                    detail_tag = row_tag.find("detail")
                    if head[0] == CONSTANT.PREFETCH_KEYWORD:
                        contents = [
                            detail_tag.find("name").text,
                            [val for key, val in detail_tag.find("information").items()],
                            [val for key, val in detail_tag.find("mft").items()],
                            [timeTag.text for timeTag in detail_tag.find("execution_time").getchildren()],
                            [val for key, val in detail_tag.find("volumn").items()],
                            [stringTag.text for stringTag in detail_tag.find("dir_strings").getchildren()],
                            [rscTag.text for rscTag in detail_tag.find("loadedResources").getchildren()],
                        ]
                    elif head[0] in [CONSTANT.HISTORY_KEYWORD, CONSTANT.CACHE_KEYWORD, CONSTANT.DOWNLOAD_KEYWORD]:
                        contents = [dataTag.text for dataTag in detail_tag.getchildren()]
                    elif head[0] in [CONSTANT.LNKFILE_KEYWORD, CONSTANT.DESTLIST_KEYWORD]:
                        contents = [
                            detail_tag.find("name").text,
                            detail_tag.find("software").text,
                            detail_tag.find("type").text,
                            [dataTag.text for dataTag in detail_tag.findall("data")]
                        ]
                    else:
                        contents = detail_tag.text
                    row.append(contents)
                    result.append(row)
                    r += 1
                    self.performanced.emit("Importing {}/{} - {}".format(r, row_count, self.file_name))
        except Exception as e:
            QMessageBox.warning(self, "Error", "{}".format(e), QMessageBox.Ok)
            return
        self.completed.emit([self.file_name, root.get("timestamp"), selected_sw], result)
        self.is_importing = False

class ExportXMLThread(QThread):
    completed = pyqtSignal(str)
    performanced = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.is_exporting = False

    def set_target(self, table, time_str, file_name, is_current_results):
        self.table = table
        self.time_str = time_str
        self.file_name = file_name
        self.is_current_results = is_current_results

    def run(self):
        self.is_exporting = True
        try:
            detail_idx = -2
            from xml.etree.ElementTree import ElementTree, Element, SubElement
            sw = "/".join(map(str, self.table.selected_sw)) if self.table.selected_sw else None
            root = Element(
                "root",
                timestamp=self.time_str,
                selectedSW="{}".format(sw),
            )
            r = 0
            r2 = 0
            total = len(self.table.artifacts_list)
            for item in self.table.artifacts_list:
                r += 1
                if self.is_current_results and self.table.isRowHidden(r):
                    continue
                r2 += 1
                row = Element("row", type="/".join(map(str, item[0])))
                if item[0][0] == CONSTANT.HISTORY_KEYWORD:
                    max_columns = 3
                elif item[0][0] == CONSTANT.PREFETCH_KEYWORD:
                    max_columns = 4
                else:
                    max_columns = 5
                for i in range(1, max_columns + 1):
                    SubElement(row, "column").text = item[i]
                detail = Element("detail")
                if item[0][0] == CONSTANT.PREFETCH_KEYWORD:
                    SubElement(detail, "name").text = item[detail_idx][0]
                    information = Element("information", execName=item[detail_idx][1][0], runCount=item[detail_idx][1][1])
                    detail.append(information)
                    mft = Element("mft", seqNum=item[detail_idx][2][0], entryNum=item[detail_idx][2][1])
                    detail.append(mft)
                    execution_time = Element("execution_time")
                    for t in item[detail_idx][3]:
                        SubElement(execution_time, "time").text = t
                    detail.append(execution_time)

                    volume = Element("volumn", name=item[detail_idx][4][0], created=item[detail_idx][4][1], serial=item[detail_idx][4][2])
                    detail.append(volume)

                    dir_strings = Element("dir_strings")
                    for string in item[detail_idx][5]:
                        SubElement(dir_strings, "string").text = string
                    detail.append(dir_strings)

                    loaded = Element("loadedResources")
                    for rsc in item[detail_idx][6]:
                        SubElement(loaded, "resource").text = rsc
                    detail.append(loaded)
                elif item[0][0] in [CONSTANT.HISTORY_KEYWORD, CONSTANT.CACHE_KEYWORD, CONSTANT.DOWNLOAD_KEYWORD]:
                    for i in item[detail_idx]:
                        SubElement(detail, "data").text = i
                elif item[0][0] in [CONSTANT.LNKFILE_KEYWORD, CONSTANT.DESTLIST_KEYWORD]:
                    SubElement(detail, "name").text = item[detail_idx][0]
                    SubElement(detail, "software").text = item[detail_idx][1]
                    SubElement(detail, "type").text = item[detail_idx][2]
                    for i in item[detail_idx][3]:
                        SubElement(detail, "data").text = i
                else:
                    detail.text = item[detail_idx]
                row.append(detail)
                root.append(row)
                self.performanced.emit("Exporting ... {}/{} - {}".format(r, total, self.file_name))
            root.attrib["rowCount"] = str(r2)
            self.indent(root)
            ElementTree(root).write(self.file_name, encoding="utf-8")
        except Exception as e:
            QMessageBox.critical(self, "Error", "{}".format(e), QMessageBox.Ok)
            return
        self.completed.emit(self.file_name.rsplit("\\", 1)[0])
        self.is_exporting = False

    def indent(self, elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
