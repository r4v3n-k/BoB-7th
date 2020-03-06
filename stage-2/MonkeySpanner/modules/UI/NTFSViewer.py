from PyQt5.QtGui import QCursor, QColor, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import *
from libs.ParseNTFS import MFT, LogFile, UsnJrnl, AttributeTypeEnum, BootSector
import datetime
from threading import Thread

'''

0. 파이썬 코딩 가이드 숙지.
1. 메모리를 많이 먹는 부분을 찾는다.
2. MFT, UsnJrnl, LogFile 객체 대신 제너레이터를 사용한다. (불필요한 메모리 낭비 방지)

[방법1]
Main Thread --> BootSector/MFT      --> 필요부분만 list
    (1) 1024 바이트씩 읽어서 리스트를 만든다.
    (2) 절대 경로는 리스트가 만들어진 뒤 인덱싱(=엔트리 번호)을 통해 얻도록 한다.
ㄴ Thread 2 --> UsnJrnl Generator  --> 필요부분만 list --> UsnJrnlTable
    (1) record 종류를 알아야 크기를 추측할 수 있으므로, 첫 ?바이트를 먼저 읽는다.
    (2) 뽑는 족족 QTableWidgetItem을 생성한다.
ㄴ Thread 3 --> LogFile Generator  --> 필요부분만 list --> LogFileTable
    (1) record 종류를 알아야 크기를 추측할 수 있으므로, 첫 ?바이트를 먼저 읽는다.
    (2) 뽑는 족족 QTableWidgetItem을 생성한다.
        [+] 트랜잭션에 필요한 부분도 함께 뽑을 것
    (3) 트랜잭션: 트랜잭션 id를 키로 갖고, lsn을 값으로 갖는 리스트를 반환
    
3. UsnJrnl 과 연관된 트랜잭션 로그는 직접 접근이 가능하도록 해야 함. (인덱스 = 트랜잭션 ID or MFT Entry ID)
4. QTableWidgetItem 을 생성하는 것과 함께 [방법1]이 수행되어야 함.

'''

