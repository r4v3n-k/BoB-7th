import pyesedb
import datetime
import modules.constant as CONSTANT

DOM_EXTENSION = ['htm', 'html', 'js', 'css', 'php', 'jsp', 'asp', 'aspx']
DOC_EXTENSION = ['doc', 'docx', 'hta', 'rtf', 'xls', 'ppts', 'pptx', 'woff', 'sct', 'wsc']
ETC_EXTENSION = ['dll', 'bat']

#Get file time
def getFiletime(dt):
    if dt == 0:
        return "-"
    else:
        try:
            microseconds = dt / 10
            seconds, microseconds = divmod(microseconds, 1000000)
            days, seconds = divmod(seconds, 86400)
            return "{}".format(datetime.datetime(1601, 1, 1) + datetime.timedelta(days, seconds, microseconds))
        except:
            return "-"

#Fix response data
def fixRespData(txtin):
    if txtin is not None:
        # fixed = txtin.decode("unicode-escape").replace("\n","\\").replace("\r","\\").replace(","," ").replace('"'," ")
        fixed = txtin.decode("unicode-escape").replace(","," ").replace('"'," ")
        return ''.join(i for i in fixed if ord(i)<128)
    else:
        return ""

#Get history
def getHistory(filepath, timeline=None):
    esedb_file = pyesedb.file()
    esedb_file.open(filepath)
    containers = esedb_file.get_table_by_name("Containers")

    #Get list of containers that contain IE history
    histContList = []
    histNameDict = dict()
    histDirDict = dict()
    for cRecords in containers.records:
        if "Hist" in cRecords.get_value_data_as_string(8):
            histContList.append("Container_%s" % cRecords.get_value_data_as_integer(0))
            histNameDict["Container_%s" % cRecords.get_value_data_as_integer(0)] = cRecords.get_value_data_as_string(8)
            histDirDict["Container_%s" % cRecords.get_value_data_as_integer(0)] = cRecords.get_value_data_as_string(10)

    items = []
    head = [CONSTANT.HISTORY_KEYWORD, False, CONSTANT.IE, 1] # Edge OK
    #Get history from each container
    for hcl in histContList:
        histCont = esedb_file.get_table_by_name(hcl)
        for hRecords in histCont.records:
            _url = hRecords.get_value_data_as_string(17)
            if _url.count("@") > 0:
                URL = _url.split("@")[1]
                if not URL.startswith("http"):
                    continue
                accessedTime = getFiletime(hRecords.get_value_data_as_integer(13))
                modifiedTime = getFiletime(hRecords.get_value_data_as_integer(12))
                content = [
                    "{}.{}".format(hRecords.get_value_data_as_integer(1), hRecords.get_value_data_as_integer(0)),
                    histNameDict[hcl],
                    "{}".format(getFiletime(hRecords.get_value_data_as_integer(10))),
                    "{}".format(accessedTime),
                    "{}".format(modifiedTime),
                    "{}".format(getFiletime(hRecords.get_value_data_as_integer(11))),
                    "{}".format(getFiletime(hRecords.get_value_data_as_integer(9))),
                    str(hRecords.get_value_data_as_integer(15)),
                    str(hRecords.get_value_data_as_integer(8)),
                    _url,
                    hRecords.get_value_data_as_string(18),
                    str(hRecords.get_value_data_as_integer(5)),
                    histDirDict[hcl],
                    None
                ]
                items.append([head, accessedTime, URL, modifiedTime, content])

    return items

