#!/usr/bin/python
# -*- coding: utf-8 -*-

#####################################################################################################
# Parquet file preparation and RML rule application from the nextProcurement project
# 
# This file prepares the parquet file so RML rules can be applied, and then applies them. 
# Code from the TBFY is reused.
# 
# Author   : mnavas (UPM)
# License  : Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Project  : Developed as part of the nextProcurement project
# Funding  : nextProcurement has received funding from the European Union
#####################################################################################################

import config
import tbfy.json_utils
import tbfy.statistics

import logging

import os
import sys
import getopt

import time
import datetime
from datetime import datetime
from datetime import timedelta

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import datetime
from rdflib.plugin import register, Serializer, Parser
import morph_kgc
from filesplit.split import Split


# **********
# Statistics
# **********

stats_files = tbfy.statistics.files_statistics_count.copy()

def write_stats(output_folder):
    global stats_files

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    sfile = open(os.path.join(output_folder, 'STATISTICS.TXT'), 'w+')
    for key in stats_files.keys():
        sfile.write(str(key) + " = " + str(stats_files[key]) + "\n")
    sfile.close()


def reset_stats():
    global stats_files

    stats_files = tbfy.statistics.files_statistics_count.copy()


# *************
# Main function
# *************

def main(argv):
    global stats_files

    logging.basicConfig(level=config.logging["level"])
    
    input_folder = ""
    output_folder = ""
    rml = ""

    try:
        opts, args = getopt.getopt(argv, "hs:e:r:i:o:")
    except getopt.GetoptError:
        print("applyRules.py -i <input_folder> -o <output_folder> -r <rule_file_path>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("applyRules.py -i <input_folder> -o <output_folder> -r <rule_file_path>")
            sys.exit()
        elif opt in ("-i"):
            dirPath = arg
        elif opt in ("-o"):
            outputDirPath = arg
        elif opt in ("-r"):
            rml = arg

    logging.debug("applyRules.py: input_folder = " + dirPath)
    logging.debug("applyRules.py: output_folder = " + outputDirPath)
    logging.debug("applyRules.py: rule_file_path = " + rml)
    logging.debug("applyRules.py: CurrentDir = " + os.getcwd())
    
    process_start_time = datetime.datetime.now()
        
    # Functionality Starts
    if os.path.isdir(dirPath):
        if not os.path.exists(outputDirPath):
            os.makedirs(outputDirPath)
        for filename in os.listdir(dirPath):
            inputFilePath = os.path.join(dirPath, filename)
            ext = os.path.splitext(inputFilePath)[-1].lower()
            if (ext == ".parquet"):
                output_filename = os.path.splitext(filename)[0] + '_output.parquet'
                outputFilePath = os.path.join(outputDirPath, output_filename)
                output_filename2 = os.path.splitext(filename)[0] + '.nt'
                outputFilePath2 = os.path.join(outputDirPath, output_filename2)
                logging.info("applyRules.py: file = " + outputFilePath)
                logging.info("applyRules.py: file = " + outputFilePath2)
                    
                prepareAndApply(inputFilePath, outputFilePath, outputFilePath2, rml, outputDirPath)
                                        
                tbfy.statistics.update_stats_count(stats_files, "number_of_files")

    process_end_time = datetime.datetime.now()
    duration_in_seconds = (process_end_time - process_start_time).total_seconds()
    tbfy.statistics.update_stats_value(stats_files, "files_processed_duration_in_seconds", duration_in_seconds)
    write_stats(outputDirPath) # Write statistics
    reset_stats() # Reset statistics for next folder date


def processingAPI(dirPath, outputDirPath, rml):
    global stats_files

    logging.basicConfig(level=config.logging["level"])
    
    logging.debug("applyRules.py: input_folder = " + dirPath)
    logging.debug("applyRules.py: output_folder = " + outputDirPath)
    logging.debug("applyRules.py: rule_file_path = " + rml)
    logging.debug("applyRules.py: CurrentDir = " + os.path.abspath(os.getcwd()))

    process_start_time = datetime.datetime.now()
     
    
    # Functionality Starts
    if os.path.isdir(dirPath):
        if not os.path.exists(outputDirPath):
            os.makedirs(outputDirPath)
        for filename in os.listdir(dirPath):
            inputFilePath = os.path.join(dirPath, filename)
            ext = os.path.splitext(inputFilePath)[-1].lower()
            if (ext == ".parquet"):
                output_filename = os.path.splitext(filename)[0] + '_output.parquet'
                outputFilePath = os.path.join(outputDirPath, output_filename)
                output_filename2 = os.path.splitext(filename)[0] + '.nt'
                outputFilePath2 = os.path.join(outputDirPath, output_filename2)
                logging.info("applyRules.py: file = " + outputFilePath)
                logging.info("applyRules.py: file = " + outputFilePath2)
                    
                prepareAndApply(inputFilePath, outputFilePath, outputFilePath2, rml, outputDirPath)
                                        
                tbfy.statistics.update_stats_count(stats_files, "number_of_files")

    process_end_time = datetime.datetime.now()
    duration_in_seconds = (process_end_time - process_start_time).total_seconds()
    tbfy.statistics.update_stats_value(stats_files, "files_processed_duration_in_seconds", duration_in_seconds)
        
    write_stats(outputDirPath) # Write statistics
    reset_stats() # Reset statistics for next folder date

    return("files_processed_duration_in_seconds" + str(duration_in_seconds))


def prepareAndApply(input, output, output_nt, rml, outputDirPath):
    # We preprocess the data
    df = pd.read_parquet(input, engine='pyarrow')
    
    logging.info("applyRules.py: parquet file read")
    
    # Tipo de Contrato
    tipos_contrato = {1: 'goods' , 2: 'services' , 3:'works' , 21: 'services' , 31:'works'}
    df["Tipo de Contrato"] = df["Tipo de Contrato"].map(tipos_contrato)

    logging.info("applyRules.py: prepare and apply type contract")
    
    def datetimeNone(x,y):
        try:
            if(type(y)==str):
                z = x + 'T' + y
                d = datetime.datetime.strptime(z, '%Y-%m-%dT%H:%M:%S')
                return d + '.000000+01:00'
            else:
                z = x + 'T00:00:00'
                d = datetime.datetime.strptime(z, '%Y-%m-%dT%H:%M:%S')
                return d + '.000000+01:00'
        except (TypeError, ValueError):
            return '1111-11-11T11:11:11.111111+01:00'
        
    df["Presentación de Solicitudes (Fecha)"] = df.apply(lambda x: datetimeNone(x["Presentación de Solicitudes (Fecha)"],["Presentación de Solicitudes (Hora)"]), axis=1)

    df['Plazo de Ejecución (Duración)'] = df['Plazo de Ejecución (Duración)'].astype(int)
    df['Tipo de Procedimiento'] = df['Tipo de Procedimiento'].astype(int)
    df['Número de Licitadores Participantes'] = df['Número de Licitadores Participantes'].astype(int)
    
    
    logging.info("applyRules.py: prepare and apply date")
    # Estado
    # estado = {'ANUL': "cancelled" , 2: 'services' , 3:'works' , 21: 'services' , 31:'works'}
    # df["Estado"] = df["Estado"].map(estado)
    # print(df["Estado"].unique())

    # Resultado
    # resultado = {'ANUL': "cancelled" , 2: 'services' , 3:'works' , 21: 'services' , 31:'works'}
    # df["Resultado"] = df["Estado"].map(resultado)
    # print(df["Resultado"].unique())



    #print(df["Tipo de Contrato"])
    #print(df["Tipo de Contrato"].unique())


    table = pa.Table.from_pandas(df)
    pq.write_table(table, output)
    
    applyRules(output, output_nt, rml)
    
    # We split the nt file, that can be large
    LINES_PER_FILE = 10000 
    Split(output_nt, outputDirPath).bylinecount(LINES_PER_FILE)
    logging.info("applyRules.py: file = " + output + " correctly split")
    
    # We delete the two intermediate files
    os.remove(output_nt)
    logging.info("applyRules.py: file = " + output_nt + " correctly deleted")
    os.remove(output)
    logging.info("applyRules.py: file = " + output + " correctly deleted")



def applyRules(input, output, rml):
    print(os.getcwd())
    # configuration file
    config_morph = """
                                [DataSource1]
                                file_path=""" + input + """
                                mappings=""" + rml

    print(config_morph)
    # generate the triples and load them to an RDFlib graph
    graph = morph_kgc.materialize(config_morph)
    # work with the graph
    graph.serialize(destination=output, format='nt')  
    

# *****************
# Run main function
# *****************

if __name__ == "__main__": main(sys.argv[1:])









