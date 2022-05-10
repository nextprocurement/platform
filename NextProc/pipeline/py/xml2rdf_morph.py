#!/usr/bin/python
# -*- coding: utf-8 -*-

#####################################################################################################
# Data ingestion script for the TBFY Knowledge Graph (http://data.tbfy.eu/)
# 
# This file contains a script that runs the RML Mapper on XML files and produces N-triples files.
# 
# Copyright: SINTEF 2018-2021
# Author   : Brian Elvesæter (brian.elvesater@sintef.no)
# License  : Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Project  : Developed as part of the TheyBuyForYou project (https://theybuyforyou.eu/)
# Funding  : TheyBuyForYou has received funding from the European Union's Horizon 2020
#            research and innovation programme under grant agreement No 780247
#####################################################################################################

import config

import tbfy.statistics

import logging

import requests
import json

import os
import shutil
import sys
import getopt

import time
import datetime
from datetime import datetime
from datetime import timedelta

import morph_kgc

# **********
# Statistics
# **********

stats_xml2rdf = tbfy.statistics.xml2rdf_statistics_count.copy()

def write_stats(output_folder):
    global stats_xml2rdf

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    sfile = open(os.path.join(output_folder, 'STATISTICS.TXT'), 'w+')
    for key in stats_xml2rdf.keys():
        sfile.write(str(key) + " = " + str(stats_xml2rdf[key]) + "\n")
    sfile.close()


def reset_stats():
    global stats_xml2rdf

    stats_xml2rdf = tbfy.statistics.xml2rdf_statistics_count.copy()

# *************
# Main function
# *************

