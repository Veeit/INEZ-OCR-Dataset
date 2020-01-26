# FindIt Evaluation

This project provides tools for evaluating the performance fraud detection methods. 
These tools are used in an academic context during the Fraud Detection Contest held during  ICPR 2018. 
One can find more details here : http://findit.univ-lr.fr

## Tools Provided

The project provides three tools : 
- EvalT1.py evaluate the detection of modified documents among others in a set of documents containing both genuine and modified documents. The evaluation script produces a CSV file with the Precision, Recall and FMeasure results, and, for your information, the ID of each receipt and its status (True Negative, FN, TP, FP).
- EvalT2-img.py evaluates the spotting of one or several modifications in a set of document images. The evaluation script produces a CSV file with, for each receipt, its name and the Jaccard index between the set of pixels covered by your localization results and those of the Groundtruth.
- EvalT2-img.py evaluates the spotting of one or several modifications in a document OCR output (text file). The evaluation script produces a CSV file with, for each receipt, its name, and 3 measures of Jaccard index corresponding to 3 different sets:
    + set of the lines covered by your localization results,
    + set of the lines and column covered by your localization results,
    + set of the lines, column and length of token covered by your localization results.

### Prerequisites

The tools require the use of Python 3.0+ and several libraries.

Workspace setup can be greatly simplified by using "virtualenv" and its 
convenient helper "virtualenvwrapper", but this is not compulsory for the use of provided tools. If so, you can skip this section go directly to Installing

Modern Python installation should provide "pip", the package installation tool 
for Python. If not, install the "python-pip" package.

To install "virtualenv" and "virtualenvwrapper", use:
$ pip install virtualenv 
$ pip install virtualenvwrapper

If necessary, automate the activation of virtualenvwrapper by adding those three lines to your shell startup file (.bashrc, .profile, etc.):
    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/Devel
    source /usr/local/bin/virtualenvwrapper.sh
For Windows and more details, see:
    https://virtualenvwrapper.readthedocs.org/en/latest/install.html

Then, setup and activate a new virtual environment to prevent changing your 
global Python setup:
$ mkvirtualenv findit

### Installing

You're now ready to go.

If necessary, you can  activate your virtual environment using:
$ workon findit

You can now install all the required dependencies:
$ pip install -r requirements.txt

### Usage
Each script have a help option (-h) at the commandline to facilitate their use.

To evaluate the performance of the detection of modified document on a set of documents and produce a summary in a csv file :
  $ python EvalT1.py -fg PATH/TO/GT_FILE.xml -fe PATH/TO/EXPE_FILE.xml -o PATH/TO/OUTPUT_FILE.csv

To evaluate the spotting of modified areas in a set of document images and produce a summary in a csv file :
  $ python EvalT2-img.py -fg PATH/TO/GT/FILES -fe PATH/TO/EXPEFILES -o PATH/TO/OUTPUT_FILE.csv

To evaluate the spotting of modified informations in a set of document OCR outputs and produce a summary in a csv file :
  $ python EvalT2-txt.py -fg PATH/TO/GT/FILES -fe PATH/TO/EXPEFILES -o PATH/TO/OUTPUT_FILE.csv

## Authors
Chloé Artaud (chloe.artaud@univ-lr.fr)
Nicolas Sidère (nicolas.sidere@univ-lr.fr)


