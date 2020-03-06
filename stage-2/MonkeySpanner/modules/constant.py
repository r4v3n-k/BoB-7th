import os

cwd = os.getcwd()
TITLE = "MonkeySpanner"
ICON_PATH = [
    "{}\\logo.ico".format(cwd),
    "{}\\img\\filter.png".format(cwd),
    "{}\\img\\conversion.png".format(cwd),
    "{}\\img\\logo.png".format(cwd)
]
# OS
WIN7 = 'Windows7'
WIN10 = 'Windows10'

# Software Number
ADOBE_READER = 1
ADOBE_FLASH_PLAYER = 2
EDGE = 3
HWP = 4
IE = 5
OFFICE = 6
LPE = 7

# Software Keyword
ADOBE_READER_KEYWORD = "Adobe Reader"
ADOBE_FLASH_PLAYER_KEYWORD = "Adobe Flash Player"
EDGE_KEYWORD = "Microsoft Edge"
HWP_KEYWORD = "Hancom Word Process"
IE_KEYWORD = "Internet Explorer"
OFFICE_KEYWORD = "MS-Office"
LPE_KEYWORD = "Kernel(Local-Privilege-Escalation)"

SOFTWARE = {
    ADOBE_READER_KEYWORD: ADOBE_READER,
    # ADOBE_FLASH_PLAYER_KEYWORD: ADOBE_FLASH_PLAYER,
    EDGE_KEYWORD: EDGE,
    HWP_KEYWORD: HWP,
    IE_KEYWORD: IE,
    OFFICE_KEYWORD: OFFICE,
}
'''
SOFTWARE_SELECTION = [
    "---- Select Software ----",
    ADOBE_READER_KEYWORD,
    ADOBE_FLASH_PLAYER_KEYWORD,
    EDGE_KEYWORD,
    HWP_KEYWORD,
    IE_KEYWORD,
    OFFICE_KEYWORD,
    # LPE_KEYWORD,
]
'''

# Artifact List
PREFETCH_KEYWORD = "Prefetch"
EVENTLOG_KEYWORD = "EventLog"
WER_KEYWORD = "ErrorReport"
HISTORY_KEYWORD = "History"
DOWNLOAD_KEYWORD = "Download"
CACHE_KEYWORD = "WebCache"
REGISTRY_KEYWORD = "Registry"
LNKFILE_KEYWORD = "JumpList[L]"
DESTLIST_KEYWORD = "JumpList[D]"

ARTIFACT_LIST = [
    PREFETCH_KEYWORD,
    EVENTLOG_KEYWORD,
    WER_KEYWORD,
    HISTORY_KEYWORD,
    CACHE_KEYWORD,
    REGISTRY_KEYWORD,
    LNKFILE_KEYWORD,
    DESTLIST_KEYWORD
]

COLOR_LIST = {
    "Gray": 0,
    "Red": 1,
    "Orange": 2,
    "Yellow": 3,
    "Green": 4,
    "Blue": 5,
    "Navy": 6,
    "Purple": 7
}

# Table Header
TABLE_HEADER = {
    PREFETCH_KEYWORD: ["Timeline", "File Name", "Executable Name", "Action", ""],                       # 4 columns
    WER_KEYWORD: ["Modified Time", "Path", "Module", "Exception Code", "Created Time"],                 # 5 columns
    REGISTRY_KEYWORD: ["Modified Time", "Execution Path", "Size", "Exec Flag", "Registry Key"],         # 5 columns
    LNKFILE_KEYWORD: ["Accessed Time", "File Path", "Drive Type", "Size", "Created Time"],              # 5 columns
    DESTLIST_KEYWORD: ["Timestamp", "File Path", "File Name", "Access", "Last Recorded Time"],    # 5 columns
    EVENTLOG_KEYWORD: ["Logged Time", "Provider Name", "Event ID", "Level", "Data"],                    # 5 columns
    HISTORY_KEYWORD: ["Accessed Time", "URL", "Modified Time", "", ""],                                 # 3 columns
    CACHE_KEYWORD: ["Accessed Time", "URL", "File Name", "Size", "Created Time"],                       # 5 columns
    DOWNLOAD_KEYWORD: ["Accessed Time", "URL", "File Name", "Size", "Downloaded Path"],                       # 5 columns
}

