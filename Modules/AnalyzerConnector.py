import logging
import Modules.Basic.basic_functions as bf
import os
import re
import xml.etree.ElementTree as ET
import datetime

class Trace:
    def __init__(self):
        self.name = ''
        self.ext = ''
        self.path = []
        self.m_timestamp = ''
        self.a_timestamp = ''
        self.size = ''
        self.content = ''
        self.type = ''
        self.source = ''

def msofficeParser(path_dir):
    datalist = []
    filecount = 0

    filelist = os.listdir(path_dir)
    for file in filelist:
        fullpath = os.path.join(path_dir, file)
        if file == 'com.microsoft.Word.plist':
            try:
                pl = bf.plistparser(fullpath)
                for key in pl:
                    if 'NSWindow Frame CUI' in key:
                        data_info = Trace()
                        datalist.append(data_info)
                        datalist[filecount].name = key.split('/')[-1].split('.')[0:-1][0]
                        datalist[filecount].ext = key.split('/')[-1].split('.')[-1]
                        datalist[filecount].path = key.split('/')[1:-1]
                        datalist[filecount].type = 'MSOFFICE'
                        datalist[filecount].source = 'com.microsoft.Word.plist'
                        filecount += 1
            except Exception as e:
                logging.error(f"Error occurred while parsing {file}: {str(e)}")

        elif file == 'ComRPCDB':
            # Not developed yet
            continue
        elif file == 'ComRPCDB-wal':
            try:
                with open(fullpath, 'rb') as output_file:
                    s = output_file.read()
                    file_start_offset = [m.start() for m in re.finditer(b"\x4D\x45\x4F\x57\x04\x00\x00\x00\x0F\x00\x00\x00\x00\x00\x00\x00\xC0\x00\x00\x00\x00\x00\x00\x46\x03\x03\x00\x00\x00\x00\x00\x00\xC0\x00\x00\x00\x00\x00\x00\x46\x00\x00\x00\x00", s)]
                    for i in range(0, len(file_start_offset)):
                        if s[file_start_offset[i]+44] != 92: #0x52
                            data_info = Trace()
                            datalist.append(data_info)
                            tempfilesize = s[file_start_offset[i]+50]
                            if 'https' not in str(s[file_start_offset[i]+54:file_start_offset[i]+54+tempfilesize-1])[2:].replace('\\\\','/').split('/')[0]:
                                datalist[filecount].path = str(s[file_start_offset[i]+54:file_start_offset[i]+54+tempfilesize-1])[2:].replace('\\\\','/').split('/')[1:-1]
                            datalist[filecount].name = str(s[file_start_offset[i]+54:file_start_offset[i]+54+tempfilesize-1])[2:].replace('\\\\','/').split('/')[-1].split('.')[0]
                            datalist[filecount].ext = str(s[file_start_offset[i]+54:file_start_offset[i]+54+tempfilesize-1])[2:-1].replace('\\\\','/').split('/')[-1].split('.')[1]
                            datalist[filecount].type = 'MSOFFICE'
                            datalist[filecount].source = 'ComRPCDB'
                            filecount += 1
            except Exception as e:
                logging.error(f"Error occurred while parsing {file}: {str(e)}")

        elif 'MicrosoftRegistrationDB' in file:
            try:
                cur = bf.sqliteparser(fullpath)
                cur.execute(
                    "SELECT node_id FROM HKEY_CURRENT_USER_values where value like '%docx%' or value like '%pptx%' or value like '%xlsx%'")
                rows = cur.fetchall()
                nodeid_list = []
                for row in set(rows):
                    nodeid_list.append(row[0])
                for nodeid in nodeid_list:
                    cur.execute("SELECT name, value FROM HKEY_CURRENT_USER_values WHERE node_id = ?", (nodeid,))
                    rows = cur.fetchall()
                    for row in rows:
                        data_info = Trace()
                        datalist.append(data_info)
                        datalist[filecount].type = 'MSOFFICE'
                        datalist[filecount].source = 'MicrosoftRegistrationDB'

                        if row[0] == 'Datetime':
                            datalist[filecount].a_timestamp = row[1]
                        if row[0] == 'Timestamp':
                            datalist[filecount].a_timestamp = row[1]
                        if row[0] == 'File Path':
                            if 'Document in' in row[1]:
                                datalist[filecount].name = row[1].split(' in ')[1].split('.')[0]
                                datalist[filecount].ext = row[1].split(' in ')[1].split('.')[1]
                            else:
                                datalist[filecount].path = row[1].split('/')[1:-1]
                                datalist[filecount].name = row[1].split('/')[-1].split('.')[0:-1][0]
                                datalist[filecount].ext = row[1].split('/')[-1].split('.')[-1]
                        if row[0] == 'FileName':
                            datalist[filecount].name = row[1].split('.')[0:-1][0]
                            datalist[filecount].ext = row[1].split('.')[-1]
                        if row[0] == 'DocumentUrl':
                            datalist[filecount].path = row[1].replace('file:///', '').split('/')[0:-1]
                        if row[0] == 'FileSizeInBytes':
                            datalist[filecount].size = row[1]
                        if row[0] == 'Data':
                            datalist.remove(data_info)
                            filecount = filecount - 1
                        filecount = filecount + 1
            except Exception as e:
                logging.error(f"Error occurred while parsing {file}: {str(e)}")

    return datalist

