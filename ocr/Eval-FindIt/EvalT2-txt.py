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

def jaccard(set1, set2):
    """
        indice de Jaccard : intersection/union
        intersection : tab containing common elements
        union : cardinality of sets - cardinality of intersection
"""
    intersection = []
    for i in set1:
        if i in set2:
            intersection.append(i)
        else:
            pass
    return float(len(intersection)/(len(set1) + len(set2) - len(intersection)))



def evaltask2text(GTfile, candidatefile):
    """
    Function: evaluate the results of training and testing for task 2 text (forgeries localization)
    Input: file of Gound Truth, file of results
    Output: jaccard index with 3 different precisions : line, line + column, line + column + length of token
    """
    fGT = open(GTfile, encoding="utf-8", mode="r")
    xmlGT = fGT.read()
    soupGT = BeautifulSoup(xmlGT, 'xml')
    fcandidat = open(candidatefile, encoding="utf-8", mode="r")
    xmlcand = fcandidat.read()
    soupcand = BeautifulSoup(xmlcand, 'xml')
    
    listfraudlineGT = soupGT.find_all("fraud")
    listfraudlineCand = soupcand.find_all("fraud")
    logger.debug(listfraudlineGT)
    
    """Only lines"""
    listnblineCand = [fraud["line"] for fraud in listfraudlineCand]
    listnblineGT = [fraud["line"] for fraud in listfraudlineGT]
    jacclineresult = jaccard(set(listnblineCand), set(listnblineGT))
    logger.debug(jacclineresult)
    
    #diff = set(listnblineCand) - set(listnblineGT)
    #print(diff)
    """Lines + col"""
    listnbpositionCand = [(fraud["line"], fraud["col"]) for fraud in listfraudlineCand]
    listnbpositionGT = [(fraud["line"], fraud["col"]) for fraud in listfraudlineGT]
    jaccpositionresult = jaccard(set(listnbpositionCand), set(listnbpositionGT))
    logger.debug(jaccpositionresult)
    
    """Lines + col + length of token"""
    listnbtokenCand = [(fraud["line"], fraud["col"], len(fraud["forged_value"])) for fraud in listfraudlineCand]
    listnbtokenGT = [(fraud["line"], fraud["col"], len(fraud["forged_value"])) for fraud in listfraudlineGT]
    jacctokenresult = jaccard(set(listnbtokenCand), set(listnbtokenGT))
    logger.debug(jacctokenresult)

    return jacclineresult, jaccpositionresult, jacctokenresult



def main():
    parser = argparse.ArgumentParser(
        description="Evaluate the spotting of modified informations in a set of document OCR outputs.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-d', '--debug',
        action="store_true",
        help="Activate debug output.") 

    parser.add_argument('-pg', '--pathGT',
        type=str,
        required=True,
        help="path to Groundtruth files")

    parser.add_argument('-pe', '--pathExp',
        type=str,
        required=True,
        help="path to Experimentation files")

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

    if not os.path.isdir(args.pathGT):
        logger.info("output_directory argument is not a valid path")
        sys.exit(1)
    
    logger.info(args.pathGT)

    list_results =[]

    for filename in os.listdir(os.path.join(args.pathGT)):
        dict_results = collections.OrderedDict()
        logger.info(filename)
        dict_results['filename']=str(filename)   
        dict_results['jacclineresult'], dict_results['jaccpositionresult'],dict_results['jacctokenresult']  = evaltask2text(os.path.join(args.pathGT, filename), os.path.join(args.pathExp, filename))
        # logger.info(dict_results)
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
    #----------------------------------------------------------------
    logger.info("Exiting...")
    #----------------------------------------------------------------
    



if __name__ == "__main__":
    main()