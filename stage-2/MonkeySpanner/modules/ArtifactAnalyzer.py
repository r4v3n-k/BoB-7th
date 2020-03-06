import os
import datetime
import logging

from PyQt5.QtCore import QThread, pyqtSignal
import modules.constant as CONSTANT

class AppEvtxAnalyzerThread(QThread):
    completed = pyqtSignal()

    def __init__(self, env, artifacts_list, timeline=None):
        QThread.__init__(self)
        self.env = env
        self.artifacts_list = artifacts_list
        self.timeline = timeline

    def run(self):
        evtx_name = 'Application.evtx'
        if self.env[1]:
            if not os.path.exists(self.env[4][1]):
                return
            full_path = self.env[4][1] + evtx_name
        else:
            full_path = CONSTANT.EVENTLOG + evtx_name
            copy(full_path, self.env[4][1], 'Not copied "{}"'.format(evtx_name))

        items = []
        wer_list = []
        checked_sw = [
            "ACRORD32.EXE",
            '',
            ["MICROSOFTEDGE.EXE", "MICROSOFTEDGEBCHOST.EXE", "MICROSOFTEDGECP.EXE"],
            ["HWP.EXE", "GBB.EXE", "GSWIN32C.EXE"],
            "IEXPLORE.EXE",
            ["WINWORD.EXE", "POWERPNT.EXE", "EXCEL.EXE", "WMIPRVSE.EXE", "EQNEDT32.EXE", "DW20.EXE", "DWWIN.EXE", "FLTLDR.EXE"],
        ]
        color_number = [(3, 5), (0, 0), (2, 4), (5, 5), (2, 4), (5, 5)]

        checked = {
            '1000': 'Application Error',
            '1001': 'Windows Error Reporting',
        }

        import libs.ParseEvtx.Evtx as evtx
        with evtx.Evtx(full_path) as log:
            for event in log.records():
                try:
                    system_tag = event.lxml()[0]
                    logged_time = system_tag[5].get("SystemTime")
                    provider_name = system_tag[0].get("Name")
                    event_id = system_tag[1].text
                    if not logged_time: continue
                    checked_id = list(checked.keys())
                    if event_id in checked_id and provider_name == checked[event_id]:
                        # if self.timeline:
                        #     if datetime.datetime.strptime(logged_time, "%Y-%m-%d %H:%M:%S.%f") < self.timeline:
                        #         logging.info("[Exception] EID - {}, {} was skipped, it's more older timeline".format(event_id, provider_name))
                        #         continue

                        if system_tag[2].text == '4':
                            level = 'Information'
                        elif system_tag[2].text == '3':
                            level = 'Warning'
                        elif system_tag[2].text == '2':
                            level = 'Error'
                        elif system_tag[2].text == '1':
                            level = 'Fatal'

                        if event_id == checked_id[0]:
                            data_tag = event.lxml()[1]
                            etc = data_tag[0].text  # idx - 0 (SW), 3 (Module), 6 (Exception Code)
                            swNum = 0
                            for sw in checked_sw:
                                if etc.upper() in sw:
                                    swNum = checked_sw.index(sw) + 1
                                    colorNum = color_number[swNum-1][0]
                                    break
                            if not swNum: continue
                            items.append([
                                [CONSTANT.EVENTLOG_KEYWORD, False, swNum, colorNum],
                                logged_time, provider_name, event_id, level, etc, event.xml()
                            ])
                        elif event_id == checked_id[1]:
                            data_tag = event.lxml()[1]
                            etc = data_tag[5].text  # idx - 5 (SW), 8 (Module), 11 (Exception Code), 16 (PATH)
                            swNum = 0
                            for sw in checked_sw:
                                if etc.upper() in sw:
                                    swNum = checked_sw.index(sw) + 1
                                    colorNum = color_number[swNum-1][1]
                                    break
                            if not swNum: continue
                            if data_tag[16].text:
                                wer_list.append([data_tag[16].text, data_tag[8].text, data_tag[11].text, swNum])
                            items.append([
                                [CONSTANT.EVENTLOG_KEYWORD, False, swNum, colorNum],
                                logged_time, provider_name, event_id, level, etc, event.xml()])
                except Exception as e:
                    if event_id in checked_id:
                        logging.info('[Error] EID - {} in "{}": {}'.format(event_id, evtx_name, e))
        if wer_list:
            self.getReportWER(wer_list)
        self.artifacts_list += items
        self.completed.emit()

    def getReportWER(self, wer_list):
        dbDir = self.env[4][2]
        if not os.path.exists(dbDir):
            return
        items = []
        if self.env[1]:
            for data in wer_list:
                full_path = dbDir + "{}\\Report.wer".format(data[0].rsplit('\\', 1)[-1])
                if os.path.exists(full_path):
                    colorNum = 0
                    if data[-1] in [CONSTANT.ADOBE_READER, CONSTANT.EDGE]:
                        colorNum = 6
                    elif data[-1] in [CONSTANT.HWP, CONSTANT.OFFICE, CONSTANT.IE]:
                        colorNum = 5
                    created_time = "{}".format(datetime.datetime.fromtimestamp(os.path.getctime(full_path)))
                    modifiedTime = "{}".format(datetime.datetime.fromtimestamp(os.path.getmtime(full_path)))
                    with open(full_path, "rb") as f:
                        content = f.read().decode('utf-16')
                    items.append([
                        [CONSTANT.WER_KEYWORD, False, data[-1], colorNum],
                        modifiedTime, full_path, data[1], data[2], created_time, content
                    ])
        else:
            for data in wer_list:
                if os.path.exists(data[0]):
                    colorNum = 0
                    if data[-1] in [CONSTANT.ADOBE_READER, CONSTANT.EDGE]:
                        colorNum = 6
                    elif data[-1] in [CONSTANT.HWP, CONSTANT.OFFICE, CONSTANT.IE]:
                        colorNum = 5
                    full_path = data[0] + "\\Report.wer"
                    dirName = data[0].rsplit("\\", 1)[-1]
                    os.mkdir(dbDir + dirName)
                    copy(full_path, dbDir + '{}\\'.format(dirName), 'Not copied "{}"'.format(full_path))

                    created_time = "{}".format(datetime.datetime.fromtimestamp(os.path.getctime(full_path)))
                    modifiedTime = "{}".format(datetime.datetime.fromtimestamp(os.path.getmtime(full_path)))
                    with open(full_path, "rb") as f:
                        content = f.read().decode('utf-16')
                    items.append([
                        [CONSTANT.WER_KEYWORD, False, data[-1], colorNum],
                        modifiedTime, full_path, data[1], data[2], created_time, content
                    ])
        self.artifacts_list += items

