#!/usr/bin/python
# -*- coding: utf-8 -*-

#####################################################################################################
# Data ingestion script for the nextProcurement project, based on code from TBFY
# 
# This file contains a script that publishes nt files to the triplestore database.
# 
# Author   : mnavas (UPM) [based on a script by Brian Elvesæter (brian.elvesater@sintef.no)]
# License  : Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Project  : Developed as part of the nextProcurement project
# Funding  : nextProcurement has received funding from the European Union
#####################################################################################################

import config

import tbfy.statistics

import logging

import requests
import json

import os
import sys
import getopt

import time
import datetime
from datetime import datetime
from datetime import timedelta
from requests.auth import HTTPDigestAuth


# **********
# Statistics
# **********

stats_publish = tbfy.statistics.publish_statistics_count.copy()

def write_stats(output_folder):
    global stats_publish

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    sfile = open(os.path.join(output_folder, 'STATISTICS_PUBLISH.TXT'), 'w+')
    for key in stats_publish.keys():
        sfile.write(str(key) + " = " + str(stats_publish[key]) + "\n")
    sfile.close()


def reset_stats():
    global stats_publish

    stats_publish = tbfy.statistics.publish_statistics_count.copy()


# ****************
# Global variables
# ****************

virtuoso_url = os.getenv("VIRTUOSO_URL") or config.virtuoso["virtuoso_url"]
virtuoso_dataset = os.getenv("VIRTUOSO_DATASET") or config.virtuoso["dataset"]
virtuoso_user = os.getenv("VIRTUOSO_USER") or config.virtuoso["virtuoso_user"]
virtuoso_pass = os.getenv("VIRTUOSO_PASS") or config.virtuoso["virtuoso_pass"]


# ***************************
# Read RDF data from RDF file
# ***************************

def read_rdf_data(rdf_file):
    rdf_contents = open(rdf_file, encoding='utf-8').read()
    return rdf_contents.encode('utf-8')
    

def number_of_triples(rdf_file):
    no_triples = 0
    with open(rdf_file, encoding='utf-8') as f:
        for line in f:
            no_triples += 1
    return no_triples


# ****************************************
# Publish RDF data to triplestore database
# ****************************************
def publish_rdf(rdf_data):
    url = virtuoso_url + "/sparql-graph-crud-auth?graph-uri=" + virtuoso_url +"/" + virtuoso_dataset

    body = rdf_data    

    auth = HTTPDigestAuth(virtuoso_user, virtuoso_pass) 

    headers = {
        "Content-Type": "text/turtle;charset=utf-8"
    }

    timeout = 150
    tries = 3
    for i in range(tries):
        try:
            response = requests.post(url, data=body, auth=auth, headers=headers, timeout=timeout)
            requests.session().close()
            #response.connection.close()
            if response.status_code != 201 and response.status_code != 200:
                logging.info("publish_rdf(): ERROR: " + str(response))
                return None
            else:
                return response
        except requests.Timeout:
            logging.info("publish_rdf(): timeout exception in request POST. Trying again")
            if i < tries - 1: # i is zero indexed
                continue
            else:
                logging.info("publish_rdf(): ERROR in request POST. Timeout tries endend.")
                return None
        except:
            logging.info("publish_rdf(): ERROR in request POST")
            return None


# *************
# Main function
# *************

