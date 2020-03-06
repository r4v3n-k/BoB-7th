from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

class EnvironmentWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui()

    def ui(self):
        import platform
        self.setWindowTitle("Environment")
        layout = QVBoxLayout(self)

        env_label = QLabel("Environment", self)
        env_label.setFixedHeight(15)
        env_label.setAlignment(Qt.AlignBottom)

        env_table = QTableWidget(self)
        env_table.setFixedSize(400, 95)
        env_table.setColumnCount(2)
        env_table.setRowCount(3)
        env_table.verticalHeader().setVisible(False)
        env_table.horizontalHeader().setVisible(False)
        env_table.setItem(0, 0, QTableWidgetItem("OS"))
        env_table.setItem(0, 1, QTableWidgetItem("{} {} {}".format(
            platform.system(), platform.release(), platform.architecture()[0])
        ))
        env_table.setItem(1, 0, QTableWidgetItem("Version"))
        env_table.setItem(1, 1, QTableWidgetItem(platform.version()))
        env_table.setItem(2, 0, QTableWidgetItem("Processor"))
        env_table.setItem(2, 1, QTableWidgetItem(platform.processor()))
        env_table.horizontalHeader().setStretchLastSection(True)
        env_table.verticalHeader().setStretchLastSection(True)

        layout.addWidget(env_label)
        layout.addWidget(env_table)

        rst, self.contents = self.get_basic_reg_settings()
        if not rst:
            QMessageBox.critical(self, "Error", self.contents, QMessageBox.Ok)
        else:
            reg_label = QLabel("Registry Settings", self)
            reg_label.setFixedHeight(20)
            reg_label.setAlignment(Qt.AlignBottom)

            reg_table = QTableWidget(self)
            reg_table.setFixedHeight(95)
            reg_table.setColumnCount(2)
            reg_table.setRowCount(3)
            reg_table.verticalHeader().setVisible(False)
            reg_table.horizontalHeader().setVisible(False)
            for row in range(len(self.contents)-1):
                reg_table.setItem(row, 0, QTableWidgetItem(self.contents[row][0]))
                reg_table.setItem(row, 1, QTableWidgetItem(self.contents[row][1]))
            reg_table.resizeColumnsToContents()
            reg_table.verticalHeader().setStretchLastSection(True)
            reg_table.horizontalHeader().setStretchLastSection(True)

            reg_label2 = QLabel("- Application Compaitibility Settings", self)
            reg_label2.setFixedHeight(20)
            reg_label2.setAlignment(Qt.AlignBottom)
            if len(self.contents[-1]) == 1:
                reg_table2 = QLabel(self.contents[-1][0], self)
                reg_table2.setFixedHeight(40)
                reg_table2.setAlignment(Qt.AlignCenter)
            else:
                reg_table2 = QTableWidget(self)
                reg_table2.setFixedHeight(125)
                reg_table2.setColumnCount(2)
                reg_table2.setRowCount(4)
                row = 0
                for item in self.contents[-1]:
                    reg_table2.setItem(row, 0, QTableWidgetItem(item[0]))
                    reg_table2.setItem(row, 1, QTableWidgetItem(item[1]))
                    row += 1
                reg_table2.resizeColumnsToContents()
                reg_table2.verticalHeader().setVisible(False)
                reg_table2.horizontalHeader().setVisible(False)
                reg_table2.verticalHeader().setStretchLastSection(True)
                reg_table2.horizontalHeader().setStretchLastSection(True)
            layout.addWidget(reg_label)
            layout.addWidget(reg_table)
            layout.addWidget(reg_label2)
            layout.addWidget(reg_table2)
        self.show()

    def get_basic_reg_settings(self):
        contents = []
        try:
            import winreg as reg
        except ImportError as e:
            return False, "{}".format(e)

        hReg = reg.ConnectRegistry(None, reg.HKEY_LOCAL_MACHINE)

        # Event Log
        try:
            evtx_reg = reg.OpenKey(hReg, r'SYSTEM\\CurrentControlSet\\Services\\EventLog')
            bin_data = reg.QueryValueEx(evtx_reg, 'Start')[0]
            if bin_data == 1:
                val = "Auto(Delayed Start)"
            elif bin_data == 2:
                val = "Auto"
            elif bin_data == 3:
                val = "Menual"
            elif bin_data == 4:
                val = "Disabled"
        except EnvironmentError:
            val = "Not Set"
        contents.append(["Event Log Start", val])

        # Prefetch
        try:
            prefetch_reg = reg.OpenKey(hReg,
                                      r'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters')
            bin_data = reg.QueryValueEx(prefetch_reg, 'EnablePrefetcher')[0]
            if bin_data == 0:
                val = "Disabled"
            elif bin_data == 1:
                val = "Used to run applications"
            elif bin_data == 2:
                val = "Use for boot area only"
            elif bin_data == 3:
                val = "Use for application/Boot execution"
        except EnvironmentError:
            val = "Not Set"
        contents.append(["Enable Prefetcher", val])

        # Recent Doc History
        try:
            recent_reg = reg.OpenKey(hReg, r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer')
            bin_data = reg.QueryValueEx(recent_reg, 'NoRecentDocsHistory')[0]
            if not bin_data:
                val = "Enabled"
            else:
                val = "Disabled"
        except EnvironmentError:
            val = "Not set"
        contents.append(["RecentDocsHistory  ", val])

        # AppCompat
        try:
            compat_reg = reg.OpenKey(hReg, r'SOFTWARE\\Policies\\Microsoft\\Windows\\AppCompat')
        except EnvironmentError:
            print()
            contents.append(["Not Set"])
            return True, contents

        app_compat_contents = [
            ["SwitchBack Compatibility Engine", "Off"],
            ["Application Compatibility Engine", "Off"],
            ["Program Compatibility Assistant", "Off"],
            ["Detect compatibility issues for applications and drivers", "On"],
        ]
        try:
            bin_data = reg.QueryValueEx(compat_reg, 'SbEnable')[0]
            if not bin_data:
                app_compat_contents[0][1] = "On"
        except Exception:
            app_compat_contents[0][1] = "Not set"

        try:
            bin_data = reg.QueryValueEx(compat_reg, 'DisableEngine')[0]
            if not bin_data:
                app_compat_contents[1][1] = "On"
        except Exception:
            app_compat_contents[1][1] = "Not Set"

        try:
            bin_data = reg.QueryValueEx(compat_reg, 'DisablePCA')[0]
            if not bin_data:
                app_compat_contents[2][1] = "On"
        except Exception:
            app_compat_contents[2][1] = "Not set"

        try:
            bin_data = reg.QueryValueEx(compat_reg, 'DisablePcaUI')[0]
            if not bin_data:
                app_compat_contents[3][1] = "Off"
        except Exception:
            app_compat_contents[3][1] = "Not set"
        contents.append(app_compat_contents)

        return True, contents
