from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread, QWaitCondition, QMutex
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDialog, QBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QFileDialog, \
    QGroupBox, QCheckBox, QHBoxLayout, QSpacerItem

class NTFSLogFileDialog(QDialog, QObject):
    complete = pyqtSignal()

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        QObject.__init__(self)
        self.selected_partition = -1
        self.ui()

    def ui(self):
        self.setWindowTitle("Import File System Log File")
        self.setFixedSize(self.sizeHint())
        self.layout = QBoxLayout(QBoxLayout.TopToBottom, self)
        spacer_item1 = QSpacerItem(10, 5)
        self.layout.addItem(spacer_item1)
        self.setLayout(self.layout)

        # First Group
        self.disk_raw_chk_box = QCheckBox("In this case, it's possible to carve some files.", self)
        self.disk_raw_chk_box.stateChanged.connect(lambda: self.select_type(self.disk_raw_chk_box))
        self.disk_raw_group_box = QGroupBox(self)
        self.disk_raw_group_box.setStyleSheet("margin-top: 0;")
        self.disk_raw_group_box.setDisabled(True)
        disk_raw_group_box_layout = QHBoxLayout(self.disk_raw_group_box)
        self.disk_raw_group_box.setLayout(disk_raw_group_box_layout)

        self.disk_raw_label = QLabel("Disk Raw: ", self)
        self.disk_raw_text_box = QLineEdit()
        self.disk_raw_text_box.setReadOnly(True)
        self.disk_raw_text_box.setFixedWidth(400)

        self.browse_disk_raw_btn = QPushButton("...", self)
        self.browse_disk_raw_btn.setFixedWidth(50)
        self.browse_disk_raw_btn.clicked.connect(self.btn_clicekd)
        self.browse_disk_raw_btn.setCursor(QCursor(Qt.PointingHandCursor))

        disk_raw_group_box_layout.addWidget(self.disk_raw_label)
        disk_raw_group_box_layout.addWidget(self.disk_raw_text_box)
        disk_raw_group_box_layout.addWidget(self.browse_disk_raw_btn)

        self.layout.addWidget(self.disk_raw_chk_box)
        self.layout.addWidget(self.disk_raw_group_box)

        # Second Group
        self.ntfs_log_file_chk_box = QCheckBox("In this case, NTFS Log analysis only supported.", self)
        self.ntfs_log_file_chk_box.stateChanged.connect(lambda: self.select_type(self.ntfs_log_file_chk_box))

        self.ntfs_log_group_box = QGroupBox(self)
        self.ntfs_log_group_box.setStyleSheet("margin-top: 0;")
        self.ntfs_log_group_box.setDisabled(True)
        ntfs_log_group_box_layout = QGridLayout(self)
        self.ntfs_log_group_box.setLayout(ntfs_log_group_box_layout)

        self.mft_label = QLabel("$MFT: ", self)
        self.mft_path_text_box = QLineEdit(self)
        self.mft_path_text_box.setReadOnly(True)
        self.mft_path_text_box.setFixedWidth(400)
        self.browse_mft_btn = QPushButton("...", self)
        self.browse_mft_btn.setFixedWidth(50)
        self.browse_mft_btn.clicked.connect(self.btn_clicekd)
        self.browse_mft_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.usnjrnl_label = QLabel("$UsnJrnl: ", self)
        self.usnjrnl_path_text_box = QLineEdit(self)
        self.usnjrnl_path_text_box.setReadOnly(True)
        self.usnjrnl_path_text_box.setFixedWidth(400)
        self.browse_usnjrnl_btn = QPushButton("...", self)
        self.browse_usnjrnl_btn.setFixedWidth(50)
        self.browse_usnjrnl_btn .clicked.connect(self.btn_clicekd)
        self.browse_usnjrnl_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.logfile_label = QLabel("$LogFile: ", self)
        self.logfile_path_text_box = QLineEdit(self)
        self.logfile_path_text_box.setReadOnly(True)
        self.logfile_path_text_box.setFixedWidth(400)
        self.browse_logfile_btn = QPushButton("...", self)
        self.browse_logfile_btn.setFixedWidth(50)
        self.browse_logfile_btn.clicked.connect(self.btn_clicekd)
        self.browse_logfile_btn.setCursor(QCursor(Qt.PointingHandCursor))

        ntfs_log_group_box_layout.addWidget(self.mft_label, 0, 0)
        ntfs_log_group_box_layout.addWidget(self.mft_path_text_box, 0, 1)
        ntfs_log_group_box_layout.addWidget(self.browse_mft_btn, 0, 2)
        ntfs_log_group_box_layout.addWidget(self.usnjrnl_label, 1, 0)
        ntfs_log_group_box_layout.addWidget(self.usnjrnl_path_text_box, 1, 1)
        ntfs_log_group_box_layout.addWidget(self.browse_usnjrnl_btn, 1, 2)
        ntfs_log_group_box_layout.addWidget(self.logfile_label, 2, 0)
        ntfs_log_group_box_layout.addWidget(self.logfile_path_text_box, 2, 1)
        ntfs_log_group_box_layout.addWidget(self.browse_logfile_btn, 2, 2)

        self.submit_btn = QPushButton("Submit", self)
        self.submit_btn.setFixedSize(100, 40)
        self.submit_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.logging_label = QLabel("Loading...", self)
        self.logging_label.setFixedHeight(20)
        self.logging_label.setAlignment(Qt.AlignCenter)
        self.logging_label.hide()

        self.loading_bar = QProgressBar(self)
        self.loading_bar.setFixedHeight(10)
        self.loading_bar.setTextVisible(False)
        self.loading_bar.hide()

        self.bar_thread = LoadingBarThread(self)
        self.bar_thread.change_value.connect(self.loading_bar.setValue)

        self.spacer_item2 = QSpacerItem(10, 15)
        self.spacer_item3 = QSpacerItem(10, 20)
        self.layout.addItem(self.spacer_item2)
        self.layout.addWidget(self.ntfs_log_file_chk_box)
        self.layout.addWidget(self.ntfs_log_group_box)
        self.layout.addItem(self.spacer_item3)
        self.layout.addWidget(self.submit_btn, alignment=Qt.AlignHCenter)

        # self.setWindowModality(Qt.WindowModal)
        self.setWindowFlag(Qt.WindowCloseButtonHint | Qt.WindowModal)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def select_type(self, b):
        if b is self.disk_raw_chk_box:
            if b.isChecked():
                self.ntfs_log_file_chk_box.setChecked(False)
                self.ntfs_log_group_box.setDisabled(True)
                self.disk_raw_group_box.setDisabled(False)
            else:
                self.disk_raw_group_box.setDisabled(True)
        else:
            if b.isChecked():
                self.disk_raw_chk_box.setChecked(False)
                self.disk_raw_group_box.setDisabled(True)
                self.ntfs_log_group_box.setDisabled(False)
            else:
                self.ntfs_log_group_box.setDisabled(True)

    def btn_clicekd(self):
        sender = self.sender()
        fileName = QFileDialog.getOpenFileName(self)
        if sender is self.browse_disk_raw_btn:
            self.disk_raw_text_box.setText(fileName[0])
        elif sender is self.browse_mft_btn:
            self.mft_path_text_box.setText(fileName[0])
        elif sender is self.browse_usnjrnl_btn:
            self.usnjrnl_path_text_box.setText(fileName[0])
        elif sender is self.browse_logfile_btn:
            self.logfile_path_text_box.setText(fileName[0])

    def ready(self):
        self.submit_btn.hide()
        self.layout.removeWidget(self.submit_btn)
        self.layout.addWidget(self.logging_label, alignment=Qt.AlignBottom | Qt.AlignHCenter)
        self.layout.addWidget(self.loading_bar)
        self.logging_label.show()
        self.loading_bar.show()
        self.bar_thread.start()

    def resume(self):
        if self.bar_thread.cnt < 50:
            self.bar_thread.cnt = 100
            return
        self.bar_thread.toggle_status()

    def change_interface(self, contents):
        from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
        self.layout.removeWidget(self.disk_raw_chk_box)
        self.disk_raw_chk_box.hide()
        self.layout.removeWidget(self.disk_raw_group_box)
        self.disk_raw_group_box.hide()
        self.layout.removeItem(self.spacer_item2)
        self.layout.removeWidget(self.ntfs_log_file_chk_box)
        self.ntfs_log_file_chk_box.hide()
        self.layout.removeWidget(self.ntfs_log_group_box)
        self.ntfs_log_group_box.hide()
        self.layout.removeItem(self.spacer_item3)
        self.layout.removeWidget(self.submit_btn)

        self.disk_name_label = QLabel("Image Name:\t" + contents[0][0], self)
        self.disk_size_label = QLabel("Image Size:\t{} Bytes".format(contents[0][1]), self)
        self.disk_size_label.setFixedHeight(20)
        self.disk_size_label.setAlignment(Qt.AlignVCenter)
        self.disk_part_label = QLabel("Partition:", self)
        self.disk_part_label.setFixedHeight(20)
        self.disk_part_label.setAlignment(Qt.AlignBottom)

        self.partition_tree = QTreeWidget(self)
        self.partition_tree.setHeaderLabels(["Order", "File System", "Active", "Starting Offset", "Total Sector", "Size"])
        self.partition_tree.item_changed.connect(self.item_changed)
        self.partition_tree.resizeColumnToContents(2)
        self.partition_tree.resizeColumnToContents(3)
        self.partition_tree.resizeColumnToContents(4)
        self.partition_tree.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.partition_tree.headerItem().setTextAlignment(1, Qt.AlignCenter)

        self.partition_items = []
        for row in range(1, 5):
            self.partition_tree.headerItem().setTextAlignment(row + 1, Qt.AlignCenter)
            item = QTreeWidgetItem(self.partition_tree)
            item.setText(0, str(row))
            item.setTextAlignment(0, Qt.AlignLeft)
            if not contents[row]:
                item.setText(1, "None")
                item.setCheckState(0, Qt.Unchecked)
                item.setDisabled(True)
                continue
            for col in range(5):
                item.setText(col + 1, contents[row][col])
                item.setTextAlignment(col + 1, Qt.AlignCenter)
            item.setTextAlignment(1, Qt.AlignLeft)
            item.setCheckState(0, Qt.Unchecked)
            self.partition_items.append(item)

        self.layout.addWidget(self.disk_name_label)
        self.layout.addWidget(self.disk_size_label)
        self.layout.addWidget(self.disk_part_label)
        self.layout.addWidget(self.partition_tree)
        self.layout.addItem(QSpacerItem(10, 10))
        self.layout.addWidget(self.submit_btn, alignment=Qt.AlignCenter)

    def item_changed(self, changed_item, p_int):
        if changed_item.checkState(0) == Qt.Checked:
            self.selected_partition = int(changed_item.text(0))
            for item in self.partition_items:
                if item is not changed_item:
                    item.setCheckState(0, Qt.Unchecked)


class LoadingBarThread(QThread):
    change_value = pyqtSignal(int)
    completed = pyqtSignal()

    def __init__(self, parent):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.isRunning = True
        self.parent = parent

    def __del__(self):
        self.wait()

    def run(self):
        self.cnt = 0
        while True:
            self.mutex.lock()

            if not self.isRunning:
                self.cond.wait(self.mutex)

            if self.cnt == 50:
                self.toggle_status()

            if self.cnt == 100:
                self.completed.emit()
                break

            self.cnt += 1
            self.change_value.emit(self.cnt)
            self.msleep(10)

            self.mutex.unlock()

    def toggle_status(self):
        self.isRunning = not self.isRunning
        if self.isRunning:
            self.cond.wakeAll()
