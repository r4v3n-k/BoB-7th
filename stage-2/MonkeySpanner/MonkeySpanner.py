import os
import sys
import ctypes
import platform

import qdarkstyle
import win32com.shell.shell as shell
from PyQt5.QtWidgets import QApplication, QMessageBox

from MainWindow import Main
from modules.constant import WIN7, WIN10

def uac_require():
    asadmin = 'asadmin'
    try:
        if sys.argv[-1] != asadmin:
            script = os.path.abspath(sys.argv[0])
            params = ''.join([script]+sys.argv[1:]+[asadmin])
            shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
            sys.exit()
        return True, None
    except Exception as e:
        return False, "{}".format(e)

if __name__ == "__main__":
    env = platform.system() + platform.release()
    if env != WIN7 and env != WIN10:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText("Not Supported. {}".format(env))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(sys.exit)
        msg.exec_()
    if ctypes.windll.shell32.IsUserAnAdmin():
        app = QApplication(sys.argv)
        w = Main(env)
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        sys.exit(app.exec_())
    else:
        rst, msg = uac_require()
        if rst:
            app = QApplication(sys.argv)
            w = Main(env)
            app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
            sys.exit(app.exec_())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setText(msg)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.buttonClicked.connect(sys.exit)
            msg.exec_()