class WERDiagEvtxAnalyzerThread(QThread):
    completed = pyqtSignal()

    def __init__(self, env, artifacts_list, timeline=None):
        QThread.__init__(self)
        self.env = env
        self.artifacts_list = artifacts_list
        self.timeline = timeline

    def run(self):
        evtx_name = 'Microsoft-Windows-WER-Diag%4Operational.evtx'
        if self.env[1]:
            if not os.path.exists(self.env[4][1]):
                return
            full_path = self.env[4][1] + evtx_name
        else:
            full_path = CONSTANT.EVENTLOG + evtx_name
            copy(full_path, self.env[4][1], 'Not copied "{}"'.format(evtx_name))

        import libs.ParseEvtx.Evtx as evtx
        items = []
        head = [CONSTANT.EVENTLOG_KEYWORD, True, 3, 0, 0, 4, 3, 4]
        checked_id = [2]
        checkedProviders = {
            '2': 'Microsoft-Windows-WER-Diag'
        }
        with evtx.Evtx(full_path) as log:
            for event in log.records():
                try:
                    system_tag = event.lxml()[0]
                    logged_time = system_tag[7].get("SystemTime")
                    provider_name = system_tag[0].get("Name")
                    event_id = system_tag[1].text
                    if not logged_time: continue
                    if int(event_id) in checked_id and provider_name == checkedProviders[event_id]:
                        # if self.timeline:
                        #     if datetime.datetime.strptime(logged_time, "%Y-%m-%d %H:%M:%S.%f") < self.timeline:
                        #         logging.info("[Exception] EID - {}, {} was skipped, it's more older timeline".format(event_id, provider_name))
                        #         continue
                        if system_tag[3].text == '1':
                            level = 'Fatal'
                        elif system_tag[3].text == '2':
                            level = 'Error'
                        elif system_tag[3].text == '3':
                            level = 'Warning'
                        elif system_tag[3].text == '4':
                            level = 'Information'
                        etc = 'Heap Corruption'
                        items.append([head, logged_time, provider_name, event_id, level, etc, event.xml()])
                except Exception as e:
                    if int(event_id) in checked_id:
                        logging.info('[Error] EID - {} in "{}": {}'.format(event_id, evtx_name, e))
        self.artifacts_list += items
        self.completed.emit()