# Environment Variable
LOCALAPPDATA = os.environ["LOCALAPPDATA"]   # C:\\Users\\[username]\\AppData\\Local
APPDATA = os.environ["APPDATA"]             # C:\\Users\\[username]\\AppData\\Roaming
SYSTEMDRIVE = os.environ["SYSTEMDRIVE"]     # C:\\Users\\[username]\\AppData\\Roaming
SYSTEMROOT = os.environ["SYSTEMROOT"]       # C:\\Windows


# Common Path
REGISTRY = {
    'SAM': SYSTEMROOT + "\\System32\\config\\SAM",
    'SYSTEM': SYSTEMROOT + "\\System32\\config\\SYSTEM",
    'SECURITY': SYSTEMROOT + "\\System32\\config\\SECURITY",
    'SOFTWARE': SYSTEMROOT + "\\System32\\config\\SOFTWARE",
}

PREFETCH = SYSTEMROOT + '\\Prefetch\\'
WER = {
    WIN7: LOCALAPPDATA + "\\Microsoft\\Windows\\WER\\ReportArchive\\",
    WIN10: 'C:\\ProgramData\\Microsoft\\Windows\\WER\\ReportArchive\\'
}
EVENTLOG = SYSTEMROOT + '\\System32\\Winevt\\logs\\'
JUMPLIST = [
    APPDATA + '\\Microsoft\\Windows\\Recent\\AutomaticDestinations\\',      # AutomaticDestinations
    APPDATA + '\\Microsoft\\Windows\\Recent\\CustomDestinations\\'          # CustomDestinations
]

JUMPLIST_HASH = [
    ['Excel 2010 (32-bit)', '9839aec31243a928'],            # [00]
    ['Excel 2010 (64-bit)', '6e855c85de07bc6a'],            # [01]
    ['Excel 2013 (32-bit)', 'f0275e8685d95486'],            # [02]
    ['Excel 2013, 2016 (64-bit)', 'b8ab77100df80ab2'],      # [03]
    ['PowerPoint 2010 (32-bit)', '9c7cc110ff56d1bd'],       # [04]
    ['PowerPoint 2010 (64-bit)', '5f6e7bc0fb699772'],       # [05]
    ['PowerPoint 2013, 2016 (64-bit)', 'd00655d2aa12ff6d'], # [06]
    ['Word 2010 (32-bit)', 'a7bd71699cd38d1c'],             # [07]
    ['Word 2010 (64-bit)', '44a3621b32122d64'],             # [08]
    ['Word 2013 (32-bit)', 'a4a5324453625195'],             # [09]
    ['Word 365 (32-bit)', 'fb3b0dbfee58fac8'],              # [10]
    ['Word 2016 (64-bit)', 'a18df73203b0340e'],             # [11]
    ['Internet Explorer 8/9/10 (32-bit)', '28c8b86deab549a1'],  # [12]
    ['Internet Explorer 11 (64-bit)', '5da8f997fd5f9428'],      # [13]
    ['Adobe Flash CS5 (32-bit)', 'e2a593822e01aed3'],       # [14]
    ['HWP 2010', '20f18d57e149e379'],                       # [15]
    ['HWP 2014', '35a932d3d281dbfd'],                       # [16]
    ['HWP 2018', 'bcc51871d3e0b707'],                       # [17]
    ['Adobe Acrobat 9.4.0', '23646679aaccfae0'],            # [18]
    ['Adobe Reader 9', '23646679aaccfae0'],                 # [19]
    ['Adobe Reader 7.1.0', 'f0468ce1ae57883d'],             # [20]
    ['Adobe Reader 8.1.2', 'c2d349a0e756411b'],             # [21]
    ['Adobe Reader X 10.1.0', 'ee462c3b81abb6f6'],          # [22]
    ['Acrobat Reader 15.x', 'de48a32edcbe79e4'],            # [23]
    ['Acrobat Reader 18.x??', 'ff103e2cc310d0d'],           # [24]
    ['Chrome 9.0.597.84 / 12.0.742.100 / 13.0.785.215 / 26', '5d696d521de238c3'],     # [25]
    ['Edge 42.17134.1.0', '9d1f905ce5044aee'],                           # [26]
    ['Edge 44.17763.1.0', '90ca02effa84052f'],                           # [27]
]

# Software Path
FLASH_ARTIFACT_PATH = [
    APPDATA + '\\Macromedia\\Flash Player\\#SharedObjects\\',   # Directory
    APPDATA + '\\Adobe\\Flash Player\\NativeCache\\NativeCache.directory',      # Cache
    APPDATA + '\\Macromedia\\Flash Player\\macromedia.com\\support\\flashplayer\\sys\\settings.sol',    # settings
]

