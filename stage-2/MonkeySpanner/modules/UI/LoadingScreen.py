import logging

from PyQt5.QtGui import QMovie, QFont
from PyQt5.QtWidgets import QWidget, QProgressBar, QLabel, QSizePolicy, QBoxLayout
from PyQt5.QtCore import Qt, QThread, QWaitCondition, QMutex, pyqtSignal, QObject

import qdarkstyle

class LoadingBarThread(QThread):
    change_value = pyqtSignal(int)

    def __init__(self, parent, limit):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.is_running = True
        self.limit = limit
        self.parent = parent

    def __del__(self):
        self.wait()

    def run(self):
        self.cnt = 0
        while True:
            self.mutex.lock()

            if not self.is_running:
                self.cond.wait(self.mutex)

            if self.cnt == self.limit:
                self.toggle_status()

            self.cnt += 1
            self.change_value.emit(self.cnt)
            self.msleep(10)

            self.mutex.unlock()

    def toggle_status(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.cond.wakeAll()

class LoadingWidget(QWidget, QObject):
    completed = pyqtSignal()

    def __init__(self, parent, max_cnt):
        QWidget.__init__(self, parent)
        QObject.__init__(self)
        self.setStyleSheet("background-color: #31353a;")
        self.setAutoFillBackground(True)
        self.loading_img_path = "img/loading.gif"

        layout = QBoxLayout(QBoxLayout.TopToBottom, self)
        self.setLayout(layout)

        self.loading_movie = QMovie(self.loading_img_path)
        self.loading_img = QLabel(self)
        self.loading_img.setMovie(self.loading_movie)
        self.loading_img.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.loading_img.setAlignment(Qt.AlignCenter)

        self.log_label = QLabelLogger(self)
        self.log_label.setFormatter(logging.Formatter('%(message)s'))
        logging.getLogger().addHandler(self.log_label)
        logging.getLogger().setLevel(logging.INFO)

        self.loading_bar = QProgressBar(self)
        self.loading_bar.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.loading_bar.setMaximum(max_cnt * 100)
        self.loading_bar.setFixedHeight(10)
        self.loading_bar.setTextVisible(False)

        self.bar_thread = LoadingBarThread(self, 100)
        self.bar_thread.change_value.connect(self.loading_bar.setValue)

        layout.addWidget(self.loading_img)
        layout.addWidget(self.log_label.widget)
        layout.addWidget(self.loading_bar)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def start(self):
        self.loading_movie.start()
        self.bar_thread.start()
        self.show()

    def resume(self):
        self.bar_thread.limit += 100
        if not self.bar_thread.is_running:
            self.bar_thread.toggle_status()
        if self.loading_movie.state() != QMovie.Running:
            self.loading_movie.start()

    # def clear(self):
    #     self.loading_movie.stop()
    #     self.bar_thread.cnt = 0

class QLabelLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QLabel("Analyzing...", parent)
        self.widget.setAlignment(Qt.AlignCenter)
        self.widget.setFont(QFont("Times New Roman", 11))
        self.logs = ''

    def emit(self, msg):
        self.logs += "{}\n".format(msg)
        msg = self.format(msg)
        self.widget.setText(msg)