class FaultHeapEvtxAnalyzerThread(QThread):
    completed = pyqtSignal()

    def __init__(self, env, artifacts_list, timeline=None):
        QThread.__init__(self)
        self.env = env
        self.artifacts_list = artifacts_list
        self.timeline = timeline

    def run(self):
        evtx_name = 'Microsoft-Windows-Fault-Tolerant-Heap%4Operational.evtx'
        if self.env[1]:
            if not os.path.exists(self.env[4][1]):
                return
            full_path = self.env[4][1] + evtx_name
        else:
            full_path = CONSTANT.EVENTLOG + evtx_name
            copy(full_path, self.env[4][1], 'Not copied "{}"'.format(evtx_name))

        items = []
        head = [CONSTANT.EVENTLOG_KEYWORD, True, 5, 0, 0, 4, 4, 4]
        checked_id = [1001]
        checkedProviders = {
            '1001': 'Microsoft-Windows-Fault-Tolerant-Heap',
        }
        import libs.ParseEvtx.Evtx as evtx
        with evtx.Evtx(full_path) as log:
            for event in log.records():
                try:
                    system_tag = event.lxml()[0]
                    logged_time = system_tag[7].get("SystemTime")
                    provider_name = system_tag[0].get("Name")
                    event_id = system_tag[1].text
                    if not logged_time: continue
                    if int(event_id) in checked_id and provider_name == checkedProviders[event_id]:
                        # if self.timeline:
                        #     if datetime.datetime.strptime(logged_time, "%Y-%m-%d %H:%M:%S.%f") < self.timeline:
                        #         logging.info("[Exception] EID - {}, {} was skipped, it's more older timeline".format(event_id, provider_name))
                        #         continue
                        if system_tag[3].text == '1':
                            level = 'Fatal'
                        elif system_tag[3].text == '2':
                            level = 'Error'
                        elif system_tag[3].text == '3':
                            level = 'Warning'
                        elif system_tag[3].text == '4':
                            level = 'Information'
                        data_tag = event.lxml()[1]
                        etc = data_tag.get("Name")
                        items.append([head, logged_time, provider_name, event_id, level, etc, event.xml()])
                except Exception as e:
                    if int(event_id) in checked_id:
                        logging.info('[Error] EID - {} in "{}": {}'.format(event_id, evtx_name, e))
        self.artifacts_list += items
        self.completed.emit()

class OAlertsEvtxAnalyzerThread(QThread):
    completed = pyqtSignal()

    def __init__(self, env, artifacts_list, timeline=None):
        QThread.__init__(self)
        self.env = env
        self.artifacts_list = artifacts_list
        self.timeline = timeline

    def run(self):
        evtx_name = 'OAlerts.evtx'
        if self.env[1]:
            if not os.path.exists(self.env[4][1]):
                return
            full_path = self.env[4][1] + evtx_name
        else:
            full_path = CONSTANT.EVENTLOG + evtx_name
            copy(full_path, self.env[4][1], 'Not copied "{}"'.format(evtx_name))

        items = []
        head = [CONSTANT.EVENTLOG_KEYWORD, False, CONSTANT.OFFICE, 3]
        checked_id = [300]
        import libs.ParseEvtx.Evtx as evtx
        with evtx.Evtx(full_path) as log:
            for event in log.records():
                try:
                    system_tag = event.lxml()[0]
                    logged_time = system_tag[5].get("SystemTime")
                    provider_name = system_tag[0].get("Name")
                    event_id = system_tag[1].text
                    if not logged_time: continue
                    if int(event_id) in checked_id:
                        # if self.timeline:
                        #     if datetime.datetime.strptime(logged_time, "%Y-%m-%d %H:%M:%S.%f") < self.timeline:
                        #         logging.info("[Exception] EID - {}, {} was skipped, it's more older timeline".format(event_id, provider_name))
                        #         continue
                        if system_tag[2].text == '1':
                            level = 'Fatal'
                        elif system_tag[2].text == '2':
                            level = 'Error'
                        elif system_tag[2].text == '3':
                            level = 'Warning'
                        elif system_tag[2].text == '4':
                            level = 'Information'
                        data_tag = event.lxml()[1]
                        etc = data_tag[0].text
                        items.append([head, logged_time, provider_name, event_id, level, etc, event.xml()])
                except Exception as e:
                    if int(event_id) in checked_id:
                        logging.info('[Error] EID - {} in "{}": {}'.format(event_id, evtx_name, e))
        self.artifacts_list += items
        self.completed.emit()

