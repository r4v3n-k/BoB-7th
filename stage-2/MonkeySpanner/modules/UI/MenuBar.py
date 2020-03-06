from PyQt5.QtWidgets import *
from modules.ArtifactAnalyzer import getRecentFileCache, JumpListAnalyzerThreadForViewer

class MenuBar(QMenuBar):

    def __init__(self, parent):
        QMenuBar.__init__(self, parent)
        self.menu = ["&File", "&View", "&Window", "&Help"]
        self.action = [
            ["Import Directory", "Import CSV", "Export as CSV", "Import XML", "Export ALL as XML", "Export as XML", "Exit"],
            ["\"Home\" Tab", "show NTFS Log", "show JumpList", "show RecentFileCache.bcf", "show Amcache.hve"], # "show Registry"
            ["Environment", "About"]
        ]
        self.ui()

    def ui(self):
        file_menu = self.addMenu(self.menu[0])
        view_menu = self.addMenu(self.menu[1])
        help_menu = self.addMenu(self.menu[-1])

        # File
        import_dir_menu = QAction(self.action[0][0], self)
        import_dir_menu.setShortcut("Ctrl+O")
        import_dir_menu.triggered.connect(self.parent().import_dir)
        file_menu.addAction(import_dir_menu)
        file_menu.addSeparator()

        import_csv_menu = QAction(self.action[0][1], self)
        import_csv_menu.setShortcut("C")
        import_csv_menu.triggered.connect(self.parent().import_csv)
        file_menu.addAction(import_csv_menu)

        export_csv_menu = QAction(self.action[0][2], self)
        export_csv_menu.setShortcut("E")
        export_csv_menu.triggered.connect(self.parent().export_as_csv)
        file_menu.addAction(export_csv_menu)
        file_menu.addSeparator()

        import_xml_menu = QAction(self.action[0][3], self)
        import_xml_menu.setShortcut("Ctrl+X")
        import_xml_menu.triggered.connect(self.parent().import_xml)
        file_menu.addAction(import_xml_menu)

        export_all_xml_menu = QAction(self.action[0][4], self)
        export_all_xml_menu.setShortcut("Alt+E")
        export_all_xml_menu.triggered.connect(self.parent().export_all_as_xml)
        file_menu.addAction(export_all_xml_menu)

        export_xml_menu = QAction(self.action[0][5], self)
        export_xml_menu.setShortcut("Alt+X")
        export_xml_menu.triggered.connect(self.parent().export_as_xml)
        file_menu.addAction(export_xml_menu)
        file_menu.addSeparator()

        exit_menu = QAction(self.action[0][-1], self)
        exit_menu.setShortcut("Q")
        exit_menu.triggered.connect(qApp.quit)
        file_menu.addAction(exit_menu)

        # View
        home_tab_menu = QAction(self.action[1][0], self)
        home_tab_menu.triggered.connect(self.parent().show_home_tab)
        view_menu.addAction(home_tab_menu)
        view_menu.addSeparator()

        ntfs_menu = QAction(self.action[1][1], self)
        ntfs_menu.triggered.connect(self.show_ntfs_viewer)
        view_menu.addAction(ntfs_menu)

        jumplist_menu = QAction(self.action[1][2], self)
        jumplist_menu.triggered.connect(self.show_jumplist_viewer)
        view_menu.addAction(jumplist_menu)

        recentfilebcf_menu = QAction(self.action[1][3], self)
        recentfilebcf_menu.triggered.connect(self.show_recentfilecache_viewer)
        view_menu.addAction(recentfilebcf_menu)

        amcache_menu = QAction(self.action[1][4], self)
        amcache_menu.triggered.connect(self.show_amcache_viewer)
        view_menu.addAction(amcache_menu)

        # Help
        env_action = QAction(self.action[-1][0], self)
        env_action.triggered.connect(self.show_user_env_viewer)
        help_menu.addAction(env_action)

        about_action = QAction(self.action[-1][1], self)
        about_action.triggered.connect(self.show_about_viewer)
        help_menu.addAction(about_action)

        self.jumplist_analyzer_thread = JumpListAnalyzerThreadForViewer()
        self.jumplist_analyzer_thread.completed.connect(self.on_completed_jumplist_thread)
        self.jumplist_analyzer_thread.performanced.connect(self.on_performanced_jumplist_thread)

    def show_ntfs_viewer(self):
        from modules.UI.NTFSViewer import NTFSViewer
        self.env = self.parent().env
        self.parent().ntfsViewer = NTFSViewer(self.env)

    def show_jumplist_viewer(self):
        self.env = self.parent().env
        if len(self.env) == 2:
            QMessageBox.information(
                self, "Help",
                "First, you need to perform analysis on the active system or import the directory.",
                QMessageBox.Ok
            )
            return
        elif not self.env[4][3]:
            QMessageBox.information(self, "Help", "The file does not exist.", QMessageBox.Ok)
            return
        self.contents = []
        self.jumplist_analyzer_thread.set_target(self.env, self.contents)
        self.jumplist_analyzer_thread.start()

    def on_performanced_jumplist_thread(self, str):
        self.parent().statusBar().showMessage(str)

    def on_completed_jumplist_thread(self, str):
        QMessageBox.information(self, "Help", str, QMessageBox.Ok)
        if str.startswith("C"):
            from modules.UI.JumpListViewer import JumpListViewer
            self.parent().jumplist_viewer = JumpListViewer(self.contents, self.env)

    def show_recentfilecache_viewer(self):
        from modules.UI.ListViewer import ListViewer
        file_name, _ = QFileDialog.getOpenFileName(self, filter="*.bcf")
        if not file_name and not _: return
        rst, contents = getRecentFileCache(file_name)
        if rst:
            self.parent().list_viewer = ListViewer("RecentFileCache Viewer", contents)
        else:
            QMessageBox.information(self, "Help", contents, QMessageBox.Ok)

    def show_amcache_viewer(self):
        self.env = self.parent().env
        from modules.UI.AmcacheViewer import AmcacheViewer
        from libs.ParseRegistry.Amcache import get
        file_name, _ = QFileDialog.getOpenFileName(self, filter="*.hve")
        if not file_name and not _: return
        rst, contents = get(file_name)
        if rst:
            self.parent().amcache_viewer = AmcacheViewer("Amcache.hve Viewer", contents, self.env)
        else:
            QMessageBox.information(self, "Help", contents, QMessageBox.Ok)

    def show_user_env_viewer(self):
        from modules.UI.EnvironmentWidget import EnvironmentWidget
        self.env_widget = EnvironmentWidget()

    def show_about_viewer(self):
        from modules.UI.AboutWidget import AboutWidget
        self.about_widget = AboutWidget()