#Get content
def getContent(filepath, timeline=None):
    esedb_file = pyesedb.file()
    esedb_file.open(filepath)
    containers = esedb_file.get_table_by_name("Containers")

    #Get list of containers that contain IE content
    histContList = []
    histNameDict = dict()
    histDirDict = dict()
    for cRecords in containers.records:
        if "Content" in cRecords.get_value_data_as_string(8):
            histContList.append("Container_%s" % cRecords.get_value_data_as_integer(0))
            histNameDict["Container_%s" % cRecords.get_value_data_as_integer(0)] = cRecords.get_value_data_as_string(8)
            histDirDict["Container_%s" % cRecords.get_value_data_as_integer(0)] = cRecords.get_value_data_as_string(10)

    items = []
    head = [
        [CONSTANT.CACHE_KEYWORD, False, CONSTANT.IE, 1],
        [CONSTANT.CACHE_KEYWORD, False, CONSTANT.HWP, 0],
        [CONSTANT.CACHE_KEYWORD, False, CONSTANT.OFFICE, 4],
        [CONSTANT.CACHE_KEYWORD, False, CONSTANT.ADOBE_READER, 0],
        [CONSTANT.CACHE_KEYWORD, False, CONSTANT.IE, 0],
    ]

    #Get content from each container
    for hcl in histContList:
        histCont = esedb_file.get_table_by_name(hcl)
        for hRecords in histCont.records:
            headIdx = 4
            fileName = hRecords.get_value_data_as_string(18)
            if fileName.count("."):
                extension = fileName.split(".")[1]
                if extension in DOM_EXTENSION:
                    headIdx = 0
                elif extension in DOC_EXTENSION:
                    headIdx = 2
                elif extension == 'hwp':
                    headIdx = 1
                elif extension == 'pdf':
                    headIdx = 3
            else:
                continue
            accessedTime = getFiletime(hRecords.get_value_data_as_integer(13))
            _url = hRecords.get_value_data_as_string(17)
            fileSize = str(hRecords.get_value_data_as_integer(5))
            createdTime = str(getFiletime(hRecords.get_value_data_as_integer(10)))
            content = [
                "{}.{}".format(hRecords.get_value_data_as_integer(1), hRecords.get_value_data_as_integer(0)),
                histNameDict[hcl],
                "{}".format(createdTime),
                "{}".format(accessedTime),
                "{}".format(getFiletime(hRecords.get_value_data_as_integer(12))),
                "{}".format(getFiletime(hRecords.get_value_data_as_integer(11))),
                "{}".format(getFiletime(hRecords.get_value_data_as_integer(9))),
                str(hRecords.get_value_data_as_integer(15)),
                str(hRecords.get_value_data_as_integer(8)),
                _url,
                fileName,
                fileSize,
                histDirDict[hcl],
                fixRespData(hRecords.get_value_data(21)),
            ]
            items.append([head[headIdx], accessedTime, _url, fileName, fileSize, createdTime, content])
    return items

def getDownloads(type, filepath, prefetchList, timeline=None):
    esedb_file = pyesedb.file()
    esedb_file.open(filepath)
    containers = esedb_file.get_table_by_name("Containers")

    # Get list of containers that contain IE downloads
    histContList = []
    histNameDict = dict()
    histDirDict = dict()
    for cRecords in containers.records:
        if "download" in cRecords.get_value_data_as_string(8):
            histContList.append("Container_%s" % cRecords.get_value_data_as_integer(0))
            histNameDict["Container_%s" % cRecords.get_value_data_as_integer(0)] = cRecords.get_value_data_as_string(8)
            histDirDict["Container_%s" % cRecords.get_value_data_as_integer(0)] = cRecords.get_value_data_as_string(10)

    # Get downloads from each container
    items = []
    head = ["Download", 1]
    grayHead = ["Download", 0]
    for hcl in histContList:
        histCont = esedb_file.get_table_by_name(hcl)
        for hRecords in histCont.records:
            accessedTime = getFiletime(hRecords.get_value_data_as_integer(13))
            if timeline:
                if datetime.datetime.strptime(accessedTime, "%Y-%m-%d %H:%M:%S.%f") < timeline:
                    continue
            fileName = hRecords.get_value_data_as_string(18)
            _url = hRecords.get_value_data_as_string(17)
            downloadPath = fixRespData(hRecords.get_value_data(21)) # 파싱필요
            print(_url, fileName)
            print(hRecords.get_value_data(21))
            print("*"*80)
            if fileName:
                extension = fileName.split('.')[1]
                if type in [CONSTANT.IE, CONSTANT.EDGE]:
                    if extension == "exe":
                        prefetchList += fileName.upper()
                        print(fileName)
                elif type == CONSTANT.OFFICE and extension not in DOC_EXTENSION:
                    continue
                elif type == CONSTANT.HWP and extension != "hwp":
                    continue
                elif type == CONSTANT.ADOBE_READER and extension != "pdf":
                    continue
            else:
                head = grayHead
            fileSize = str(hRecords.get_value_data_as_integer(5))
            content = [
                "{}.{}".format(hRecords.get_value_data_as_integer(1), hRecords.get_value_data_as_integer(0)),
                histNameDict[hcl],
                "{}".format(getFiletime(hRecords.get_value_data_as_integer(10))),
                "{}".format(accessedTime),
                "{}".format(getFiletime(hRecords.get_value_data_as_integer(12))),
                "{}".format(getFiletime(hRecords.get_value_data_as_integer(11))),
                "{}".format(getFiletime(hRecords.get_value_data_as_integer(9))),
                str(hRecords.get_value_data_as_integer(15)),
                str(hRecords.get_value_data_as_integer(8)),
                _url,
                fileName,
                fileSize,
                histDirDict[hcl],
                downloadPath,
            ]
            items.append([head, accessedTime, _url, fileName, fileSize, "", content])
        return items