class PrefetchAnalyzerThread(QThread):
    completed = pyqtSignal()

    def __init__(self, env, artifacts_list, timeline=None):
        QThread.__init__(self)
        self.env = env
        self.artifacts_list = artifacts_list
        self.timeline = timeline

    def run(self):
        if not self.env[4][0]: return
        from libs.ParsePrefetch.prefetch import Prefetch
        items = []
        included = {
            # swNum, originColor, reExecColor, WERColor
            "ACRORD32.EXE": [CONSTANT.ADOBE_READER, 1, 2, 4],
            "MICROSOFTEDGE.EXE": [CONSTANT.EDGE, 1, 1, 3],
            "HWP.EXE": [CONSTANT.HWP, 1, 2, 5],
            "IEXPLORE.EXE": [CONSTANT.IE, 1, 6, 3],
            "WINWORD.EXE": [CONSTANT.OFFICE, 1, 2, 5],
            "POWERPNT.EXE": [CONSTANT.OFFICE, 1, 2, 5],
            "EXCEL.EXE": [CONSTANT.OFFICE, 1, 2, 5],
            "MICROSOFTEDGEBCHOST.EXE": [CONSTANT.EDGE, 5, 5, 3],
            "MICROSOFTEDGECP.EXE": [CONSTANT.EDGE, 5, 5, 3],
            "GBB.EXE": [CONSTANT.HWP, 3, 3, 5],
            "GSWIN32C.EXE": [CONSTANT.HWP, 3, 3, 5],
            "WMIPRVSE.EXE": [CONSTANT.OFFICE, 3, 3, 5],
            "EQNEDT32.EXE": [CONSTANT.OFFICE, 3, 3, 6],
            "DW20.EXE": [CONSTANT.OFFICE, 3, 3, 5],
            "DWWIN.EXE": [CONSTANT.OFFICE, 3, 3, 5],
            "FLTLDR.EXE": [CONSTANT.OFFICE, 3, 3, 5]
        }

        full_path = self.env[4][0] if self.env[1] else CONSTANT.PREFETCH
        for file_name in os.listdir(full_path):
            if file_name.endswith(".pf"):
                if os.path.getsize(full_path + file_name) == 0:
                    continue
                try:
                    p = Prefetch(full_path + file_name)
                    if not self.env[1]:
                        copy(CONSTANT.PREFETCH + file_name,
                             self.env[4][0],
                             'Not copied "{}"'.format(file_name))
                except Exception as e:
                    logging.info("[Error] {} could not be parsed. {}".format(file_name, e))
                    continue
                pf_name = "{}-{}.pf".format(p.executableName, p.hash)
                created_time = p.volumesInformationArray[0]["Creation Date"]
                content = p.getContents()
                if p.executableName in included.keys():
                    number_list = included[p.executableName]
                    items.append([
                        [CONSTANT.PREFETCH_KEYWORD, False, number_list[0], number_list[1]],
                        created_time, pf_name, p.executableName, "Create", content
                    ])
                    for timestamp in p.timestamps:
                        items.append([
                            [CONSTANT.PREFETCH_KEYWORD, False, number_list[0], number_list[2]],
                            timestamp, pf_name, p.executableName, "Execute", content
                        ])
                    continue
                elif p.executableName == "WERFAULT.EXE":
                    head = [CONSTANT.PREFETCH_KEYWORD, False, number_list[0], number_list[3]]
                    for target in included.keys():
                        flag = False
                        for rsc in p.resources:
                            if target.lower() in rsc.rsplit('\\', 1)[-1].lower():
                                flag = True
                                number_list = included[target]
                                items.append([head, created_time, pf_name, p.executableName, "Create", content])
                                for timestamp in p.timestamps:
                                    items.append([head, timestamp, pf_name, p.executableName, "Execute", content])
                                break
                        if flag: break
                    continue
                elif p.executableName in ["CMD.EXE", "POWERSHELL.EXE"]:
                    head = [CONSTANT.PREFETCH_KEYWORD, True, 7, 7, 7, 7, 7, 7]
                    items.append([head, created_time, pf_name, p.executableName, "Create", content])
                    for timestamp in p.timestamps:
                        items.append([head, timestamp, pf_name, p.executableName, "Execute", content])
                    continue
                head = [CONSTANT.PREFETCH_KEYWORD, True, 0, 0, 0, 0, 0, 0]
                items.append([head, created_time, pf_name, p.executableName, "Create", content])
                for timestamp in p.timestamps:
                    items.append([head, timestamp, pf_name, p.executableName, "Execute", content])
        self.artifacts_list += items
        self.completed.emit()