class NTFSViewer(QWidget):
    USNJRNL = 1
    LOGFILE = 2
    ONLY_SHOW = 1
    ONLY_HIDE = 2
    SIMPLE_SHOW = 3
    CREATE_KEYWORD = "FILE_CREATE"
    DELETE_KEYWORD = "FILE_DELETE"
    EXTEND_KEYWORD = "DATA_EXTEND"
    OVERWRITE_KEYWORD = "DATA_OVERWRITE"

    def __init__(self, env=None):
        QWidget.__init__(self)
        import os
        '''
        if len(env) == 2:
            self.db_dir = os.getcwd() + "\\"
        else:
            self.db_dir = env[5]
        '''
        self.db_dir = os.getcwd() + "\\"

        from modules.UI.NTFSLogFileDialog import NTFSLogFileDialog
        self.ntfs_dialog = NTFSLogFileDialog(self)
        self.ntfs_dialog.submit_btn.clicked.connect(self.ready)
        self.selected_btn_num = 0
        self.is_recovery_allowed = False
        self.usnjrnl_table_header_labels = ['Timestamp', 'USN', 'File Name', 'Full Path', 'Reason', 'File Attributes', 'Source']
        self.logfile_table_header_labels = ['LSN', 'Transaction #', 'MFT Modified Time', 'File Name', 'Full Path',
                                        'File Accessed Time', 'Redo Operation', 'Undo Operation', 'Cluster Index', 'Target VCN']
        self.filtering_text = {
            "Created Files": self.CREATE_KEYWORD,
            "Deleted Files": self.DELETE_KEYWORD,
            "Extended Files": self.EXTEND_KEYWORD,
            "Overwritten Files": self.OVERWRITE_KEYWORD,
        }

    def ready(self):
        if not self.ntfs_dialog.ntfs_log_file_chk_box.isChecked() and not self.ntfs_dialog.disk_raw_chk_box.isChecked():
            QMessageBox.information(self, "Help", "Please Select analyzed file type.", QMessageBox.Ok)
            return
        if self.ntfs_dialog.disk_raw_chk_box.isChecked():
            _path = self.ntfs_dialog.disk_raw_text_box.text()
            if self.ntfs_dialog.selected_partition == -1:
                import os
                disk_size = os.path.getsize(_path)
                if disk_size < 500:
                    QMessageBox.critical(self, "Error", "This is not a disk image file.", QMessageBox.Ok)
                    return

                disk_info = [[_path, str(disk_size)]]
                with open(_path, 'rb') as f:
                    checked = f.read(512)
                    if checked[510:512] != b"\x55\xaa":
                        QMessageBox.critical(self, "Error", "This is not a disk image file.", QMessageBox.Ok)
                        return

                    self.ntfs_dialog.disk_raw_group_box.setDisabled(True)
                    f.seek(0x1BE)
                    for i in range(4):
                        partition_info = []
                        partition_table = f.read(16)
                        if partition_table[4:5] == b"\x07":
                            file_system = "NTFS"
                        elif partition_table[4:5] in [b"\x05", b"\x0F"]:
                            file_system = "Extended Partition"
                        else:
                            disk_info.append(None)
                            continue
                        partition_info.append(file_system)

                        active = None
                        if partition_table[0] == "\x80":
                            active = "True"
                        elif partition_table[0] == "\x00":
                            active = "False"
                        else:
                            active = "Unknown"
                        partition_info.append(active)

                        partition_starting_sector = int.from_bytes(partition_table[8:12], byteorder='little')
                        partition_info.append(str(hex(partition_starting_sector * 512)))

                        partition_sector_number = int.from_bytes(partition_table[12:], byteorder='little')
                        partition_info.append(str(partition_sector_number))
                        partition_info.append(str(partition_sector_number * 512))

                        disk_info.append(partition_info)

                self.ntfs_dialog.change_interface(disk_info)
                return
            else:
                partition_starting_offset = self.ntfs_dialog.partition_items[self.ntfs_dialog.selected_partition-1].text(3)
                self.sector = BootSector(image_name=_path,
                                    offset_sectors=None,
                                    offset_bytes=int(partition_starting_offset, 16),
                                    sector_size=512)
                rst, msg = self.sector.getResult()
                if not rst:
                    QMessageBox.critical(self, "Error", msg, QMessageBox.Ok)
                    return
                else:
                    QMessageBox.information(self, "Help", msg, QMessageBox.Ok)
                self.is_recovery_allowed = True
        elif self.ntfs_dialog.ntfs_log_file_chk_box.isChecked():
            _path = [
                self.ntfs_dialog.mft_path_text_box.text(),
                self.ntfs_dialog.usnjrnl_path_text_box.text(),
                self.ntfs_dialog.logfile_path_text_box.text()
            ]
            self.ntfs_dialog.ntfs_log_group_box.setDisabled(True)
            self.ntfs_dialog.disk_raw_chk_box.setDisabled(True)
        rst, msg = self.check(_path)
        if rst:
            self.ui()
            self.ntfs_dialog.ready()
            try:
                t = Thread(target=self.load, args=())
                t.start()
            except Exception as e:
                QMessageBox.critical(self, "Error", "{}".format(e), QMessageBox.Ok)
                self.ntfs_dialog.accept()
                return
            self.ntfs_dialog.bar_thread.completed.connect(self.show_viewer)
        else:
            QMessageBox.critical(self, "Error", msg, QMessageBox.Ok)
            self.ntfs_dialog.accept()

    def show_viewer(self):
        alert_str = "MFT total entry: {0}\nUsnJrnl total record: {1}\nLogFile total record: {2}\nTransaction total: {3}" \
            .format(len(self.mft.entries), self.usnjrnl_len, self.logfile_len, len(self.logfile.transactions))
        QMessageBox.information(self, "Help", alert_str, QMessageBox.Ok)
        self.ntfs_dialog.accept()

        self.usnjrnl_export_bar.setMaximum(self.usnjrnl_len)
        self.logfile_export_bar.setMaximum(self.logfile_len)
        self.usnjrnl_export_thread = ExportThread(self.usnjrnl.records, self.USNJRNL, self.db_dir)
        self.usnjrnl_export_thread.change_value.connect(self.usnjrnl_export_bar.setValue)
        self.usnjrnl_export_thread.exported.connect(self.thread_finished)
        self.logfile_export_thread = ExportThread(self.logfile.rcrd_records, self.LOGFILE, self.db_dir)
        self.logfile_export_thread.change_value.connect(self.logfile_export_bar.setValue)
        self.logfile_export_thread.exported.connect(self.thread_finished)

        if self.is_recovery_allowed:
            self.recovery_thread = RecoveryThread(self.mft)
            self.recovery_thread.recoveried.connect(self.thread_finished)

        self.showMaximized()

    def check(self, path):
        if self.is_recovery_allowed:
            self.mft = MFT(image_name=path, boot_sector=self.sector)
            rst, output = self.mft.extract_data(inum=2, output_file=self.db_dir, stream=0, is_recovering=False)
            logfile_path = output

            usn_jrnl_inum = self.mft.entries[11]. \
                attributes[AttributeTypeEnum.INDEX_ROOT][0]. \
                entries[AttributeTypeEnum.FILE_NAME]['$UsnJrnl']. \
                file_reference_mft_entry
            rst, output = self.mft.extract_data(inum=usn_jrnl_inum, output_file=self.db_dir, stream=0, is_recovering=False)
            usnjrnl_path = output
        else:
            for p in path:
                if not p:
                    return False, "Please import log file."
            self.mft = MFT(image_name=path[0])
            usnjrnl_path = path[1]
            logfile_path = path[2]
        if not self.mft.entries[0].is_valid:
            return False, "Not $MFT file"
        self.usnjrnl = UsnJrnl(usnjrnl_path)
        error_dir = self.db_dir + "errorpages"
        self.logfile = LogFile(dump_dir=error_dir, file_name=logfile_path)
        return True, None

    def ui(self):
        from modules.constant import ICON_PATH
        self.setWindowIcon(QIcon(ICON_PATH[0]))
        self.setWindowTitle("File System Log")

        # Layout
        window_layout = QBoxLayout(QBoxLayout.TopToBottom, self)
        self.options_layout = QBoxLayout(QBoxLayout.LeftToRight)
        window_layout.addLayout(self.options_layout)

        # Set up Filtering
        self.group_box = QGroupBox(self)
        chk_layout = QHBoxLayout()
        self.group_box.setLayout(chk_layout)
        self.group_box.setMaximumWidth(860)
        self.create_chk_box = QCheckBox('Created Files', self)
        self.delete_chk_box = QCheckBox('Deleted Files', self)
        self.extend_chk_box = QCheckBox('Extended Files', self)
        self.overwrite_chk_box = QCheckBox("Overwritten Files", self)
        self.create_chk_box.stateChanged.connect(lambda: self.filter(self.create_chk_box))
        self.delete_chk_box.stateChanged.connect(lambda: self.filter(self.delete_chk_box))
        self.extend_chk_box.stateChanged.connect(lambda: self.filter(self.extend_chk_box))
        self.overwrite_chk_box.stateChanged.connect(lambda: self.filter(self.overwrite_chk_box))
        chk_layout.addWidget(self.create_chk_box)
        chk_layout.addWidget(self.delete_chk_box)
        chk_layout.addWidget(self.extend_chk_box)
        chk_layout.addWidget(self.overwrite_chk_box)

        # Set up Button
        self.usnjrnl_export_btn = QPushButton("Export $UsnJrnl as CSV", self)
        self.usnjrnl_export_btn.setFixedSize(200, 40)
        self.usnjrnl_export_btn.setStyleSheet("background-color: darkslategray;")
        self.usnjrnl_export_btn.clicked.connect(self.export_usn)
        self.usnjrnl_export_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.logfile_export_btn = QPushButton("Export $LogFile as CSV", self)
        self.logfile_export_btn.setFixedSize(200, 40)
        self.logfile_export_btn.setStyleSheet("background-color: darkslategray;")
        self.logfile_export_btn.clicked.connect(self.export_lsn)
        self.logfile_export_btn.setCursor(QCursor(Qt.PointingHandCursor))

        # Set up Text Box for Search
        self.search_box = QLineEdit(self)
        self.search_box.setFixedHeight(30)
        self.search_box.showMaximized()
        self.search_box.setPlaceholderText("Search...")
        self.search_box.returnPressed.connect(self.search)

        # Set up UsnJrnl Table
        self.usnjrnl_table = QTableWidget()
        usnjrnl_table_header = self.usnjrnl_table.verticalHeader()
        usnjrnl_table_header.setDefaultSectionSize(28)
        usnjrnl_table_header.setMaximumSectionSize(28)
        self.usnjrnl_table.setColumnCount(7)
        self.usnjrnl_table.setHorizontalHeaderLabels(self.usnjrnl_table_header_labels)
        self.usnjrnl_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.usnjrnl_table.verticalHeader().setVisible(False)
        self.usnjrnl_table.cellDoubleClicked.connect(self.show_detail)

        # Set up LogFile Table
        self.logfile_table = QTableWidget()
        logfile_table_header = self.logfile_table.verticalHeader()
        logfile_table_header.setDefaultSectionSize(28)
        logfile_table_header.setMaximumSectionSize(28)
        self.logfile_table.setColumnCount(10)
        self.logfile_table.setHorizontalHeaderLabels(self.logfile_table_header_labels)
        self.logfile_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.logfile_table.verticalHeader().setVisible(False)

        # Set up Tab Widget
        self.tab = QTabWidget()
        self.tab.addTab(self.usnjrnl_table, "$UsnJrnl")
        self.tab.addTab(self.logfile_table, "$LogFile")
        self.tab.currentChanged.connect(self.tabChanged)

        self.options_layout.addWidget(self.group_box)
        self.options_layout.addWidget(self.usnjrnl_export_btn, alignment=Qt.AlignBottom)
        self.options_layout.addWidget(self.logfile_export_btn, alignment=Qt.AlignBottom)
        window_layout.addWidget(self.search_box)
        window_layout.addWidget(self.tab)
        self.setLayout(window_layout)

        # Export Progress Bar
        self.usnjrnl_export_bar = QProgressBar(self)
        self.usnjrnl_export_bar.setFixedSize(200, 40)
        self.usnjrnl_export_bar.setAlignment(Qt.AlignCenter)
        self.usnjrnl_export_bar.hide()
        self.logfile_export_bar = QProgressBar(self)
        self.logfile_export_bar.setFixedSize(200, 40)
        self.logfile_export_bar.setAlignment(Qt.AlignCenter)
        self.logfile_export_bar.hide()

    def tabChanged(self, idx):
        if idx:
            self.group_box.setDisabled(True)
        else:
            self.group_box.setDisabled(False)

    def load(self):
        thread_list = []
        try:
            thread_list.append(Thread(target=self.usnjrnl.parse, args=()))
            thread_list.append(Thread(target=self.logfile.parse_all, args=()))

            for t in thread_list:
                t.start()
            for t in thread_list:
                t.join()

            self.logfile.connect_transactions()

            self.usnjrnl_len = len(self.usnjrnl.records)
            self.logfile_len = len(self.logfile.rcrd_records)

            thread_list.clear()
            thread_list.append(Thread(target=self.load_usnjrnlTable, args=()))
            thread_list.append(Thread(target=self.load_logfileTable, args=()))
            for t in thread_list:
                t.start()
            for t in thread_list:
                t.join()
        except Exception as e:
            raise Exception(e)

        self.ntfs_dialog.resume()

    def load_usnjrnlTable(self):
        usn_row = 0
        self.details = []
        for record in self.usnjrnl.records:
            self.usnjrnl_table.insertRow(usn_row)
            detail = []  # [ mft, usn record, logfile transaction ]
            entry = self.mft.entries[record.file_reference_mft_entry]
            detail.append(entry.detail())

            parent_ref_entry_num = record.parent_file_reference_mft_entry
            if parent_ref_entry_num != record.file_reference_mft_entry:
                full_path = (self.mft.getFullPath(parent_ref_entry_num) + "\\" + record.file_name).replace(".\\","C:\\")
            else:
                if entry.is_base_entry:
                    full_path = record.file_name
                else:
                    full_path = "~unknown-ENTRY[{}]\\{}".format(entry.inum, record.file_name)
            self.usnjrnl_table.setItem(usn_row, 0, QTableWidgetItem("{}".format(record.timestamp_datetime)))
            self.usnjrnl_table.setItem(usn_row, 1, QTableWidgetItem(str(record.usn)))
            self.usnjrnl_table.setItem(usn_row, 2, QTableWidgetItem(record.file_name))
            self.usnjrnl_table.setItem(usn_row, 3, QTableWidgetItem(full_path))
            self.usnjrnl_table.setItem(usn_row, 4, QTableWidgetItem(record.reason_string))
            self.usnjrnl_table.setItem(usn_row, 5, QTableWidgetItem(record.file_attributes_string))
            self.usnjrnl_table.setItem(usn_row, 6, QTableWidgetItem("OS" if record.source_info else "User"))

            self.usnjrnl_table.item(usn_row, 0).setTextAlignment(Qt.AlignCenter)
            self.usnjrnl_table.item(usn_row, 1).setTextAlignment(Qt.AlignCenter)
            self.usnjrnl_table.item(usn_row, 5).setTextAlignment(Qt.AlignCenter)
            self.usnjrnl_table.item(usn_row, 6).setTextAlignment(Qt.AlignCenter)

            detail.append([
                str(record.usn),
                record.file_name,
                "{}".format(record.timestamp),
                record.reason_string,
                record.file_attributes_string,
            ])

            if entry.lsn in self.logfile.transactions.keys():
                transaction = self.logfile.transactions[entry.lsn]
                if transaction.contains_usn:
                    for usn in transaction.usns:
                        if usn[1] == record.usn:
                            detail.append([
                                transaction.transaction_num,
                                transaction.all_opcodes,
                            ])
                            for c in range(self.usnjrnl_table.columnCount()):  # Adjust COLOR of Row
                                self.usnjrnl_table.item(usn_row, c).setBackground(QColor(125, 125, 125, 30))

            if self.DELETE_KEYWORD in record.reason_string:
                checked_fname = record.file_name.lower()
                if checked_fname.endswith(".ps") or checked_fname.endswith(".eps"):
                    for c in range(self.usnjrnl_table.columnCount()):
                        self.usnjrnl_table.item(usn_row, c).setBackground(QColor(0, 0, 155, 30))
                elif checked_fname[0] == '~' and checked_fname.endswith(".tmp"):
                    for c in range(self.usnjrnl_table.columnCount()):
                        self.usnjrnl_table.item(usn_row, c).setBackground(QColor(0, 125, 255, 30))

            self.details.append(detail)
            usn_row += 1

        self.usnjrnl_table.setColumnWidth(0, 180)
        self.usnjrnl_table.setColumnWidth(1, 90)
        self.usnjrnl_table.setColumnWidth(2, 200)
        self.usnjrnl_table.setColumnWidth(3, 400)
        self.usnjrnl_table.setColumnWidth(4, 180)
        self.usnjrnl_table.setColumnWidth(5, 100)
        self.usnjrnl_table.horizontalHeader().setStretchLastSection(True)

    def load_logfileTable(self):
        log_row = 0
        for rcrd in self.logfile.rcrd_records:
            prev_redo = 0
            prev_undo = 0
            for (lsn_hdr, lsn_data) in rcrd.lsn_entries:
                self.logfile_table.insertRow(log_row)
                self.logfile_table.setItem(log_row, 0, QTableWidgetItem(str(lsn_hdr.this_lsn)))
                self.logfile_table.setItem(log_row, 1, QTableWidgetItem(str(lsn_hdr.transaction_num)))
                try:
                    entry = self.mft.entries[lsn_data.deriv_inum]
                    attr = entry.attributes[AttributeTypeEnum.FILE_NAME][0]
                    # File Name
                    self.logfile_table.setItem(log_row, 3, QTableWidgetItem(attr.name))
                    # Full Path
                    self.logfile_table.setItem(log_row, 4, QTableWidgetItem(self.mft.getFullPath(entry.inum)))
                    # File Accessed Time
                    self.logfile_table.setItem(log_row, 5, QTableWidgetItem(datetime.datetime.strftime(attr.file_access_time_datetime, "%Y-%m-%d %H:%M:%S.%f")))
                    self.logfile_table.item(log_row, 5).setTextAlignment(Qt.AlignCenter)
                except Exception as e:
                    self.logfile_table.setItem(log_row, 3, QTableWidgetItem(""))
                    self.logfile_table.setItem(log_row, 4, QTableWidgetItem(""))
                    self.logfile_table.setItem(log_row, 5, QTableWidgetItem(""))
                try:
                    attr2 = entry.attributes[AttributeTypeEnum.STANDARD_INFORMATION][0]
                    # MFT Modified Time
                    self.logfile_table.setItem(log_row, 2, QTableWidgetItem(datetime.datetime.strftime(attr2.mft_altered_time_datetime, "%Y-%m-%d %H:%M:%S.%f")))
                    self.logfile_table.item(log_row, 2).setTextAlignment(Qt.AlignCenter)
                except Exception as e:
                    self.logfile_table.setItem(log_row, 2, QTableWidgetItem(""))
                self.logfile_table.setItem(log_row, 6, QTableWidgetItem(lsn_data.deriv_redo_operation_type))
                self.logfile_table.setItem(log_row, 7, QTableWidgetItem(lsn_data.deriv_undo_operation_type))
                self.logfile_table.setItem(log_row, 8, QTableWidgetItem(str(lsn_data.mft_cluster_index)))
                self.logfile_table.setItem(log_row, 9, QTableWidgetItem(str(lsn_data.target_vcn)))
                self.logfile_table.item(log_row, 1).setTextAlignment(Qt.AlignCenter)
                self.logfile_table.item(log_row, 8).setTextAlignment(Qt.AlignCenter)
                self.logfile_table.item(log_row, 9).setTextAlignment(Qt.AlignCenter)
                if lsn_data.redo_operation == 3 and lsn_data.undo_operation == 2:
                    if prev_redo == 15 and prev_undo == 14:
                        for i in range(self.logfile_table.columnCount()):
                            self.logfile_table.item(log_row-1, i).setBackground(QColor(255, 0, 0, 30))
                            self.logfile_table.item(log_row, i).setBackground(QColor(255, 0, 0, 30))
                prev_redo = lsn_data.redo_operation
                prev_undo = lsn_data.undo_operation
                log_row += 1

        self.logfile_table.resizeColumnsToContents()
        self.logfile_table.setColumnWidth(2, 170)
        self.logfile_table.setColumnWidth(3, 200)
        self.logfile_table.setColumnWidth(4, 400)
        self.logfile_table.setColumnWidth(5, 170)
        self.logfile_table.setColumnWidth(6, 200)
        self.logfile_table.setColumnWidth(7, 200)

    def search(self):
        keyword = self.search_box.text()
        if self.tab.currentIndex():
            if not keyword:
                for row in range(self.logfile_table.rowCount()):
                    if self.logfile_table.isRowHidden(row):
                        self.logfile_table.showRow(row)
                return
            items = self.logfile_table.findItems(keyword, Qt.MatchContains)
            included_rows = [self.logfile_table.row(item) for item in items]
            for row in range(self.logfile_table.rowCount()):
                if row in included_rows:
                    self.logfile_table.showRow(row)
                else:
                    self.logfile_table.hideRow(row)
        else:
            if not keyword:
                if self.selected_btn_num == 0 or self.selected_btn_num == 4:
                    for i in range(len(self.details)):
                        if self.usnjrnl_table.isRowHidden(i):
                            self.usnjrnl_table.showRow(i)
                else:
                    checkedKeyword = []
                    if self.create_chk_box.isChecked():
                        checkedKeyword.append(self.CREATE_KEYWORD)
                    if self.delete_chk_box.isChecked():
                        checkedKeyword.append(self.DELETE_KEYWORD)
                    if self.overwrite_chk_box.isChecked():
                        checkedKeyword.append(self.OVERWRITE_KEYWORD)
                    if self.extend_chk_box.isChecked():
                        checkedKeyword.append(self.EXTEND_KEYWORD)
                    for i in range(len(self.details)):
                        if self.details[i][1][3] in checkedKeyword:
                            self.usnjrnl_table.showRow(i)
                return
            items = self.usnjrnl_table.findItems(keyword, Qt.MatchContains)
            included_rows = list(set([self.usnjrnl_table.row(item) for item in items]))
            for row in range(len(self.details)):
                if self.usnjrnl_table.isRowHidden(row):
                    continue
                if row in included_rows:
                    self.usnjrnl_table.showRow(row)
                else:
                    self.usnjrnl_table.hideRow(row)

    def filter(self, b):
        if self.tab.currentIndex():
            return
        keyword = self.filtering_text[b.text()]
        if b.isChecked():
            filter_type = self.ONLY_SHOW if self.selected_btn_num else self.SIMPLE_SHOW
            self.selected_btn_num += 1
        else:
            self.selected_btn_num -= 1
            if self.selected_btn_num:
                filter_type = self.ONLY_HIDE
            else:
                keyword = None
                filter_type = self.SIMPLE_SHOW

        if filter_type == self.ONLY_SHOW:
            for row in range(len(self.details)):
                if keyword in self.details[row][1][3]:
                    self.usnjrnl_table.showRow(row)
        elif filter_type == self.ONLY_HIDE:
            for row in range(len(self.details)):
                if keyword in self.details[row][1][3]:
                    self.usnjrnl_table.hideRow(row)
        elif filter_type == self.SIMPLE_SHOW:
            if not keyword:
                for row in range(len(self.details)):
                    if self.usnjrnl_table.isRowHidden(row):
                        self.usnjrnl_table.showRow(row)
            else:
                for row in range(len(self.details)):
                    if self.usnjrnl_table.isRowHidden(row):
                        continue
                    if keyword in self.details[row][1][3]:
                        self.usnjrnl_table.showRow(row)
                    else:
                        self.usnjrnl_table.hideRow(row)

    def show_detail(self, row, column):
        from modules.UI.NTFSDetailViewer import NTFSDetailViewer
        self.ntfs_detail_viewer = NTFSDetailViewer()
        self.ntfs_detail_viewer.ui(self.details[row])

    def export_usn(self):
        self.usnjrnl_export_btn.hide()
        self.options_layout.replaceWidget(self.usnjrnl_export_btn, self.usnjrnl_export_bar)
        self.usnjrnl_export_bar.show()
        self.usnjrnl_export_thread.start()

    def export_lsn(self):
        self.logfile_export_btn.hide()
        self.options_layout.replaceWidget(self.logfile_export_btn, self.logfile_export_bar)
        self.logfile_export_bar.show()
        self.logfile_export_thread.start()

    def thread_finished(self, msg, path):
        if not self.usnjrnl_export_bar.isHidden():
            self.usnjrnl_export_bar.hide()
            self.options_layout.replaceWidget(self.usnjrnl_export_bar, self.usnjrnl_export_btn)
            self.usnjrnl_export_btn.show()
            self.usnjrnl_export_bar.setValue(0)
        if not self.logfile_export_bar.isHidden():
            self.logfile_export_bar.hide()
            self.options_layout.replaceWidget(self.logfile_export_bar, self.logfile_export_btn)
            self.logfile_export_btn.show()
            self.logfile_export_bar.setValue(0)
        reply = QMessageBox.question(self, "Help", msg, QMessageBox.Open, QMessageBox.Close)
        if reply == QMessageBox.Open:
            import subprocess
            subprocess.call('explorer.exe {}'.format(self.db_dir), shell=True)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setCursor(QCursor(Qt.PointingHandCursor))
        copy_action = QAction("Copy")
        recovery_action = QAction("Recovery")
        menu.addAction(copy_action)
        menu.addAction(recovery_action)
        if self.tab.currentIndex() or not self.is_recovery_allowed:
            recovery_action.setDisabled(True)
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == copy_action:
            table = self.logfile_table if self.tab.currentIndex() else self.usnjrnl_table
            selected = table.selectedItems()
            if len(selected) == 1:
                copied = selected[0].text()
            else:
                copied = " ".join(currentQTableWidgetItem.text() for currentQTableWidgetItem in selected)
            import pyperclip
            pyperclip.copy(copied)
        elif action == recovery_action:
            if self.recovery_thread.is_recovering:
                return
            import os
            dir_name = self.db_dir
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
            carving_item = []
            overlap_inum = []
            for item in self.usnjrnl_table.selectedItems():
                row = item.row()
                inum = int(self.details[item.row()][0][0])
                if self.mft.entries[inum].is_directory:
                    msg = "This entry-#{} is about directory not a file.".format(inum)
                    QMessageBox.information(self, "Help", msg, QMessageBox.Ok)
                    continue
                fname_in_usn = self.usnjrnl_table.item(row, 2).text()
                fname_in_mft = self.details[row][0][-1]
                mft_names = [attr[0] for attr in fname_in_mft]
                if not fname_in_mft:
                    msg = '[{}] MFT Entry is changed, but want to recover? ' \
                          'This entry-#{} has not $FileName Attribute. ' \
                          'So, It will be saved as temporary name like "MFT_Entry_#43212"'.format(fname_in_usn, inum)
                    reply = QMessageBox.question(self, "Help", msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.No:
                        continue
                    output_name = dir_name + "MFT_Entry_#43212"
                elif fname_in_usn not in mft_names:
                    msg = 'MFT Entry is changed, but want to recover? ' \
                          'This entry-#{} has names "{}"\n' \
                          'So, It will be saved as temporary name like "{}"'.format(inum, ', '.join(mft_names), mft_names[0])
                    reply = QMessageBox.question(self, "Help", msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.No:
                        continue
                    output_name = dir_name + mft_names[0]
                else:
                    output_name = dir_name + fname_in_usn
                if inum in overlap_inum:
                    continue
                carving_item.append([fname_in_usn, inum, output_name])
                overlap_inum.append(inum)
            self.recovery_thread.set_target(carving_item)
            self.recovery_thread.start()

class ExportThread(QThread):
    change_value = pyqtSignal(int)
    exported = pyqtSignal(str, str)

    def __init__(self, records, type, db_dir):
        QThread.__init__(self)
        self.records = records
        self.type = type
        self.db_dir = db_dir

    def run(self):
        import csv, datetime
        datetime_str = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S%f")
        msg = ''
        output_file = ''
        self.is_exporting = True
        self.cnt = 0
        self.msleep(500)
        if self.type == NTFSViewer.USNJRNL:
            output_file = "{}usnjrnl_{}.csv".format(self.db_dir, datetime_str)
            msg = "Success! - Export $UsnJrnl as CSV"
            if not self.records:
                return
            first = self.records[0]
            with open(output_file, 'w', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(first.formatted_csv_column_headers())
                for record in self.records:
                    csv_writer.writerow(record.formatted_csv())
                    self.cnt += 1
                    self.change_value.emit(self.cnt)
        elif self.type == NTFSViewer.LOGFILE:
            output_file = "{}logfile_{}.csv".format(self.db_dir, datetime_str)
            msg = "Success! - Export $LogFile as CSV"
            if not self.records:
                return
            first_rcrd = self.records[0]
            header = first_rcrd.formatted_csv_column_headers
            header.extend(first_rcrd.lsn_header_csv_columns)
            header.extend(first_rcrd.lsn_data_csv_columns)
            with open(output_file, 'w', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(header)
                for rcrd in self.records:
                    rcrd.export_csv(csv_writer)
                    self.cnt += 1
                    self.change_value.emit(self.cnt)
        self.exported.emit(msg, output_file)

class RecoveryThread(QThread):
    recoveried = pyqtSignal(str, str)

    def __init__(self, mft):
        QThread.__init__(self)
        self.is_recovering = False
        self.mft = mft

    def set_target(self, recovery_list):
        self.recovery_list = recovery_list

    def run(self):
        self.is_recovering = True
        msg = ''
        fail_cnt = 0
        for item in self.recovery_list:
            rst, output = self.mft.extract_data(inum=item[1], output_file=item[2], stream=0, is_recovering=True)
            if not rst:
                msg += "{} can't be recoveried. cause: {}\n".format(item[0], output)
                fail_cnt += 1
        if not fail_cnt:
            msg = "Success All."
        else:
            msg += "Fail: {}/{}".format(fail_cnt, len(self.recovery_list))
        self.is_recovering = False
        self.recoveried.emit(msg, item[2])