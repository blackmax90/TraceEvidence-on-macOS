import os
import logging
import Modules.Basic.basic_functions as bf

def spotlightExtractor(sourceFolder, destinationFolder, username):
    des = destinationFolder + '/spotlight'
    try:
        with os.scandir(f"{sourceFolder}/Users/{username}/Library/Application Support/com.apple.spotlight") as entries:
            for entry in entries:
                if entry.name == 'com.apple.spotlight.Shortcuts':
                    bf.file_copy(entry.path, des)
    except Exception as e:
        logging.error(f"Error extracting spotlight files: {e}")

    try:
        with os.scandir(f"{sourceFolder}/Users/{username}/Library/Metadata/CoreSpotlight/index.spotlightV3") as entries:
            for entry in entries:
                if 'journalAttr.' in entry.name:
                    bf.file_copy(entry.path, des)
    except Exception as e:
        logging.error(f"Error extracting spotlightV3 files: {e}")

    try:
        with os.scandir(f"{sourceFolder}/_.Spotlight-V100/Store-V2") as entries:
            for entry in entries:
                if 'journalAttr.' in entry.name:
                    bf.file_copy(entry.path, des)
    except Exception as e:
        logging.error(f"Error extracting Spotlight-V100 files: {e}")

    try:
        with os.scandir(f"{sourceFolder}/_.Spotlight-V100/Store-V2") as entries:
            for entry in entries:
                if '_.store.db' in entry.name:
                    bf.file_copy(entry.path, des)
    except Exception as e:
        logging.error(f"Error extracting store.db files: {e}")

def msofficeExtractor(sourceFolder, destinationFolder, username):
    des = destinationFolder + '/msoffice'
    try:
        fullpath = sourceFolder+'/Users/' + username + '/Library/Containers/com.microsoft.Word/Data/Library/Preferences'
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if 'com.microsoft.Word.plist' in file:
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error extracting com.microsoft.Word.plist: {e}")

    try:
        fullpath = sourceFolder+'/Users/' + username + '/Library/Group Containers/UBF8T346G9.Office/ComRPC32'
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if file == 'ComRPCDB' or file == 'ComRPCDB-wal':
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error extracting ComRPCDB or ComRPCDB-wal: {e}")

    try:
        fullpath = sourceFolder+'/Users/' + username + '/Library/Group Containers/UBF8T346G9.Office/MicrosoftRegistrationDB'
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if 'MicrosoftRegistrationDB' in file:
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error extracting MicrosoftRegistrationDB: {e}")

    try:
        fullpath = sourceFolder+'/Users/' + username + '/Library/Containers/com.microsoft.Word/Data/Library/Application Support/Microsoft/Temp'
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if 'WRF' in file or 'WRS' in file:
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error extracting WRF or WRS: {e}")

    try:
        fullpath = sourceFolder+'/Users/' + username + '/Library/Containers/com.microsoft.Word/Data/Library/Preferences'
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if 'com.microsoft.Word.securebookmarks.plist' in file:
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error extracting com.microsoft.Word.securebookmarks.plist: {e}")

def googledriveExtractor(sourceFolder, destinationFolder, username):
    des = destinationFolder + '/googledrive'
    fullpath = sourceFolder+'/Users/' + username + '/Library/Application Support/Google/DriveFS'
    if os.path.isdir(fullpath):
        for (path, dir, files) in os.walk(fullpath):
            for file in files:
                if 'metadata_sqlite' in file or 'psid' in file or 'structured_log' in file or 'finder_ext' in file or 'driver_ext' in file:
                    bf.file_copy(path+'/'+file, des)
    else:
        logging.error("Error extracting Google Drive: %s does not exist", fullpath)

def diagnosticExtractor(sourceFolder, destinationFolder, username):
    des = destinationFolder + '/diagnostic'
    try:
        fullpath = f"{sourceFolder}/private/var/db/diagnostics/Persist"
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if 'tracev3' in file:
                    bf.file_copy(f"{fullpath}/{file}", des)
    except Exception as e:
        logging.error(f"Error extracting diagnostic-persist-tracev3 files: {e}")

    try:
        fullpath = f"{sourceFolder}/private/var/db/diagnostics/Special"
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if 'tracev3' in file:
                    bf.file_copy(f"{fullpath}/{file}", des)
    except Exception as e:
        logging.error(f"Error extracting diagnostic-special-tracev3 files: {e}")

    try:
        fullpath = f"{sourceFolder}/private/var/log/DiagnosticMessages"
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if '.asl' in file:
                    bf.file_copy(f"{fullpath}/{file}", des)
    except Exception as e:
        logging.error(f"Error extracting diagnostic-asl files: {e}")

