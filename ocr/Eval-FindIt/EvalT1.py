#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-09
# @Author  : Chloé Artaud (chloe.artaud@univ-lr.fr), Nicolas Sidère (nicolas.sidere@univ-lr.fr)
# @Link    : http://findit.univ-lr.fr/
# @Version : $Id$

import os
import logging
import argparse
import csv
import collections
import sys
from argparse import ArgumentTypeError as err
from bs4 import BeautifulSoup
import numpy as np

# ==============================================================================
logger = logging.getLogger(__name__)
# ==============================================================================

def evaltask1(GTfile, candidatefile):
    """
    Function: evaluate the results of training and testing for task 1 (fake documents retrieval)
    Input: file of Gound Truth, file of results
    Output: precision, recall, f-measure
    """
    fGT = open(GTfile, encoding="utf-8", mode="r")
    xmlGT = fGT.read()
    soupGT = BeautifulSoup(xmlGT, 'xml')
    fcandidat = open(candidatefile, encoding="utf-8", mode="r")
    xmlcand = fcandidat.read()
    soupcand = BeautifulSoup(xmlcand, 'xml')
    listdocidGT = soupGT.find_all('doc')
    listdocidCand = soupcand.find_all('doc')
    dicCand = {}
    listResults = []
    for docid in listdocidCand:
        idCand = docid.get("id")
        valCand = docid.get("modified")
        dicCand[idCand] = valCand
    nbtp, nbfp, nbtn, nbfn = 0, 0, 0, 0


    for doc in listdocidGT:
        dicResults = collections.OrderedDict()
        dicResults['ID'] = doc['id']
        if doc['id'] in dicCand:
            if doc['modified']== "1" and dicCand[doc['id']]=="1":
                nbtp +=1
                dicResults['Status'] = 'True Positive'
            elif doc['modified']== "0" and dicCand[doc['id']]=="0":
                nbtn += 1
                dicResults['Status'] = 'True Negative'
            elif doc['modified']== "0" and dicCand[doc['id']]=="1":
                nbfp += 1
                dicResults['Status'] = 'False Positive'
            elif doc['modified']== "1" and dicCand[doc['id']]=="0":
                nbfn += 1
                dicResults['Status'] = 'False Negative'
        else:
            if doc['modified']== "0":
                nbfp += 1
                dicResults['Status'] = 'False Positive'
            elif doc['modified']== "1":
                nbfn += 1
                dicResults['Status'] = 'False Negative'
        

        listResults.append(dicResults)
    precision = nbtp/(nbtp+nbfp)
    recall = nbtp/(nbtp+nbfn)
    if nbtp == 0:
        fmeasure= 0
    else :
        fmeasure = 2*precision*recall/(precision + recall)

    return precision, recall, fmeasure, listResults
    




def main():
    parser = argparse.ArgumentParser(
        description="Evaluate detection of modified/falsified documents in a set of documents.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-d', '--debug',
        action="store_true",
        help="Activate debug output.") 

    parser.add_argument('-fg', '--fileGT',
        type=str,
        required=True,
        help="path to GroundTruth file")

    parser.add_argument('-fe', '--fileExp',
        type=str,
        required=True,
        help="path to Experimentation file")

    parser.add_argument('-o', '--output_file',
        type=str,
        required=True,
        help="path to Output File")
    

    args = parser.parse_args();

    # Logging
    formatter = logging.Formatter("%(name)-12s %(levelname)-7s: %(message)s")
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)
    if args.debug:
        logger.setLevel(logging.DEBUG)

    #----------------------------------------------------------------
    logger.info("Starting up...")
    #----------------------------------------------------------------

    list_results =[]
    list_detailed = []

    dict_results = collections.OrderedDict()
    dict_results['precision'], dict_results['recall'],dict_results['fmeasure'], list_detailed = evaltask1(args.fileGT, args.fileExp)
    list_results.append(dict_results)

    bool_header = True

    with open(args.output_file, 'w', newline='', encoding='utf-8') as csv_file: 
        csvwriter = csv.writer(csv_file)

        for it_result in list_results:
            if bool_header == True:
                header = it_result.keys()
                csvwriter.writerow(header)
                bool_header = False
            csvwriter.writerow(it_result.values())
        bool_header = True

        for it_result in list_detailed:
            if bool_header == True:
                header = it_result.keys()
                csvwriter.writerow(header)
                bool_header = False
            csvwriter.writerow(it_result.values())
    #----------------------------------------------------------------
    logger.info("Exiting...")
    #----------------------------------------------------------------

if __name__ == "__main__":
    main()