def googledriveParser(path_dir):
    datalist = []
    filecount = 0

    filelist = os.listdir(path_dir)
    for file in filelist:
        fullpath = os.path.join(path_dir, file)
        if file == 'metadata_sqlite_db' or file == 'mirror_metadata_sqlite.db':
            try:
                cur = bf.sqliteparser(fullpath)
                cur.execute("SELECT local_title, modified_date, viewed_by_me_date, file_size from items WHERE is_folder is 0")
                rows = cur.fetchall()

                for row in rows:
                    if 'docx' in row[0].split('.')[-1] or 'pptx' in row[0].split('.')[-1] or 'xlsx' in row[0].split('.')[-1]: # msoffice only
                        data_info = Trace()
                        datalist.append(data_info)
                        datalist[filecount].type = 'GOOGLEDRIVE'
                        datalist[filecount].source = file

                        datalist[filecount].name = row[0].split('.')[0:-1][0]
                        datalist[filecount].ext = row[0].split('.')[-1]
                        datalist[filecount].m_timestamp = datetime.datetime.utcfromtimestamp(row[1]/1000).strftime('%Y-%m-%dT%H:%M:%SZ')
                        datalist[filecount].a_timestamp = datetime.datetime.utcfromtimestamp(row[2]/1000).strftime('%Y-%m-%dT%H:%M:%SZ')
                        datalist[filecount].size = row[3]
                        filecount += 1
            except Exception as e:
                logging.error(f"Error occurred while parsing {file}: {str(e)}")

            try:
                cur.execute("SELECT proto from deleted_items")
                rows = cur.fetchall()
                for row in rows:
                    data_info = Trace()
                    datalist.append(data_info)
                    with open('temp_output.bin', 'wb') as output_file:
                        output_file.write(row[0])
                    with open('temp_output.bin', 'rb') as output_file:
                        s = output_file.read()
                        temppoint = s.find(b'local-title')
                        output_file.seek(temppoint+12)
                        tempfilesize = output_file.read(1)[0]
                        output_file.seek(temppoint+13)
                        target_data = output_file.read()[0:tempfilesize]
                        datalist[filecount].name = target_data.decode('utf-8').split('.')[0:-1][0]
                        datalist[filecount].ext = target_data.decode('utf-8').split('.')[-1]
                        datalist[filecount].type = 'GOOGLEDRIVE'
                        datalist[filecount].source = file + '(deleted)'
                        filecount += 1
            except Exception as e:
                logging.error(f"Error occurred while parsing {file}: {str(e)}")

        elif 'finder_ext_' in file or 'drive_fs' in file:
            try:
                with open(fullpath, 'r') as output_file:
                    s = output_file.read()
                    file_start_offset = [m.start() for m in re.finditer('Path:', s)]
                    file_end_offset = [m.start() for m in re.finditer(', Status:', s)]
                    for i in range(0, len(file_start_offset)):
                        data_info = Trace()
                        datalist.append(data_info)
                        datalist[filecount].name = s[file_start_offset[i] + 7:file_end_offset[i]].split('/')[-1].split('.')[
                            0]
                        datalist[filecount].ext = s[file_start_offset[i] + 7:file_end_offset[i]].split('/')[-1].split('.')[
                            1]
                        datalist[filecount].path = s[file_start_offset[i] + 7:file_end_offset[i]].split('/')[0:-1]
                        datalist[filecount].type = 'GOOGLEDRIVE'
                        datalist[filecount].source = file
                        filecount += 1
            except Exception as e:
                logging.error(f"Error occurred while parsing {file}: {str(e)}")

    return datalist