def recentfileExtractor(sourceFolder, destinationFolder, username):
    des = destinationFolder + '/recentfiles'
    try:
        fullpath = sourceFolder+'/Users/' + username + '/Library/Application Support/com.apple.sharedfilelist/com.apple.LSSharedFileList.ApplicationRecentDocuments'
        if os.path.isdir(fullpath) == True:
            for file in bf.check_file_in_folder(fullpath):
                if 'com.apple.textedit' in file or 'com.apple.preview' in file:
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error extracting recent documents files: {e}")

    try:
        fullpath = sourceFolder+'/Users/' + username + '/Library/Application Support/com.apple.sharedfilelist/'
        if os.path.isdir(fullpath) == True:
            for file in bf.check_file_in_folder(fullpath):
                if 'com.apple.LSSharedFileList.RecentDocuments' in file:
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error extracting recent documents list files: {e}")

def documentrevisionExtractor(sourceFolder, destinationFolder, username):
    des = destinationFolder + '/documentrevision'
    try:
        fullpath = sourceFolder+'/_.DocumentRevisions-V100/db-V1'
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if 'db.sqlite' in file:
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error - documentRevision:db.sqlite ({e})")

    try:
        fullpath = sourceFolder+'/_.DocumentRevisions-V100/_.cs/ChunkStorage/0/0/0'
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if file == '1':
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error - documentRevision:1 ({e})")

def printerExtractor(sourceFolder, destinationFolder, username):
    des = destinationFolder + '/printer'
    try:
        fullpath = sourceFolder + '/private/var/spool/cups'
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if 'c0001' in file or 'd0001' in file:
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error extracting printer files: {e}")

def webExtractor(sourceFolder, destinationFolder, username):
    des = os.path.join(destinationFolder, 'web')
    try:
        fullpath = os.path.join(sourceFolder, 'Users', username, 'Library', 'Preferences')
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if 'QuarantineEventsV2' in file:
                    bf.file_copy(os.path.join(fullpath, file), des)
    except Exception as e:
        logging.error(f"Error extracting web files: {e}")

def dsstoreExtractor(sourceFolder, destinationFolder, username):
    des = destinationFolder + '/dsstore'
    try:
        for folder in bf.check_file_in_folder(sourceFolder+'/Users/'+username):
            if folder == '.DS_Store':
                os.mkdir(des+'/root')
                bf.file_copy(sourceFolder+'/Users/' + username + '/' + folder, des+'/root')
            elif folder[0] == '.' or folder[0] == '_' or folder == 'Library':
                continue
            else:
                for file in bf.check_file_in_folder(sourceFolder+'/Users/'+username+'/'+folder):
                    if 'DS_Store' in file:
                        os.mkdir(des + '/' + folder)
                        bf.file_copy(sourceFolder+'/Users/'+username+'/'+folder+'/'+file, des + '/' + folder)
    except FileNotFoundError as e:
        logging.error("Error extracting DS_Store files: %s", e)
    except Exception as e:
        logging.error("Unexpected error while extracting DS_Store files: %s", e)

def fseventsdExtractor(sourceFolder, destinationFolder, username):
    des = os.path.join(destinationFolder, 'fseventsd')
    try:
        fullpath = os.path.join(sourceFolder, '_.fseventsd')
        if os.path.isdir(fullpath):
            for file in os.listdir(fullpath):
                bf.file_copy(os.path.join(fullpath, file), des)
    except Exception as e:
        logging.exception(f"Error extracting fseventsd: {e}")

def knowledgeCExtractor(sourceFolder, destinationFolder, username):
    des = destinationFolder + '/knowledgec'
    try:
        fullpath = sourceFolder + '/private/var/db/CoreDuet/Knowledge'
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if 'knowledgeC' in file:
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error extracting knowledgec files: {e}")

def notesExtractor(sourceFolder, destinationFolder, username):
    des = destinationFolder + '/notes'
    try:
        fullpath = sourceFolder+'/Users/' + username + '/Library/Group Containers/group.com.apple.notes'
        if os.path.isdir(fullpath) == True:
            for file in bf.check_file_in_folder(fullpath):
                if 'NoteStore.sqlite' in file or 'NoteStore.sqlite-wal' in file:
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error extracting notes files: {e}")

def icloudExtractor(sourceFolder, destinationFolder, username):
    des = destinationFolder + '/icloud'
    try:
        fullpath = sourceFolder + '/Users/' + username + '/Library/Application Support/CloudDocs/session/db'
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if 'client' in file or 'server' in file:
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error extracting iCloud files: {e}")

