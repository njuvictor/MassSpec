'''
   Read info from CSV
'''

import csv

def ReadfromCSV(infile)
    for row in csv.DictReader(infile, dialect='excel', delimiter='\t'):