def spotlightParser(path_dir):
    datalist = []
    filecount = 0

    # Shortcuts
    filelist = os.listdir(path_dir)
    for file in filelist:
        fullpath = path_dir + '/' + file
        # Shortcuts
        if 'com.apple.spotlight.Shortcuts' in file:
            try:
                pl = bf.plistparser(fullpath)
                for key in pl:
                    if '.docx' in pl[key]['URL'] or '.pptx' in pl[key]['URL'] or '.xlsx' in pl[key]['URL'] or '.pdf' in pl[key]['URL']:
                        data_info = Trace()
                        datalist.append(data_info)
                        datalist[filecount].name = pl[key]['DISPLAY_NAME'].split('.')[0]
                        datalist[filecount].ext = pl[key]['URL'].split('.')[-1]
                        datalist[filecount].path = pl[key]['URL'].replace('file:///','').split('/')[0:-1]
                        datalist[filecount].a_timestamp = str(pl[key]['LAST_USED']).replace(' ','T')+'Z'
                        datalist[filecount].type = 'SPOTLIGHT'
                        datalist[filecount].source = file
                        filecount = filecount + 1
            except Exception as e:
                logging.error(f"Error occurred while parsing {file}: {str(e)}")

        # store.db
        # Parsecd
        # JournalAttr

    return datalist

def knowledgeCParser(path_dir):
    datalist = []
    filecount = 0

    filelist = os.listdir(path_dir)
    for file in filelist:
        if file == 'knowledgeC.db':
            try:
                fullpath = path_dir + '/' + file
                cur = bf.sqliteparser(fullpath)
                cur.execute(
                    "select Z_DKSAFARIHISTORYMETADATAKEY__TITLE from ZSTRUCTUREDMETADATA where Z_DKSAFARIHISTORYMETADATAKEY__TITLE like '%.docx%'")
                rows = cur.fetchall()
                for row in rows:
                    data_info = Trace()
                    datalist.append(data_info)
                    datalist[filecount].name = row[0].split('.docx')[0]
                    datalist[filecount].ext = 'docx'
                    datalist[filecount].type = 'knowledgeC'
                    datalist[filecount].source = file
                    filecount = filecount + 1

                cur.execute(
                    "select Z_DKAPPLICATIONACTIVITYMETADATAKEY__CONTENTDESCRIPTION from ZSTRUCTUREDMETADATA where Z_DKAPPLICATIONACTIVITYMETADATAKEY__CONTENTDESCRIPTION like '%.docx%'")
                rows = cur.fetchall()
                for row in rows:
                    data_info = Trace()
                    datalist.append(data_info)
                    datalist[filecount].name = row[0].split('/')[-1].split('.')[0]
                    datalist[filecount].ext = 'docx'
                    datalist[filecount].type = 'knowledgeC'
                    datalist[filecount].source = file
                    filecount = filecount + 1

                cur.execute(
                    "select Z_DKAPPLICATIONACTIVITYMETADATAKEY__USERACTIVITYREQUIREDSTRING from ZSTRUCTUREDMETADATA where Z_DKAPPLICATIONACTIVITYMETADATAKEY__USERACTIVITYREQUIREDSTRING like '%.docx%'")
                rows = cur.fetchall()
                for row in rows:
                    if len(row[0].split("/t='")[1].split('.')[0]) < 20:
                        data_info = Trace()
                        datalist.append(data_info)
                        datalist[filecount].name = row[0].split("/t='")[1].split('.')[0]
                        datalist[filecount].ext = 'docx'
                        datalist[filecount].type = 'knowledgeC'
                        datalist[filecount].source = file
                        filecount = filecount + 1

            except Exception as e:
                logging.error(f"Error occurred while parsing {file}: {str(e)}")

    return datalist

def iCloudParser(path_dir):
    datalist = []
    filecount = 0

    #client.db-wal
    #server.db-wal

    return datalist