class JumpListAnalyzerThread(QThread):
    completed = pyqtSignal()

    def __init__(self, env, artifacts_list, timeline=None):
        QThread.__init__(self)
        self.env = env
        self.artifacts_list = artifacts_list
        self.timeline = timeline

    def run(self):
        if self.env[1]:
            dir_path = self.env[4][3]
            if not dir_path:
                return
        else:
            dir_path = CONSTANT.JUMPLIST[0]

        from libs.ParseJumpList.JumpListParser import lnk_file_header, lnk_file_after_header, destlist_data
        import olefile
        contents = CONSTANT.JUMPLIST_HASH[:12] + CONSTANT.JUMPLIST_HASH[15:25]
        extension = ".automaticDestinations-ms"

        items = []
        lnk_head = [
            [CONSTANT.LNKFILE_KEYWORD, False, CONSTANT.ADOBE_READER, 2],
            [CONSTANT.LNKFILE_KEYWORD, False, CONSTANT.OFFICE, 2],
            [CONSTANT.LNKFILE_KEYWORD, False, CONSTANT.HWP, 2]
        ]
        dest_head = [
            [CONSTANT.DESTLIST_KEYWORD, False, CONSTANT.ADOBE_READER, 2],
            [CONSTANT.DESTLIST_KEYWORD, False, CONSTANT.OFFICE, 2],
            [CONSTANT.DESTLIST_KEYWORD, False, CONSTANT.HWP, 2]
        ]

        for content in contents:
            file_name = content[1] + extension
            full_path = dir_path + file_name
            if not os.path.exists(full_path):
                logging.info("[Exception] {} JumpList doesn't exists".format(contents[0]))
                continue
            ole = olefile.OleFileIO(full_path)

            head_idx = 1
            if content[0][0] == 'H':
                head_idx = 2
            elif content[0][0] == 'A':
                head_idx = 0

            for item in ole.listdir():
                file = ole.openstream(item)
                file_data = file.read()
                header_value = file_data[:4]
                try:
                    if header_value[0] == 76:
                        lnk_header = lnk_file_header(file_data[:76])
                        lnk_after_header = lnk_file_after_header(file_data)
                        # if timeline:
                        #     if datetime.datetime.strptime(lnk_header, "%Y-%m-%d %H:%M:%S.%f") < timeline:
                        #         logging.info("[Exception] A log in {} JumpList is skipped, it's more older timeline".format(contents[0]))
                        #         continue
                        items.append([
                            lnk_head[head_idx],
                            lnk_header[1],                  # Accessed Time
                            lnk_after_header[3],            # LocalBasePath
                            "[LNK]" + lnk_after_header[0],  # Drive Type
                            lnk_header[3],                  # File Size
                            lnk_header[2],                  # Created Time
                            [full_path.rsplit("\\", 1)[-1], content[0], "LNK", lnk_header + lnk_after_header]
                        ])
                    else:
                        dest_list = destlist_data(file_data[:ole.get_size(item)])
                        for d in dest_list:
                            items.append([
                                dest_head[head_idx],
                                d[0],  # destlist_object_timestamp
                                d[1],  # Data = FullPath
                                d[1].rsplit("\\", 1)[-1],  # FileName
                                d[3],  # destlist_entry_access_count
                                d[5],  # destlist_access_time
                                [full_path.rsplit("\\", 1)[-1], content[0], "dest_files", d]
                            ])
                except:
                    pass
            if not self.env[1]:
                copy(full_path, self.env[4][3], 'Not copied "{}"'.format(file_name))
        self.artifacts_list += items
        self.completed.emit()

