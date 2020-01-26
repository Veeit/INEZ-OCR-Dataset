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

def jaccard(arr1, arr2):
    """
        Jaccard Index : intersection/union
    """
    set1 = set(tuple(i) for i in arr1)
    set2 = set(tuple(i) for i in arr2)
    intersection=set.intersection(set1, set2)
    logger.debug(len(intersection))
    logger.debug(len(set1))
    logger.debug(len(set2))
    return float(len(intersection)/(len(set1) + len(set2) - len(intersection)))



def evaltask2img(GTfile, candidatefile):
    """
    Function: evaluate the results of training and testing for task 2 img (forgeries localization)
    Input: file of Gound Truth, file of results
    Output: Jaccard Index
    """
    fGT = open(GTfile, encoding="utf-8", mode="r")
    xmlGT = fGT.read()
    soupGT = BeautifulSoup(xmlGT, 'xml')
    fcandidat = open(candidatefile, encoding="utf-8", mode="r")
    xmlcand = fcandidat.read()
    soupcand = BeautifulSoup(xmlcand, 'xml')
    
    listfraudlineGT = soupGT.find_all("fraud")
    listfraudlineCand = soupcand.find_all("fraud")
    arrGT=[]
    arrCand=[]

    for fraudlineGT in listfraudlineGT:
        GTx1 = int(fraudlineGT.get("x"))
        GTy1 = int(fraudlineGT.get("y"))
        GTx2 = int(fraudlineGT.get("width")) + GTx1
        GTy2 = int(fraudlineGT.get("height")) + GTy1 
        for ix in range(GTx1, GTx2):
            for iy in range(GTy1, GTy2):
                arrGT.append([ix, iy])

        
    for fraudlineCand in listfraudlineCand:
        Candx1 = int(fraudlineCand.get("x"))
        Candy1 = int(fraudlineCand.get("y"))
        Candx2 = int(fraudlineCand.get("width")) + Candx1
        Candy2 = int(fraudlineCand.get("height")) + Candy1 
        for ix in range(Candx1, Candx2):
            for iy in range(Candy1, Candy2):
                arrCand.append([ix, iy])

    
    result = jaccard(np.array(arrGT), np.array(arrCand)) 

    return result



def main():
    parser = argparse.ArgumentParser(
        description="Evaluate the spotting of modified areas in a set of document images.",
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
        dict_results['score'] = evaltask2img(os.path.join(args.pathGT, filename), os.path.join(args.pathExp, filename))
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