def teamsParser(path_dir):
    datalist = []
    file_count = 0

    for filename in os.listdir(path_dir):
        if '3.log' in filename:
            fullpath = os.path.join(path_dir, filename)
            try:
                with open(fullpath, 'rb') as file:
                    content = file.read()
                    file_start_offsets = [m.start() for m in re.finditer(b"\x22\x74\x69\x74\x6C\x65\x22\x3A\x22", content)]
                    file_end_offsets = [m.start() for m in re.finditer(b"\x2E\x64\x6F\x63\x78\x22\x2C\x22\x73\x74\x61\x74\x65\x22", content)]

                    for i in range(len(file_start_offsets)):
                        trace = Trace()
                        trace.name = str(content[file_start_offsets[i] + 9:file_end_offsets[i]+5])[2:-1].split('.')[0]
                        trace.ext = str(content[file_start_offsets[i] + 9:file_end_offsets[i]+5])[2:-1].split('.')[1]
                        trace.type = 'TEAMS'
                        trace.source = filename
                        datalist.append(trace)
                        file_count += 1
            except Exception as e:
                logging.error(f"Error occurred while parsing {file}: {str(e)}")

    return datalist

def mailParser(path_dir):
    datalist = []
    filecount = 0

    filelist = os.listdir(path_dir)
    for file in filelist:
        if 'Envelope Index-wal' in file:
            try:
                fullpath = path_dir + '/' + file
                with open(fullpath, 'rb') as output_file:
                    s = output_file.read()
                    file_start_offset = [m.start() for m in re.finditer(b"\x03\x3D\x01\xEF\x98\x80", s)]
                    for i in range(0, len(file_start_offset)):
                        data_info = Trace()
                        datalist.append(data_info)
                        datalist[filecount].name = str(s[file_start_offset[i] + 6:file_start_offset[i] + 100])[2:-1].split('.')[0]
                        datalist[filecount].ext = 'docx'
                        datalist[filecount].type = 'MAIL'
                        datalist[filecount].source = file
                        filecount += 1
            except Exception as e:
                logging.error(f"Error occurred while parsing {file}: {str(e)}")

    return datalist

def recentfilesParser(path_dir):
    datalist = []
    filecount = 0

    filelist = os.listdir(path_dir)
    for file in filelist:
        if 'com.apple.textedit.sfl2' in file:
            try:
                fullpath = path_dir + '/' + file
                with open(fullpath, 'rb') as output_file:
                    s = output_file.read()
                    file_start_offset = [m.start() for m in re.finditer(b"\x04\x10", s)]
                    for i in range(0, len(file_start_offset)-1):
                        data_info = Trace()
                        datalist.append(data_info)

                        beforeFileSize = s[file_start_offset[i]+2]

                        pathtempFirstOffset = file_start_offset[i]+2+beforeFileSize+4

                        pathtempFirstSize = s[pathtempFirstOffset]
                        pathtempFirstOffset = pathtempFirstOffset+8 # 첫번째 위치로 이동
                        datalist[filecount].path.append(s[pathtempFirstOffset:pathtempFirstOffset+pathtempFirstSize])


                        pathtempSecondSizeSize = s[pathtempFirstOffset+pathtempFirstSize+3]
                        pathtempSecondOffset = pathtempFirstOffset+pathtempFirstSize+3+8
                        datalist[filecount].path.append(s[pathtempSecondOffset:pathtempSecondOffset+pathtempSecondSizeSize])

                        pathtempThirdSizeSize = s[pathtempSecondOffset + pathtempSecondSizeSize + 1]
                        pathtempThirdOffset = pathtempSecondOffset + pathtempSecondSizeSize + 1 + 8
                        datalist[filecount].path.append(s[pathtempThirdOffset:pathtempThirdOffset + pathtempThirdSizeSize])

                        pathtempFourthSizeSize = s[pathtempThirdOffset + pathtempThirdSizeSize]
                        pathtempFourthOffset = pathtempThirdOffset + pathtempThirdSizeSize + 8
                        datalist[filecount].path.append(s[pathtempFourthOffset:pathtempFourthOffset + pathtempFourthSizeSize])

                        pathtempFifthSizeSize = s[pathtempFourthOffset + pathtempFourthSizeSize+2]
                        pathtempFifthOffset = pathtempFourthOffset + pathtempFourthSizeSize+2 + 8
                        datalist[filecount].name = str(s[pathtempFifthOffset:pathtempFifthOffset + pathtempFifthSizeSize])[2:].split('.docx')[0]
                        datalist[filecount].ext = 'docx'
                        datalist[filecount].type = 'RECENTFILES'
                        datalist[filecount].source = file
                        filecount += 1
            except Exception as e:
                logging.error(f"Error occurred while parsing {file}: {str(e)}")

    return datalist