class WebArtifactAnalyzerThread(QThread):
    completed = pyqtSignal()

    def __init__(self, env, artifacts_list, timeline=None):
        QThread.__init__(self)
        self.env = env
        self.artifacts_list = artifacts_list
        self.timeline = timeline

    def run(self):
        import glob
        import subprocess
        if self.env[1]:
            file_list = glob.glob(self.env[3] + "WebCacheV*.dat")
            if not file_list:
                logging.info("Not found WebCacheV*.dat.")
                return
            full_path = file_list[0]
        else:
            dir_name = CONSTANT.IE_ARTIFACT_PATH[self.env[0]]["History"]
            file_list = glob.glob(dir_name + "WebCacheV*.dat")
            if not file_list:
                logging.info("Not found WebCacheV*.dat.")
                return
            full_path = file_list[0]
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.call('taskkill /f /im "taskhostw.exe"', startupinfo=si)
            subprocess.call('taskkill /f /im "dllhost.exe"', startupinfo=si)
            rst = copy(full_path,
                       self.env[3],
                       "[Error] WebArtifact - Please terminate any process using " + full_path)
            if not rst:
                logging.info("Please terminate any process using " + full_path)
                return

        import libs.ParseWebArtifact.WebArtifact as WebArtifact
        history = WebArtifact.getHistory(full_path, self.timeline)
        caches = WebArtifact.getContent(full_path, self.timeline)
        self.artifacts_list += history + caches
        self.completed.emit()

class AppCompatCacheAnalyzerThread(QThread):
    completed = pyqtSignal()

    def __init__(self, env, artifacts_list, timeline=None):
        QThread.__init__(self)
        self.env = env
        self.artifacts_list = artifacts_list
        self.timeline = timeline

    def run(self):
        if self.env[1] and self.env[4][4]:
            dir_list = os.listdir(self.env[4][4])
            rst = False
            if dir_list:
                for _path in dir_list:
                    if _path.startswith("System"):
                        rst = self.get_from_hive(self.env[4][4] + _path)
                        break
        elif not self.env[1]:
            # 레지스트리 하이브 파일 복사
            rst = self.get_local_data()
        if rst:
            self.artifacts_list += rst
        self.completed.emit()

    def get_from_hive(self, _path):
        try:
            from libs.ParseRegistry import ShimCacheParser, Registry, RegistryParse
            reg = Registry.Registry(_path)
        except ImportError as e:
            logging.info("[Error] Hive parsing requires Registry.py... Didn\'t find it, bailing...\n{}".format(e))
            return False
        except RegistryParse.ParseException as e:
            logging.info("[Error] parsing %s: %s" % (_path, e))
            return False
        except Exception as e:
            logging.info("[Error] {}".format(e))
            return False

        out_list = []
        partial_hive_path = ('Session Manager', 'AppCompatCache', 'AppCompatibility')
        if reg.root().path() in partial_hive_path:
            if reg.root().path() == 'Session Manager':
                if reg.root().find_key('AppCompatCache').values():
                    keys = reg.root().find_key('AppCompatCache').values()
            else:
                keys = reg.root().values()
            for k in keys:
                bin_data = str(k.value())
                tmp_list = ShimCacheParser.read_cache(bin_data, timeline=self.timeline)
                if tmp_list:
                    path_name = "Registry Path:\n"
                    path_name += 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\%s' % (k.name())
                    for row in tmp_list:
                        row.append(path_name)
                        if row not in out_list:
                            out_list.append(row)
        else:
            root = reg.root().subkeys()
            for key in root:
                try:
                    if 'controlset' in key.name().lower():
                        session_man_key = reg.open('%s\Control\Session Manager' % key.name())
                        for subkey in session_man_key.subkeys():
                            # Read the Shim Cache structure.
                            if ('appcompatibility' in subkey.name().lower() or
                                    'appcompatcache' in subkey.name().lower()):
                                bin_data = subkey['AppCompatCache'].value()
                                tmp_list = ShimCacheParser.read_cache(bin_data, timeline=self.timeline)
                                if tmp_list:
                                    path_name = "Registry Path:\n"
                                    path_name += 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\%s' % (subkey.name())
                                    for row in tmp_list:
                                        row.append(path_name)
                                        if row not in out_list:
                                            out_list.append(row)

                except Registry.RegistryKeyNotFoundException as e:
                    logging.info("[Error] {}".format(e))
                    continue

        if len(out_list) == 0:
            return False
        else:
            return out_list

    def get_local_data(self):
        from libs.ParseRegistry.ShimCacheParser import read_cache
        out_list = []
        try:
            import winreg as reg
        except ImportError as e:
            logging.info("{}".format(e))
            return
        hReg = reg.ConnectRegistry(None, reg.HKEY_LOCAL_MACHINE)
        hSystem = reg.OpenKey(hReg, r'SYSTEM')
        for i in range(1024):
            try:
                control_name = reg.EnumKey(hSystem, i)
                if 'currentcontrolset' in control_name.lower():
                    hSessionMan = reg.OpenKey(hReg, 'SYSTEM\\%s\\Control\\Session Manager' % control_name)
                    for i in range(1024):
                        try:
                            subkey_name = reg.EnumKey(hSessionMan, i)
                            if ('appcompatibility' in subkey_name.lower()
                                    or 'appcompatcache' in subkey_name.lower()):
                                appcompat_key = reg.OpenKey(hSessionMan, subkey_name)
                                bin_data = reg.QueryValueEx(appcompat_key, 'AppCompatCache')[0]
                                tmp_list = read_cache(bin_data, timeline=self.timeline)
                                if tmp_list:
                                    path_name = "Registry Path:\n"
                                    path_name += 'SYSTEM\\%s\\Control\\Session Manager\\%s' % (control_name, subkey_name)
                                    for row in tmp_list:
                                        row.append(path_name)
                                        if row not in out_list:
                                            out_list.append(row)
                        except EnvironmentError as e:
                            logging.info("[Error] {}".format(e))
                            break
            except EnvironmentError as e:
                logging.info("[Error] {}".format(e))
                break
        if len(out_list) == 0:
            return None
        else:
            return out_list

