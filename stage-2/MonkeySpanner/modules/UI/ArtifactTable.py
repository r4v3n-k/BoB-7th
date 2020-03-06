import logging

from PyQt5.Qt import *
import modules.constant as CONSTANT

class ArtifactTable(QTableWidget, QObject):
    navigated = pyqtSignal(int)

    def __init__(self, parent, artifacts_list, is_parent=False, selected_sw=None, checked_status=None):
        QTableWidget.__init__(self, parent)
        QObject.__init__(self)
        self.is_detail_allowed = True
        self.artifacts_list = artifacts_list
        self.is_parent = is_parent
        self.selected_sw = selected_sw
        if not checked_status:
            self.checked_status = {
                    "Artifact": [Qt.Checked for i in range(len(CONSTANT.ARTIFACT_LIST))],
                    "Color": [Qt.Checked for i in range(len(CONSTANT.COLOR_LIST))],
            }
        else:
            self.checked_status = checked_status
        self.COLOR = [
            QColor(125, 125, 125, 30),
            QColor(255, 0, 0, 30),
            QColor(255, 125, 0, 30),
            QColor(255, 225, 0, 30),
            QColor(0, 255, 0, 30),
            QColor(0, 125, 255, 30),
            QColor(0, 0, 155, 30),
            QColor(155, 0, 225, 30),
        ]
        self.ui()

    def ui(self):
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["", "", "", "", "", ""])
        self.setRowCount(len(self.artifacts_list))
        # Align Column header
        for c in range(self.columnCount()):
            self.horizontalHeaderItem(c).setTextAlignment(Qt.AlignCenter)
        # Adjust row height
        self.verticalHeader().setDefaultSectionSize(28)
        self.verticalHeader().setMaximumSectionSize(28)
        # Handle event
        self.cellClicked.connect(self.change_column_header)  # One-Click
        self.cellDoubleClicked.connect(self.show_detail)  # Double-Click
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        row = 0
        for _list in self.artifacts_list:
            try:
                self.setVerticalHeaderItem(row, QTableWidgetItem(_list[0][0]))
                self.setItem(row, 0, QTableWidgetItem(_list[1]))
                self.setItem(row, 1, QTableWidgetItem(_list[2]))
                self.setItem(row, 2, QTableWidgetItem(_list[3]))
                if _list[0][0] == CONSTANT.HISTORY_KEYWORD:
                    self.item(row, 2).setTextAlignment(Qt.AlignCenter)
                    self.setItem(row, 3, QTableWidgetItem(""))
                    self.setItem(row, 4, QTableWidgetItem(""))
                elif _list[0][0] == CONSTANT.PREFETCH_KEYWORD:
                    self.setItem(row, 3, QTableWidgetItem(_list[4]))
                    self.item(row, 3).setTextAlignment(Qt.AlignCenter)
                    self.setItem(row, 4, QTableWidgetItem(""))
                else:
                    self.setItem(row, 3, QTableWidgetItem(_list[4]))
                    self.item(row, 3).setTextAlignment(Qt.AlignCenter | Qt.AlignRight)
                    self.setItem(row, 4, QTableWidgetItem(_list[5]))

                self.item(row, 0).setTextAlignment(Qt.AlignCenter)
                self.item(row, 4).setTextAlignment(Qt.AlignCenter)
                self.verticalHeaderItem(row).setTextAlignment(Qt.AlignRight)

                if self.selected_sw:
                    # Adjust COLOR of Row
                    if _list[0][1]:  # 공통
                        for c in range(self.columnCount()):
                            # swNum = 현재 선택된 소프트웨어 번호
                            # 중복일 경우 회색
                            if len(self.selected_sw) > 1:  # 선택된 소프트웨어가 1개 이상
                                for i in range(len(self.selected_sw) - 1):
                                    sw1 = self.selected_sw[i] + 1
                                    sw2 = self.selected_sw[i + 1] + 1
                                    if _list[0][sw1] != _list[0][sw2]:  # 색상이 다른 경우
                                        colorNum = 0  # 회색
                                        break;
                                    else:  # 색상이 같은 경우
                                        colorNum = _list[0][sw1]  # 그 색상으로
                            else:  # 선택된 소프트웨어가 1개일 경우
                                colorNum = _list[0][self.selected_sw[0]]
                            self.item(row, c).setBackground(self.COLOR[colorNum])
                    else:  # 공통이 아닌 경우
                        for c in range(self.columnCount()):
                            self.item(row, c).setBackground(self.COLOR[_list[0][3]])
                if self.is_parent:
                    _list.append(row)
                row += 1
            except Exception as e:
                logging.info("{}".format(e))
                pass

        # Adjust column width
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        header = self.horizontalHeader()
        self.setColumnWidth(0, 180)
        self.setColumnWidth(1, 550)
        self.setColumnWidth(2, 180)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        # self.show()

    def change_column_header(self, row, column):
        artifact_type = self.verticalHeaderItem(row).text()
        self.setHorizontalHeaderLabels(CONSTANT.TABLE_HEADER[artifact_type])

    def show_detail(self, row, column):
        if not self.is_detail_allowed: return
        viewer_title = self.verticalHeaderItem(row).text()
        viewer_content = self.artifacts_list[row][-2]
        if viewer_title == CONSTANT.PREFETCH_KEYWORD:
            from modules.UI.PrefetchDetailViewer import PrefetchDetailViewer
            self.pdv = PrefetchDetailViewer()
            self.pdv.ui(viewer_title, viewer_content)
        elif viewer_title in [CONSTANT.EVENTLOG_KEYWORD, CONSTANT.WER_KEYWORD, CONSTANT.REGISTRY_KEYWORD]:
            from modules.UI.TextViewer import TextViewer
            self.viewer = TextViewer()
            self.viewer.ui(viewer_title, viewer_content)
        elif viewer_title in [CONSTANT.HISTORY_KEYWORD, CONSTANT.CACHE_KEYWORD]:
            from modules.UI.WebArtifactDetailViewer import WebArtifactDetailViewer
            self.wadv = WebArtifactDetailViewer()
            self.wadv.ui(viewer_title, viewer_content)
        elif viewer_title == CONSTANT.LNKFILE_KEYWORD:
            from modules.UI.JumpListDetailViewer import JumpListDetailViewer
            self.jldv = JumpListDetailViewer()
            self.jldv.ui(JumpListDetailViewer.LNK_FILE, viewer_content)
        elif viewer_title == CONSTANT.DESTLIST_KEYWORD:
            from modules.UI.JumpListDetailViewer import JumpListDetailViewer
            self.jldv = JumpListDetailViewer()
            self.jldv.ui(JumpListDetailViewer.DEST_LIST, viewer_content)

    def search(self, keyword, checked_items=None):
        if not keyword:
            for row in range(len(self.artifacts_list)):
                if self.artifacts_list[row][0][0] in checked_items["Artifact"] \
                        and self.artifacts_list[row][0][3] in checked_items["Color"]:
                    if self.isRowHidden(row):
                        self.showRow(row)
            return
        items = self.findItems(keyword, Qt.MatchContains)
        included_rows = list(set([self.row(item) for item in items]))
        for row in range(len(self.artifacts_list)):
            if self.isRowHidden(row):
                continue
            if row in included_rows:
                self.showRow(row)
            else:
                self.hideRow(row)

    def filter(self, checked_item, i):
        target = checked_item.text(0)
        if target in CONSTANT.ARTIFACT_LIST:
            idx = CONSTANT.ARTIFACT_LIST.index(target)
            self.checked_status["Artifact"][idx] = checked_item.checkState(0)
            if checked_item.checkState(0) == Qt.Unchecked:
                for row in range(len(self.artifacts_list)):
                    if self.artifacts_list[row][0][0] == target:
                        self.hideRow(row)
            elif checked_item.checkState(0) == Qt.Checked:
                for row in range(len(self.artifacts_list)):
                    if self.artifacts_list[row][0][0] == target:
                        self.showRow(row)
        elif target in CONSTANT.COLOR_LIST.keys():
            target = CONSTANT.COLOR_LIST[target]
            self.checked_status["Color"][target] = checked_item.checkState(0)
            if checked_item.checkState(0) == Qt.Unchecked:
                for row in range(len(self.artifacts_list)):
                    if self.artifacts_list[row][0][3] == target:
                        self.hideRow(row)
            elif checked_item.checkState(0) == Qt.Checked:
                for row in range(len(self.artifacts_list)):
                    if self.artifacts_list[row][0][3] == target:
                        self.showRow(row)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        copy_action = menu.addAction("Copy")
        nav_action = QAction("Navigate", menu)
        menu.addAction(nav_action)
        if self.is_parent:
            nav_action.setDisabled(True)
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == copy_action:
            selected = self.selectedItems()
            if len(selected) == 1:
                copied = selected[0].text()
            else:
                copied = " ".join(currentQTableWidgetItem.text() for currentQTableWidgetItem in selected)
            import pyperclip
            pyperclip.copy(copied)
        elif action == nav_action:
            selected = self.selectedIndexes()
            original_row = self.artifacts_list[selected[0].row()][-1]
            self.navigated.emit(original_row)