def main(argv):
    global stats_xml2rdf

    logging.basicConfig(level=config.logging["level"])
    
    start_date = ""
    end_date = ""
    rml_folder = ""
    input_folder = ""
    output_folder = ""

    try:
        opts, args = getopt.getopt(argv, "hs:e:r:i:o:")
    except getopt.GetoptError:
        print("xml2rdf_morph.py -s <start_date> -e <end_date> -e <end_date> -i <input_folder> -o <output_folder>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("xml2rdf_morph.py -s <start_date> -e <end_date> -e <end_date> -i <input_folder> -o <output_folder>")
            sys.exit()
        elif opt in ("-s"):
            start_date = arg
        elif opt in ("-e"):
            end_date = arg
        elif opt in ("-r"):
            rml_folder = arg
        elif opt in ("-i"):
            input_folder = arg
        elif opt in ("-o"):
            output_folder = arg

    logging.debug("xml2rdf_morph.py: start_date = " + start_date)
    logging.debug("xml2rdf_morph.py: end_date = " + end_date)
    logging.debug("xml2rdf_morph.py: input_folder = " + input_folder)
    logging.debug("xml2rdf_morph.py: output_folder = " + output_folder)

    mapping_filename = config.rml["mapping_filename"]

    logging.debug("xml2rdf_morph.py: mapping_filename = " + mapping_filename)

    start = datetime.strptime(start_date, "%Y-%m-%d")
    stop = datetime.strptime(end_date, "%Y-%m-%d")

    while start <= stop:
        process_start_time = datetime.now()

        created_date = datetime.strftime(start, "%Y-%m-%d")
        dirname = created_date
        dirPath = os.path.join(input_folder, dirname)
        outputDirPath = os.path.join(output_folder, dirname)
        if os.path.isdir(dirPath):
            if not os.path.exists(outputDirPath):
                os.makedirs(outputDirPath)
            for filename in os.listdir(dirPath):
                filePath = os.path.join(dirPath, filename)
                outputFilePath = os.path.join(outputDirPath, str(filename).replace(".xml", ".nt"))
                logging.info("xml2rdf_morph.py: file = " + outputFilePath)

                release_start_time = datetime.now()

                # configuration file
                config_morph = """
                        [DataSourceXML]
                        file_path=""" + dirPath + "/" + filename +"""
                        mappings=""" + rml_folder + "/" + mapping_filename

                logging.debug(config_morph)

                # generate the triples and load them to an RDFlib graph
                graph = morph_kgc.materialize(config_morph)

                graph.serialize(destination=outputFilePath, format='nt')

                release_end_time = datetime.now()
                release_duration_in_seconds = (release_end_time - release_start_time).total_seconds()
                tbfy.statistics.update_stats_add(stats_xml2rdf, "release_files_processed_duration_in_seconds", release_duration_in_seconds)
                tbfy.statistics.update_stats_count(stats_xml2rdf, "number_of_release_files")
                tbfy.statistics.update_stats_count(stats_xml2rdf, "number_of_files")

        process_end_time = datetime.now()
        duration_in_seconds = (process_end_time - process_start_time).total_seconds()
        tbfy.statistics.update_stats_value(stats_xml2rdf, "files_processed_duration_in_seconds", duration_in_seconds)
        write_stats(outputDirPath) # Write statistics
        reset_stats() # Reset statistics for next folder date

        start = start + timedelta(days=1) # Increase date by one day


def xml2rdfAPI(start_date, end_date, input_folder, output_folder):
    global stats_xml2rdf

    rml_folder = "/pipeline/rml-mappings"

    logging.basicConfig(level=config.logging["level"])

    logging.debug("xml2rdf_morph.py: start_date = " + start_date)
    logging.debug("xml2rdf_morph.py: end_date = " + end_date)
    logging.debug("xml2rdf_morph.py: input_folder = " + input_folder)
    logging.debug("xml2rdf_morph.py: output_folder = " + output_folder)

    mapping_filename = config.rml["mapping_filename"]

    logging.debug("xml2rdf_morph.py: mapping_filename = " + mapping_filename)

    start = datetime.strptime(start_date, "%Y-%m-%d")
    stop = datetime.strptime(end_date, "%Y-%m-%d")

    while start <= stop:
        process_start_time = datetime.now()

        created_date = datetime.strftime(start, "%Y-%m-%d")
        dirname = created_date
        dirPath = os.path.join(input_folder, dirname)
        outputDirPath = os.path.join(output_folder, dirname)
        if os.path.isdir(dirPath):
            if not os.path.exists(outputDirPath):
                os.makedirs(outputDirPath)
            for filename in os.listdir(dirPath):
                name, extension = os.path.splitext(filename)
                if (not extension.lower() == ".txt"):
                    filePath = os.path.join(dirPath, filename)
                    outputFilePath = os.path.join(outputDirPath, str(filename).replace(".xml", ".nt"))
                    logging.info("xml2rdf_morph.py: file = " + outputFilePath)

                    release_start_time = datetime.now()

                    # configuration file
                    config_morph = """
                            [DataSourceXML]
                            file_path=""" + dirPath + "/" + filename +"""
                            mappings=""" + rml_folder + "/" + mapping_filename

                    logging.debug(config_morph)

                    # generate the triples and load them to an RDFlib graph
                    graph = morph_kgc.materialize(config_morph)

                    graph.serialize(destination=outputFilePath, format='nt')

                    release_end_time = datetime.now()
                    release_duration_in_seconds = (release_end_time - release_start_time).total_seconds()
                    tbfy.statistics.update_stats_add(stats_xml2rdf, "release_files_processed_duration_in_seconds", release_duration_in_seconds)
                    tbfy.statistics.update_stats_count(stats_xml2rdf, "number_of_release_files")
                    tbfy.statistics.update_stats_count(stats_xml2rdf, "number_of_files")

        process_end_time = datetime.now()
        duration_in_seconds = (process_end_time - process_start_time).total_seconds()
        tbfy.statistics.update_stats_value(stats_xml2rdf, "files_processed_duration_in_seconds", duration_in_seconds)
        write_stats(outputDirPath) # Write statistics
        reset_stats() # Reset statistics for next folder date

        start = start + timedelta(days=1) # Increase date by one day
        return("files_processed_duration_in_seconds", str(duration_in_seconds))




# *****************
# Run main function
# *****************

if __name__ == "__main__": main(sys.argv[1:])