class JumpListAnalyzerThreadForViewer(QThread):
    performanced = pyqtSignal(str)
    completed = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)

    def set_target(self, env, hash_list):
        self.env = env
        self.hash_list = hash_list

    def run(self):
        file_list = os.listdir(self.env[4][3])
        if not file_list:
            self.completed.emit("The file does not exist.")
            return
        for item in CONSTANT.JUMPLIST_HASH:
            for file_name in file_list:
                if item[1] in file_name:
                    self.hash_list.append(item)

        total = len(self.hash_list)
        import olefile
        from libs.ParseJumpList.JumpListParser import lnk_file_header, lnk_file_after_header, destlist_data
        for idx in range(len(self.hash_list)):
            full_path = self.env[4][3] + file_list[idx]
            lnk_files = []
            dest_files = []
            ole = olefile.OleFileIO(full_path)
            for item in ole.listdir():
                file = ole.openstream(item)
                file_data = file.read()
                header_value = file_data[:4]  # first four bytes value should be 76 bytes
                try:
                    if header_value[0] == 76:  # first four bytes value should be 76 bytes
                        lnk_header = lnk_file_header(file_data[:76])
                        lnk_after_header = lnk_file_after_header(file_data)  # after 76 bytes to last 100 bytes
                        lnk_files.append([
                            lnk_header[1],
                            lnk_header[0],
                            lnk_header[2],
                            lnk_after_header[3],
                            lnk_header[3],
                            str(int(item[0], 16)),
                            lnk_after_header[0],
                            lnk_after_header[1],
                            lnk_after_header[2],
                        ])
                    else:
                        dest_files = destlist_data(file_data[:ole.get_size(item)])
                except Exception as e:
                    print(e)
                    pass
            from operator import itemgetter
            self.hash_list[idx].append({
                "lnk_files": sorted(lnk_files, key=itemgetter(0)) if lnk_files else [],
                "dest_files": sorted(dest_files, key=itemgetter(0)) if dest_files else [],
            })
            self.performanced.emit("Analyzing {}/{}...".format(idx+1, total))
        self.completed.emit("Complete")

def getRecentFileCache(filepath):
    contents = []
    with open(filepath, "rb") as f:
        offset = 0x14
        file_size = os.stat(filepath)[6]
        f.seek(0)
        f.seek(offset)
        while (offset < file_size):
            try:
                str_len = int.from_bytes(f.read(4), byteorder='little')
                if not str_len:
                    break
                fnlen = (str_len + 1) * 2
                contents.append(f.read(fnlen).decode('unicode-escape').replace('\x00', ''))
                file_size = offset + fnlen
            except Exception as e:
                return False, "{}".format(e)
    return True, contents

def copy(src, dest, msg):
    try:
        import shutil
        shutil.copy2(src, dest)
    except Exception as e:
        logging.info('[Error] {}\nCause: {}'.format(msg, e))
        return False
    return True