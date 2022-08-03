import requests
import glob
import os
import getopt
import sys
import logging

from datetime import datetime


def main(argv):

    input_folder = ""
    api_dir = ""

    try:
        opts, args = getopt.getopt(argv, "hi:a:")
    except getopt.GetoptError:
        print("pipeline.py -i <input_folder> -a <api-dir>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("pipeline.py -i <input_folder> -a <api-dir>")
            sys.exit()
        elif opt in ("-i"):
            input_folder = arg
        elif opt in ("-a"):
            api_dir = arg

    logging.debug("pipeline.py: input_folder = " + input_folder)
    logging.debug("pipeline.py: api_dir = " + api_dir)

    api_dir = 'http://localhost:5050'

    #filepath = "D:/Documentos/TBFY_data/TBFY_DATA_DUMP_JSON/3_JSON_Enriched/2019-01-01/*.parquet"
    filepath = input_folder

    #param = 'input_07-06-2022'
    param = 'input_' + datetime.today().strftime("%d-%m-%Y-%H:%M:%S")

    logging.info('Starting pipeline')

    files = []
    for file in glob.glob(filepath):
        filename = os.path.basename(file)
        files.append(('upload_files', (filename, open(file, 'rb'))))
        
    logging.info('a total of ' + len(files) + ' files were detected')

    response = requests.post(api_dir + '/pipeline/{item_id}?destination=%2F' + param, files=files)

    print(response)