def main(argv):
    global stats_publish

    logging.basicConfig(level=config.logging["level"])
    
    input_folder = ""

    try:
        opts, args = getopt.getopt(argv, "hs:e:i:")
    except getopt.GetoptError:
        print("publish_rdf.py -i <input_folder>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("publish_rdf.py -i <input_folder>")
            sys.exit()
        elif opt in ("-i"):
            input_folder = arg

    # input_folder = "../../out"
    
    logging.debug("publish_rdf.py: input_folder = " + input_folder)
    
    process_start_time = datetime.now()
        
    rdf_data = b''

    logging.info("publish_rdf.py: " + input_folder + " reading")

    if os.path.isdir(input_folder):
        for filename in os.listdir(input_folder):
            filePath = os.path.join(input_folder, filename)
            ext = os.path.splitext(filePath)[-1].lower()
            if (ext == ".nt"):
                logging.info("publish_rdf.py: " + filename + " reading")
                rdf_data = rdf_data + read_rdf_data(filePath)
                    
                # Update statistics
                tbfy.statistics.update_stats_count(stats_publish, "number_of_files")
                tbfy.statistics.update_stats_add(stats_publish, "number_of_triples", number_of_triples(filePath))

    logging.info("publish_rdf.py: " + input_folder + " publishing")
    
    publish_rdf(rdf_data)

    process_end_time = datetime.now()
    duration_in_seconds = (process_end_time - process_start_time).total_seconds()
    tbfy.statistics.update_stats_value(stats_publish, "publish_duration_in_seconds", duration_in_seconds)
    logging.info(str(stats_publish))
    write_stats(input_folder) # Write statistics
    reset_stats() # Reset statistics for next folder date


def publish_rdfAPI(input_folder):
    global stats_publish

    logging.basicConfig(level=config.logging["level"])

    logging.debug("publish_rdf.py: input_folder = " + input_folder)

    process_start_time = datetime.now()
    rdf_data = b''

    if os.path.isdir(input_folder):
        for filename in os.listdir(input_folder):
            filePath = os.path.join(input_folder, filename)
            ext = os.path.splitext(filePath)[-1].lower()
            if (ext == ".nt"):
                logging.info("publish_rdf.py: " + filename + " reading")
                rdf_data = rdf_data + read_rdf_data(filePath)
                    
                # Update statistics
                tbfy.statistics.update_stats_count(stats_publish, "number_of_files")
                tbfy.statistics.update_stats_add(stats_publish, "number_of_triples", number_of_triples(filePath))

    logging.info("publish_rdf.py: " + input_folder)

    publish_rdf(rdf_data)

    process_end_time = datetime.now()
    duration_in_seconds = (process_end_time - process_start_time).total_seconds()
    tbfy.statistics.update_stats_value(stats_publish, "publish_duration_in_seconds", duration_in_seconds)
    write_stats(input_folder) # Write statistics
    reset_stats() # Reset statistics for next folder date

    return("publish_duration_in_seconds", str(duration_in_seconds))


def publish_rdfAPI_noDate(input_folder):
    global stats_publish

    logging.basicConfig(level=config.logging["level"])

    logging.debug("publish_rdf.py: input_folder = " + input_folder)

    process_start_time = datetime.now()

    dirPath = input_folder
    
    rdf_data = b''

    if os.path.isdir(dirPath):
        for filename in os.listdir(dirPath):
            filePath = os.path.join(dirPath, filename)
            ext = os.path.splitext(filePath)[-1].lower()
            if (ext == ".nt"):
                logging.info("publish_rdf.py: " + filename + " reading")
                rdf_data = rdf_data + read_rdf_data(filePath)
                
                # Update statistics
                tbfy.statistics.update_stats_count(stats_publish, "number_of_files")
                tbfy.statistics.update_stats_add(stats_publish, "number_of_triples", number_of_triples(filePath))

            logging.info("publish_rdf.py: " + filename)

            publish_rdf(rdf_data)

    process_end_time = datetime.now()
    duration_in_seconds = (process_end_time - process_start_time).total_seconds()
    tbfy.statistics.update_stats_value(stats_publish, "publish_duration_in_seconds", duration_in_seconds)
    write_stats(dirPath) # Write statistics
    reset_stats() # Reset statistics for next folder date

    return("publish_duration_in_seconds", str(duration_in_seconds))

# *****************
# Run main function
# *****************

if __name__ == "__main__": main(sys.argv[1:])