HWP_ARTIFACT_PATH = {           # HWP
    'Recent': APPDATA + '\\HNC\\Office\\Recent',
}
IE_ARTIFACT_PATH = {
    WIN7: {
        'History': LOCALAPPDATA + '\\Microsoft\\Windows\\WebCache\\',
        'Cache': {
            'IE10': LOCALAPPDATA + '\\Microsoft\\Windows\\Temporary Internet Files\\Content.IE5\\',
            'IE11': LOCALAPPDATA + '\\Microsoft\\Windows\\INetCookies\\'
        },
        'Download': {},
        'Cookie': {
            'IE10': APPDATA + '\\Microsoft\\Windows\\Cookies\\',
            'IE11': LOCALAPPDATA + '\\Microsoft\\Windows\\INetCache\IE\\',
        },
        'SessionRestore': LOCALAPPDATA + '\\Microsoft\\Internet Explorer\\Recovery\\'
    },
    WIN10: {
        'History': LOCALAPPDATA + '\\Microsoft\\Windows\\WebCache\\',
        'Cache': {
            'IE10': LOCALAPPDATA + '\\Microsoft\\Windows\\Temporary Internet Files\\Content.IE5\\',
            'IE11': LOCALAPPDATA + '\\Microsoft\\Windows\\INetCookies\\'
        },
        'Download': {

        },
        'Cookie': {
            'IE10': APPDATA + '\\Microsoft\\Windows\\Cookies\\',
            'IE11': LOCALAPPDATA + '\\Microsoft\\Windows\\INetCache\\IE\\',
        },
        'SessionRestore': LOCALAPPDATA + '\\Microsoft\\Internet Explorer\\Recovery\\',
    }
}