def teamsExtractor(sourceFolder, destinationFolder, username):
    des = destinationFolder + '/teams'
    try:
        fullpath = sourceFolder+'/Users/' + username + '/Library/Application Support/Microsoft/Teams/Cache'
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if file[-2:] == '_0':
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error extracting Teams Cache files: {e}")

    try:
        fullpath = sourceFolder+'/Users/' + username + '/Library/Application Support/Microsoft/Teams/IndexedDB/https_teams.live.com_0.indexeddb.leveldb'
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if '.log' in file or '.ldb' in file:
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error extracting Teams leveldb files: {e}")

    try:
        fullpath = sourceFolder+'/Users/' + username + '/Library/Application Support/Microsoft/Teams/Local Storage/leveldb'
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if '.log' in file or '.ldb' in file:
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error extracting Teams local storage files: {e}")

def slackExtractor(sourceFolder, destinationFolder, username):
    des = destinationFolder + '/slack'
    try:
        fullpath = sourceFolder+'/Users/' + username + '/Library/Application Support/Slack/Cache/Cache_Data'
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if file[-2:] == '_0':
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error - slack:random_0: {e}")

    try:
        fullpath = sourceFolder+'/Users/' + username + '/Library/Application Support/Slack/IndexedDB/https_app.slack.com_0.indexeddb.blob/1/00'
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if file == 'a':
                    bf.file_copy(fullpath + '/' + file, des)
    except Exception as e:
        logging.error(f"Error - slack:leveldb: {e}")

def ichatExtractor(source_folder, destination_folder, username):
    des = os.path.join(destination_folder, 'ichat')
    try:
        fullpath = os.path.join(source_folder, 'Users', username, 'Library/Messages')
        if os.path.isdir(fullpath):
            for file in os.listdir(fullpath):
                if 'chat.db' in file:
                    bf.file_copy(os.path.join(fullpath, file), des)
    except Exception as e:
        logging.error("Error extracting chat.db: %s", str(e))

    try:
        fullpath = os.path.join(source_folder, 'Users', username, 'Library/Messages/Archive')
        if os.path.isdir(fullpath):
            for path, dirs, files in os.walk(fullpath):
                for file in files:
                    if '.ichat' in file:
                        bf.file_copy(os.path.join(path, file), des)
    except Exception as e:
        logging.error("Error extracting .ichat files: %s", str(e))

def safariExtractor(sourceFolder, destinationFolder, username):
    des = os.path.join(destinationFolder, 'safari')
    try:
        fullpath = os.path.join(sourceFolder, 'Users', username, 'Library', 'Safari')
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if 'Downloads' in file or 'History.db' in file or 'RecentlyClosedTabs' in file:
                    bf.file_copy(os.path.join(fullpath, file), des)
    except Exception as e:
        logging.error("Error extracting Safari files: %s", str(e))

    try:
        fullpath = os.path.join(sourceFolder, 'Users', username, 'Library', 'Safari', 'Favicon Cache')
        if os.path.isdir(fullpath):
            for file in bf.check_file_in_folder(fullpath):
                if 'favicons.db' in file:
                    bf.file_copy(os.path.join(fullpath, file), des)
    except Exception as e:
        logging.error("Error extracting Safari Favicon Cache: %s", str(e))

def mailExtractor(sourceFolder, destinationFolder, username):
    des = destinationFolder + '/mail'
    '''
    try:
        fullpath = sourceFolder+'/Users/' + username + '/Library/Suggestions/pending'
        if os.path.isdir(fullpath) == True:
            for file in bf.check_file_in_folder(fullpath):
                if file == '1.qdat':
                    bf.file_copy(fullpath + '/' + file, des)
    except:
        logging.error("Error - mail:1qdat")
    '''
    try:
        fullpath = sourceFolder+'/Users/' + username + '/Library/Mail'
        if os.path.isdir(fullpath) == True:
            for (path, dir, files) in os.walk(fullpath):
                for file in files:
                    if 'Envelope Index' in file:
                        bf.file_copy(path + '/' + file, des)
    except:
        logging.error("Error - mail:envelope")

def gmailExtractor(source_folder, destination_folder, username):
    des = os.path.join(destination_folder, 'gmail')
    try:
        fullpath = os.path.join(source_folder, 'Users', username, 'Library', 'Mail')
        if os.path.exists(fullpath):
            for (path, dir, files) in os.walk(fullpath):
                for file in files:
                    if 'partial.emlx' in file:
                        bf.file_copy(os.path.join(path, file), des)
    except Exception as e:
        logging.error(f"An error occurred while extracting gmail files: {e}")