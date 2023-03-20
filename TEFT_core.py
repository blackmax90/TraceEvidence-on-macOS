import os
import getpass
import shutil
import csv
import logging
from tqdm import tqdm

import Modules.Basic.basic_functions as bf
import Modules.ExtractionConnector as ec
import Modules.AnalyzerConnector as ac
import Modules.TEFT_Display as tdi
from Modules.TEFT_Define import *

logger = logging.getLogger(__name__)

class TEFT_Core():

    TRACE_EVIDENCE_LIST = ['spotlight', 'msoffice', 'googledrive', 'diagonositc', 'recentfiles', 'documentrevision',
                              'printer', 'web', 'dsstore', 'fseventsd', 'knowledgec', 'notes', 'icloud', 'teams',
                              'slack', 'ichat', 'safari', 'mail', 'gmail']

    def __init__(self):
        self.trace_file_list = []
        self.data_for_output = []
        self.username = ''

    def run(self):
        logger.info("Starting TEFTCore")
        tdi.run_tool()
        input_type = tdi.select_input()  # 1: Live #2: Dead (Image) #3: Directory

        # Live forensics
        if input_type == '1':
            self.trace_file_list = []
            self.data_for_output = []
            ex_file_list = []
            all_file_list = []

            self.username = getpass.getuser()

            # Create temp folders
            destination_folder = f'extractedFiles - {self.username}'
            for trace_evi in self.TRACE_EVIDENCE_LIST:
                bf.temp_folder_creation(f'{destination_folder}/{trace_evi}')

            # Extract trace evidence files
            self.trace_evidence_extraction('', destination_folder, self.username)

            # Extract trace file information
            ex_file_list = self.trace_evidence_parser(destination_folder)

            # Extract all files (except Library folder)
            all_file_list = self.file_extraction('', self.username)

            # Compare the files
            self.data_for_output = self.file_comparison(set(ex_file_list), set(all_file_list))

            # Print Output
            self.print_output(self.username, self.data_for_output)

        # Input Directory
        elif input_type == '3':

            # Get input folder
            source_folder = tdi.type_source_path()
            # Get username
            account_typed = tdi.type_user_name(source_folder)

            # Unknown user account or All user account
            if account_typed == 'x':

                # Search all user account
                account_list = bf.check_file_in_folder(f'{source_folder}/Users')
                for account in account_list:
                    if account[0] != '.' and account[0] != '_' and account != 'Shared':
                        try:
                            self.username = account

                            # Initialization
                            self.trace_file_list = []
                            self.data_for_output = []
                            ex_file_list = []
                            all_file_list = []

                            # Create temp folders
                            destination_folder = f'extractedFiles - {self.username}'
                            for trace_evi in self.TRACE_EVIDENCE_LIST:
                                bf.temp_folder_creation(f'{destination_folder}/{trace_evi}')

                            # Extract trace evidence files
                            self.trace_evidence_extraction(source_folder, destination_folder, self.username)

                            # Extract trace file information
                            ex_file_list = self.trace_evidence_parser(destination_folder)

                            # Extract all files (except Library folder)
                            all_file_list = self.file_extraction(source_folder, self.username)

                            # Compare the files
                            self.data_for_output = self.file_comparison(set(ex_file_list), set(all_file_list))

                            # Print Output
                            self.print_output(self.username, self.data_for_output)

                        except:
                            continue

            # User account selected
            else:
                self.trace_file_list = []
                self.data_for_output = []
                ex_file_list = []
                all_file_list = []

                self.username = account_typed

                # Create temp folders
                destination_folder = f'extractedFiles - {self.username}'
                for trace_evi in self.TRACE_EVIDENCE_LIST:
                    bf.temp_folder_creation(f'{destination_folder}/{trace_evi}')

                # Extract trace evidence files
                self.trace_evidence_extraction(source_folder, destination_folder, self.username)

                # Extract trace file information
                ex_file_list = self.trace_evidence_parser(destination_folder)

                # Extract all files (except Library folder)
                all_file_list = self.file_extraction(source_folder, self.username)

                # Compare the files
                self.data_for_output = self.file_comparison(set(ex_file_list), set(all_file_list))

                # Print Output
                self.print_output(self.username, self.data_for_output)

        else:
            logger.error("Invalid input type")

        logger.info("TEFTCore completed")

    def trace_evidence_extraction(self, source_folder, destination_folder, username):
        ec.spotlightExtractor(source_folder, destination_folder, username)
        ec.msofficeExtractor(source_folder, destination_folder, username)
        ec.googledriveExtractor(source_folder, destination_folder, username)
        ec.diagnosticExtractor(source_folder, destination_folder, username)
        ec.recentfileExtractor(source_folder, destination_folder, username)
        ec.documentrevisionExtractor(source_folder, destination_folder, username)
        ec.printerExtractor(source_folder, destination_folder, username)
        ec.webExtractor(source_folder, destination_folder, username)
        ec.dsstoreExtractor(source_folder, destination_folder, username)
        ec.fseventsdExtractor(source_folder, destination_folder, username)
        ec.knowledgeCExtractor(source_folder, destination_folder, username)
        ec.notesExtractor(source_folder, destination_folder, username)
        ec.icloudExtractor(source_folder, destination_folder, username)
        ec.teamsExtractor(source_folder, destination_folder, username)
        ec.slackExtractor(source_folder, destination_folder, username)
        ec.ichatExtractor(source_folder, destination_folder, username)
        ec.safariExtractor(source_folder, destination_folder, username)
        ec.mailExtractor(source_folder, destination_folder, username)
        ec.gmailExtractor(source_folder, destination_folder, username)

        logger.info("Trace evidence extraction completed")

    def trace_evidence_parser(self, path_dir):
        temp_list = [] # Initialize
        final_list = []
        temp_list.append(ac.msofficeParser(path_dir+'/msoffice'))
        temp_list.append(ac.googledriveParser(path_dir+'/googledrive'))
        temp_list.append(ac.spotlightParser(path_dir+'/spotlight'))
        temp_list.append(ac.knowledgeCParser(path_dir+'/knowledgec'))
        temp_list.append(ac.iCloudParser(path_dir+'/icloud'))
        temp_list.append(ac.teamsParser(path_dir+'/teams'))
        temp_list.append(ac.mailParser(path_dir+'/mail'))
        temp_list.append(ac.recentfilesParser(path_dir+'/recentfiles'))

        for i in temp_list:
            for j in i:
                final_list.append(j)

        logger.info("Trace evidence analysis completed")
        return(final_list)

    def file_extraction(self, source_folder, username):
        fullpath = f'{source_folder}/Users/{username}'
        all_file_list = []
        for (path, dirs, files) in os.walk(fullpath):
            dirs[:] = [dir for dir in dirs if dir != 'Library']
            for file in tqdm(files, desc='Extracting files'):
                if '.docx' in file or '.xlsx' in file or '.pptx' in file:
                    all_file_list.append(file)

        logger.info("File listing completed")
        return all_file_list

    def file_comparison(self, trace_file_list, all_file_list):
        result_file_list = []
        for trace_file in trace_file_list:
            count = 0
            for exist_file in all_file_list:
                if trace_file.name == exist_file.split('.')[0]:
                    count = 1
                    break
            if count == 0:
                result_file_list.append(trace_file)

        logger.info("File comparison completed")
        return result_file_list

    def print_output(self, username, data_for_output):
        des = f'Result/{username}'
        bf.temp_folder_creation(des)
        with open(f'{des}/result.csv', 'w', newline='') as f:
            wr = csv.writer(f)
            wr.writerow(
                ['Filename', 'Extension', 'Filepath', 'Accessed Timestamp', 'Modified Timestamp', 'Filesize', 'Type',
                 'Source'])
            for i in range(0, len(data_for_output)):
                if data_for_output[i].name != '':
                    wr.writerow(
                        [data_for_output[i].name, data_for_output[i].ext, data_for_output[i].path,
                         data_for_output[i].a_timestamp, data_for_output[i].m_timestamp, data_for_output[i].size,
                         data_for_output[i].type, data_for_output[i].source])

        logger.info("Output printed to CSV file")

if __name__ == '__main__':
    mj = TEFT_Core()
    mj.run()
    print(colored("\n\n--- Completed", 'blue'))