############################# AboutWidget
aboutContents = {
            '1': '"MonkeySpanner" was made by a project manager, \n'
                 'Eunjin, Kwon, in the team, "Eunjin with MonkeySpanner".\n'
                 'Our team had performed research about security.\n'
                 'Our topic is "Precise Analysis of attacker\'s behavior\n'
                 'through Offensive Research". '
                 'But, our project scope is only to exploit vulnerabilities of software in Windows.\n\n'
                 '# Next page explain contents as below.\n'
                 '    (1) What our direction was\n'
                 '    (2) What purpose we approached as\n'
                 '    (3) Which expected effect many people can get \n'
                 '        by using this tool, and contacting with our research.\n',
            '1-1': 'A software fundamentally behaves by being executed commands of assembly unit from CPU.\n'
                   'In Digital Forensic, `Artifact` means data created \n'
                   'automatically by system or software.\n'
                   'Creating data automatically is to execute the commands \n'
                   'when do some behavior or satisfy some conditions. \n'
                   'Like Event Log, Prefetch, Registry, ... and vice versa.\n'
                   '(above artifacts from Operating System, artifacts created from each software can exists.)\n\n'
                   'So, Let Think about `Artifact Created When an Error Occurs`\n\n'
                   'This is because a exception code of are executed \n'
                   'when error inside sw or system occurs.\n'
                   '(some exception code can’t create artifacts)\n\n'
                   'In fact, all software can’t create such artifacts, but\n'
                   'if it is popular, it\'ll handle exception, and deal with it for user to find cause of error.\n'
                   'This is why popular softwares are able to create some artifacts when an error occurs.',
            '1-2': 'We needed to research popular software (like MS-Office, IE, Chrome, … etc) in Windows.\n\n'
                   'Also, we want to check on the following curiosity.\n'
                   '    (1) When exploit code executed, which artifact is left?\n'
                   '    (2) Is this treated as the artifact created when an error\n'
                   '        occurs ?\n'
                   '    (3) Such artifacts are different when not same\n'
                   '        vulnerability ?\n\n'
                   'In case (3), If such artifacts are similar,\n'
                   'Are these common for every exploit in the software only?\n\n'
                   'So, we determined to find out `common artifacts set` for popular software when error occurs in Windows.\n\n'
                   'Our research is meaningful historically, but we worried about practicality (is this useful?)\n\n'
                   '"What about Incident Response ?"\n\n'
                   'Fundamentally, it’s important to prevent from propagating malicious program after incident occurs.'
                   'So, we thought that our finding, common artifacts set will be artifacts occurred during malicious program spread.\n\n'
                   '# Direction: To define common artifacts set for target software.\n\n'
                   '# Goal: Our research reports seems to be used as logical grounds for precisely analyzing and classifying attacker’s behavior in Incident Response or Analysis',
            '1-3': 'The tool MonkeySapnner aims to be used to precisely classify and analyze attacker\'s behavior '
                   'in the process of responding to and analyzing the incident.\n'
                   'Today, the many forensic tools that add convenience are unfortunately '
                   'not in the process of extracting the associations of artifacts.\n'
                   '(There is, of course, such a tool.)\n\n'
                   'However, analysts are inconvenienced because this process requires a lot of time to invest in analysis.\n'
                   'Our tools will help you relieve this discomfort.\n\n'
                   'With the Monkey Spanner, you will be able to see artifacts grouped by software, '
                   'and you will be able to quickly identify actual inflows and respond quickly to infringement.',
            '2': 'We called the artifacts grouped by specified software "Artifact Prototype".\n(It is just simple reason)',
            '2-1': 'When you actually run malicious code, you may or may not have a variety of artifacts. \n'
                   'We do not always think that our defined artifact prototype is complete because we always consider that there is not.'
                   'It just started from the idea that it could be grouped and used as an indicator of an intrusion. \n\n'
                   'When there are various artifacts left in normal execution, they may remain redundant. '
                   'In this case, it\'s hard to see it as a significant artifact. '
                   'What we want to do is to help us identify the infringement, or to handle the error. \n\n'
                   'To summarize, we have defined the artifact prototype as a set of meaningful artifacts '
                   'that can be used to identify infringement of an infected malware by attacking certain software.',
            '2-2': 'Based on artifacts created time, if classfy exploit code,\n\n'
                   '0.1 process execute\n'
                   '        1.1 just got crash\n'
                   '        2.1 run to shellcode\n'
                   '\t    2.2 dll injection / file create\n'
                   '\t    2.3 file delete / downloader\n\n'
                   'We thought it was the most significant artifact in terms of artifacts that could distinguish each step.'
                   'In fact, what I wanted most was to find artifacts due to errors, but in the Windows environment, '
                   'not all software left these artifacts.\n\n'
                   'Usually the first stage was a prefetch, a jump list, a web artifact, '
                   'and the second stage was an event log, a temporary file, or a deleted file. '
                   'To confirm this fact, we analyzed vulnerabilities exploited in exploit-kits with high attack success rates. '
                   'The artifacts for each CVE number were grouped and excluded if not significant. '
                   'As the process repeats, more and more artifact prototypes of certain software have been completed.',
            '3': 'Please note that it is never absolute.\n'
                 'In other words, it does not show any traces of all malicious programs.'
                 'However, it is clear that this is the result of three months of research.\n\n'
                 'Please refer to "2-2 Methodology" for the way we have proceeded.',
            '3-1': '[Red] Prefetch (ACRORD32.EXE): only Creation\n\n'
                   '[Orange] Prefetch (ACRORD32.EXE): only Execution\n\n'
                   '[Orange] JumpList for Adobe Reader\n\n'
                   '[Yellow] Event Log: Application.evtx EID 1000\n\n'
                   '[Yellow] Event Log: Microsoft-Windows-WER-Diag%4Operational.evtx EID 2\n\n'
                   '[Green] Prefetch (WERFAULT.EXE) for Error Reporting referring to "acrobatreader.exe"\n\n'
                   '[Blue] Event Log: Fault-Tolerant-Heap/Operational.evtx EID 1001\n\n'
                   '[Blue] Event Log: Application.evtx EID 1001\n\n'
                   '[Navy] Window Error Report For Adobe Reader: Report.wer\n\n'
                   '[Purple] Prefetch (CMD.EXE, POWERSHELL.EXE) after 1st timeline\n\n\n'
                   '[Gray] Prefetch for the others\n\n'
                   '[Gray] Registry - AppCompatCache\n\n'
                   '[Gray] Web Cache for only extension ".pdf"\n\n\n'
                   '(PASS to Dialog) Application Compatibility Artifacts\n'
                   '    - recentfilecache.bcf (in Windows 7)\n'
                   '    - Amache.hve (in Windows 10)\n',
            '3-2': 'Preparing',
            '3-3': '[Red] Web History\n\n'
                   '[Red] Web Cache for only DOM Files like html, js, css, etc\n\n'
                   '[Red] Prefetch (MICROSOFTEDGE.EXE) before 1st timeline of history\n\n'
                   '[Orange] Event Log: Application.evtx EID 1000\n\n'
                   '[Yellow] Prefetch (SVCHOST.EXE)\n\n'
                   '[Green] Prefetch (WERFAULT.EXE) for Error Reporting After 1st timeline\n\n'
                   '[Blue] Event Log: Application.evtx EID 1001\n\n'
                   '[Navy] Window Error Report For Edge: Report.wer\n\n'
                   '[Navy] Prefetch related Edge \n\t- MICROSOFTEDGECP.EXE\n\t- MICROSOFTEDGEBCHOST.EXE)\n\n'
                   '[Navy] Web Download: dll, doc, docx, hta, xls, woff\n\n'
                   '[Navy] Web Cache: dll, doc, docx, hta, xls, woff\n\n'
                   '[Purple] Prefetch (CMD.EXE, POWERSHELL.EXE) after 1st timeline\n\n\n'
                   '[Gray] Prefetch for the others\n\n'
                   '[Gray] Registry - AppCompatCache\n\n'
                   '(PASS to Dialog) Application Compatibility Artifacts\n'
                   '    - recentfilecache.bcf (in Windows 7)\n'
                   '    - Amache.hve (in Windows 10)\n',
            '3-4': '[Red] Prefetch (HWP.EXE): only Creatation\n\n'
                   '[Orange] Prefetch (HWP.EXE): only Execution\n\n'
                   '[Orange] JumpList for HWP\n\n'
                   '[Yellow] Prefetch related HWP \n\t- GBB.EXE\n\t- GSWIN32C.EXE\n\n'
                   '[Green] Event Log: Microsoft-Windows-WER-Diag/Operational.evtx EID 2\n\n'
                   '[Green] Event Log: Fault-Tolerant-Heap/Operational.evtx EID 1001\n\n'
                   '[Blue] Prefetch (WERFAULT.EXE) for Error Reporting\n\n'
                   '[Blue] Event Log: Application.evtx EID 1000, 1001\n\n'
                   '[Blue] Window Error Repor for HWP: Report.wer\n\n'
                   '[Navy] File System Log for Deleted Files (.PS, .EPS)\n\n'
                   '[Purple] Prefetch (CMD.EXE, POWERSHELL.EXE) after 1st timeline\n\n\n'
                   '[Gray] Prefetch for the others\n\n'
                   '[Gray] Registry - AppCompatCache\n\n'
                   '[Gray] Web Cache for only extension ".hwp"'
                    '(PASS to Dialog) Application Compatibility Artifacts\n'
                   '    - recentfilecache.bcf (in Windows 7)\n'
                   '    - Amache.hve (in Windows 10)\n',
            '3-5': '[Red] Web History\n\n'
                   '[Red] Web Cache for only DOM Files like html, js, css, etc\n\n'
                   '[Red] Prefetch (IEXPLORE.EXE) before 1st timeline of history\n\n'
                   '[Orange] Event Log: Application.evtx EID 1000, 1001\n\n'
                   '[Yellow] Event Log: Microsoft-Windows-WER-Diag/Operational.evtx EID 2\n\n'
                   '[Yellow] Prefetch (WERFAULT.EXE) for Error Reporting\n\n'
                   '[Yellow] Window Error Repor for IE: Report.wer\n\n'
                   '[Green] Event Log: Fault-Tolerant-Heap/Operational.evtx EID 1001\n\n'
                   '[Blue] Prefetch (IEXPLORE.EXE): only Execution After 1st timeline\n\n'
                   '[Navy] Web Download: dll, doc, docx, hta, xls, woff, exe\n\n'
                   '[Navy] Web Cache: dll, doc, docx, hta, xls, woff\n\n'
                   '[Purple] Prefetch (CMD.EXE, POWERSHELL.EXE)\n\n\n'
                   '[Gray] Prefetch for the others\n\n'
                   '[Gray] Registry - AppCompatCache\n\n'
                    '(PASS to Dialog) Application Compatibility Artifacts\n'
                   '    - recentfilecache.bcf (in Windows 7)\n'
                   '    - Amache.hve (in Windows 10)\n',
            '3-6': '[Red] Prefetch (WINWORD.EXE, POWERPNT.EXE, EXCEL.EXE): only Creation\n\n'
                   '[Orange] Prefetch (WINWORD.EXE, POWERPNT.EXE, EXCEL.EXE): only Execution\n\n'
                   '[Orange] JumpList for MS-Office\n\n'
                   '[Yellow] Prefetch related MS-Office\n\t- WMIPRVSE.EXE\n\t- EQNEDT32.EXE\n\t- DW20.EXE\n\t- DWWIN.EXE\n\t- FLTLDR.EXE\n\n'
                   '[Yellow] Event Log: Microsoft-Office-Alerts.evtx EID:300'
                   '[Green] Event Log: Microsoft-Windows-WER-Diagnostics EID 2\n\n'
                   '[Green] Event Log: Fault-Tolerant-Heap EID 1001\n\n'
                   '[Green] Web Cache: doc, docx, xls, ppt, pptx, hta, xls, woff\n\n'
                   '[Blue] Prefetch (WERFAULT.EXE) for Error Reporting\n\n'
                   '[Blue] Window Error Report for MS-Office: Report.wer\n\n'
                   '[Blue] Event Log: Application.evtx EID 1000, 1001\n\n'
                   '[Navy] File System Log for Deleted Files (.tmp)\n\n'
                   '[Purple] Prefetch (CMD.EXE, POWERSHELL.EXE)\n\n\n'
                   '[Gray] Prefetch for the others\n\n'
                   '[Gray] Registry - AppCompatCache\n\n'
                    '(PASS to Dialog) Application Compatibility Artifacts\n'
                   '    - recentfilecache.bcf (in Windows 7)\n'
                   '    - Amache.hve (in Windows 10)\n',
            '3-7': 'Preparing',
            '4': '\n[Parser for EventLog]\n\tApache License, Version 2.0.\n\n'
                 '[Parser for NTFS Log]\n\tMIT License\n\n'
                 '[Parser for Prefetch]\n\tApache License, Version 2.0.\n\n'
                 '[Parser for Registry]\n\tApache License, Version 2.0.\n\n'
                 '[Parser for Jumplist]\n\t\tNone\n\n'
                 '[Parser for WebArtifact]\n\t\tNone\n\n\n\n'
                 '#################\n'
                 '#  Source Link  #\n'
                 '#################\n\n'
                 '[EventLog]\n     https://github.com/williballenthin/python-evtx\n\n'
                 '[NTFSLog]\n     https://github.com/NTFSparse/ntfs_parse\n\n'
                 '[JumpList]\n     https://github.com/Bhupipal/JumpListParser\n\n'
                 '[Prefetch]\n     https://github.com/PoorBillionaire/Windows-Prefetch-Parser\n\n'
                 '[Registry]\n     https://github.com/mandiant/ShimCacheParser\n\n'
                 '[WebArtifact]\n     https://github.com/jtmoran/webcacheView\n\n'
                 'The above source codes was developed as Python 2,\n'
                 'but I modified all of that to run on Python 3.\n'
                 'Also, needed function was added.\n'
                 '\t- To encode and decode Korean\n'
                 '\t- To translate MFT in NTFS Log\n'
                 '\t- To match to UTC time\n\n'
                 'Also, unneeded function was removed.',
            '4-1': 'Apache License\nVersion 2.0, January 2004\nhttp://www.apache.org/licenses/\n\n'
                   'TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION\n\n'
                   '   1. Definitions.\n\n'
                   '"License" shall mean the terms and conditions for use, reproduction,'
                   'and distribution as defined by Sections 1 through 9 of this document.\n\n'
                   '"Licensor" shall mean the copyright owner or entity authorized by'
                   'the copyright owner that is granting the License.\n\n'
                   '"Legal Entity" shall mean the union of the acting entity and all'
                   'other entities that control, are controlled by, or are under common'
                   'control with that entity. For the purposes of this definition,'
                   '"control" means (i) the power, direct or indirect, '
                   'to cause thedirection or management of such entity, whether by contract or '
                   'otherwise, or (ii) ownership of fifty percent (50%) or more of the'
                   'outstanding shares, or (iii) beneficial ownership of such entity.\n\n'
                   '"You" (or "Your") shall mean an individual or Legal Entity '
                   'exercising permissions granted by this License.\n\n'
                   '"Source" form shall mean the preferred form for making modifications,'
                   'including but not limited to software source code, documentation'
                   'source, and configuration files.\n\n'
                   '"Object" form shall mean any form resulting from mechanical'
                   'transformation or translation of a Source form, including but'
                   'not limited to compiled object code, generated documentation,'
                   'and conversions to other media types.\n\n'
                   '"Work" shall mean the work of authorship, whether in Source or '
                   'Object form, made available under the License, as indicated by a'
                   'copyright notice that is included in or attached to the work'
                   '(an example is provided in the Appendix below).\n\n'
                   '"Derivative Works" shall mean any work, whether in Source or Object '
                   'form, that is based on (or derived from) the Work and for which the '
                   'editorial revisions, annotations, elaborations, or other modifications '
                   'represent, as a whole, an original work of authorship. For the purposes '
                   'of this License, Derivative Works shall not include works that remain '
                   'separable from, or merely link (or bind by name) to the interfaces of, '
                   'the Work and Derivative Works thereof.\n\n'
                   '"Contribution" shall mean any work of authorship, including '
                   'the original version of the Work and any modifications or additions '
                   'to that Work or Derivative Works thereof, that is intentionally '
                   'submitted to Licensor for inclusion in the Work by the copyright owner '
                   'or by an individual or Legal Entity authorized to submit on behalf of '
                   'the copyright owner. For the purposes of this definition, "submitted" '
                   'means any form of electronic, verbal, or written communication sent '
                   'to the Licensor or its representatives, including but not limited to '
                   'communication on electronic mailing lists, source code control systems, '
                   'and issue tracking systems that are managed by, or on behalf of, the '
                   'Licensor for the purpose of discussing and improving the Work, but '
                   'excluding communication that is conspicuously marked or otherwise '
                   'designated in writing by the copyright owner as "Not a Contribution.\n\n"'
                   '"Contributor" shall mean Licensor and any individual or Legal Entity '
                   'on behalf of whom a Contribution has been received by Licensor and '
                   'subsequently incorporated within the Work.\n\n'
                   '2. Grant of Copyright License. Subject to the terms and conditions of '
                   'this License, each Contributor hereby grants to You a perpetual, '
                   'worldwide, non-exclusive, no-charge, royalty-free, irrevocable '
                   'copyright license to reproduce, prepare Derivative Works of, '
                   'publicly display, publicly perform, sublicense, and distribute the '
                   'Work and such Derivative Works in Source or Object form.\n\n'
                   '3. Grant of Patent License. Subject to the terms and conditions of '
                   'this License, each Contributor hereby grants to You a perpetual, '
                   'worldwide, non-exclusive, no-charge, royalty-free, irrevocable '
                   '(except as stated in this section) patent license to make, have made, '
                   'use, offer to sell, sell, import, and otherwise transfer the Work, '
                   'where such license applies only to those patent claims licensable '
                   'by such Contributor that are necessarily infringed by their '
                   'Contribution(s) alone or by combination of their Contribution(s) '
                   'with the Work to which such Contribution(s) was submitted. If You '
                   'institute patent litigation against any entity (including a '
                   'cross-claim or counterclaim in a lawsuit) alleging that the Work '
                   'or a Contribution incorporated within the Work constitutes direct '
                   'or contributory patent infringement, then any patent licenses '
                   'granted to You under this License for that Work shall terminate '
                   'as of the date such litigation is filed.\n\n'
                   '4. Redistribution. You may reproduce and distribute copies of the '
                   'Work or Derivative Works thereof in any medium, with or without '
                   'modifications, and in Source or Object form, provided that You '
                   'meet the following conditions:\n\n'
                   '(a) You must give any other recipients of the Work or '
                   'Derivative Works a copy of this License; and\n\n'
                   '(b) You must cause any modified files to carry prominent notices '
                   'stating that You changed the files; and\n\n'
                   '(c) You must retain, in the Source form of any Derivative Works '
                   'that You distribute, all copyright, patent, trademark, and '
                   'attribution notices from the Source form of the Work, '
                   'excluding those notices that do not pertain to any part of '
                   'the Derivative Works; and\n\n'
                   '(d) If the Work includes a "NOTICE" text file as part of its '
                   'distribution, then any Derivative Works that You distribute must '
                   'include a readable copy of the attribution notices contained '
                   'within such NOTICE file, excluding those notices that do not '
                   'pertain to any part of the Derivative Works, in at least one '
                   'of the following places: within a NOTICE text file distributed '
                   'as part of the Derivative Works; within the Source form or '
                   'documentation, if provided along with the Derivative Works; or, '
                   'within a display generated by the Derivative Works, if and '
                   'wherever such third-party notices normally appear. The contents '
                   'of the NOTICE file are for informational purposes only and '
                   'do not modify the License. You may add Your own attribution '
                   'notices within Derivative Works that You distribute, alongside '
                   'or as an addendum to the NOTICE text from the Work, provided '
                   'that such additional attribution notices cannot be construed '
                   'as modifying the License.\n\n'
                   'You may add Your own copyright statement to Your modifications and '
                   'may provide additional or different license terms and conditions '
                   'for use, reproduction, or distribution of Your modifications, or '
                   'for any such Derivative Works as a whole, provided Your use, '
                   'reproduction, and distribution of the Work otherwise complies with '
                   'the conditions stated in this License.\n\n'
                   '5. Submission of Contributions. Unless You explicitly state otherwise, '
                   'any Contribution intentionally submitted for inclusion in the Work '
                   'by You to the Licensor shall be under the terms and conditions of '
                   'this License, without any additional terms or conditions. '
                   'Notwithstanding the above, nothing herein shall supersede or modify '
                   'the terms of any separate license agreement you may have executed '
                   'with Licensor regarding such Contributions.\n\n'
                   '6. Trademarks. This License does not grant permission to use the trade '
                   'names, trademarks, service marks, or product names of the Licensor, '
                   'except as required for reasonable and customary use in describing the '
                   'origin of the Work and reproducing the content of the NOTICE file.\n\n'
                   '7. Disclaimer of Warranty. Unless required by applicable law or '
                   'agreed to in writing, Licensor provides the Work (and each '
                   'Contributor provides its Contributions) on an "AS IS" BASIS, '
                   'WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or '
                   'implied, including, without limitation, any warranties or conditions '
                   'of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A '
                   'PARTICULAR PURPOSE. You are solely responsible for determining the '
                   'appropriateness of using or redistributing the Work and assume any '
                   'risks associated with Your exercise of permissions under this License.\n\n'
                   '8. Limitation of Liability. In no event and under no legal theory, '
                   'whether in tort (including negligence), contract, or otherwise, '
                   'unless required by applicable law (such as deliberate and grossly '
                   'negligent acts) or agreed to in writing, shall any Contributor be '
                   'liable to You for damages, including any direct, indirect, special, '
                   'incidental, or consequential damages of any character arising as a '
                   'result of this License or out of the use or inability to use the '
                   'Work (including but not limited to damages for loss of goodwill, '
                   'work stoppage, computer failure or malfunction, or any and all '
                   'other commercial damages or losses), even if such Contributor '
                   'has been advised of the possibility of such damages.\n\n'
                   '9. Accepting Warranty or Additional Liability. While redistributing '
                   'the Work or Derivative Works thereof, You may choose to offer, '
                   'and charge a fee for, acceptance of support, warranty, indemnity, '
                   'or other liability obligations and/or rights consistent with this '
                   'License. However, in accepting such obligations, You may act only '
                   'on Your own behalf and on Your sole responsibility, not on behalf '
                   'of any other Contributor, and only if You agree to indemnify, '
                   'defend, and hold each Contributor harmless for any liability '
                   'incurred by, or claims asserted against, such Contributor by reason '
                   'of your accepting any such warranty or additional liability.\n\n'
                   'END OF TERMS AND CONDITIONS\n\n'
                   'APPENDIX: How to apply the Apache License to you\nr work.'
                   'To apply the Apache License to your work, attach the following '
                   'boilerplate notice, with the fields enclosed by brackets "[]" '
                   'replaced with your own identifying information. (Don\'t include '
                   'the brackets!)  The text should be enclosed in the appropriate '
                   'comment syntax for the file format. We also recommend that a '
                   'file or class name and description of purpose be included on the '
                   'same "printed page" as the copyright notice for easier '
                   'identification within third-party archives.\n\n'
                   'Copyright [yyyy] [name of copyright owner]\n\n'
                   'Licensed under the Apache License, Version 2.0 (the "License");\n'
                   'you may not use this file except in compliance with the License. '
                   'You may obtain a copy of the License at\n\n'
                   'http://www.apache.org/licenses/LICENSE-2.0\n\n'
                   'Unless required by applicable law or agreed to in writing, software '
                   'distributed under the License is distributed on an "AS IS" BASIS, '
                   'WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. '
                   'See the License for the specific language governing permissions and '
                   'limitations under the License.',
            '4-2': 'The MIT License (MIT)\n\n'
                   'Copyright (c) 2016 MonkeySpanner\n\n'
                   'Permission is hereby granted, free of charge, to any person obtaining a copy '
                   'of this software and associated documentation files (the "Software"), to deal '
                   'in the Software without restriction, including without limitation the rights '
                   'to use, copy, modify, merge, publish, distribute, sublicense, and/or sell '
                   'copies of the Software, and to permit persons to whom the Software is '
                   'furnished to do so, subject to the following conditions:\n\n'
                   'The above copyright notice and this permission notice shall be included in all '
                   'copies or substantial portions of the Software.\n\n'
                   'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR '
                   'IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, '
                   'FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE '
                   'AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER '
                   'LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, '
                   'OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE '
                   'SOFTWARE.',
        }