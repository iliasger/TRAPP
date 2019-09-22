import numpy as np
from numpy import genfromtxt
from numpy import median
import csv

filePaths = [
    'results/baseline_overheads/seed1/overheads_800.csv',
    'results/baseline_overheads/seed2/overheads_800.csv',
    'results/baseline_overheads/seed3/overheads_800.csv',
    'results/baseline_overheads/seed4/overheads_800.csv',
    'results/baseline_overheads/seed5/overheads_800.csv',
    'results/baseline_overheads/seed6/overheads_800.csv',
    'results/baseline_overheads/seed7/overheads_800.csv',
    'results/baseline_overheads/seed8/overheads_800.csv',
    'results/baseline_overheads/seed9/overheads_800.csv',
    'results/baseline_overheads/seed10/overheads_800.csv'
]

overheadFiles = [
    genfromtxt(filePaths[0], delimiter=','),
    genfromtxt(filePaths[1], delimiter=','),
    genfromtxt(filePaths[2], delimiter=','),
    genfromtxt(filePaths[3], delimiter=','),
    genfromtxt(filePaths[4], delimiter=','),
    genfromtxt(filePaths[5], delimiter=','),
    genfromtxt(filePaths[6], delimiter=','),
    genfromtxt(filePaths[7], delimiter=','),
    genfromtxt(filePaths[8], delimiter=','),
    genfromtxt(filePaths[9], delimiter=',')
]

lengths = [
    len(overheadFiles[0]),
    len(overheadFiles[1]),
    len(overheadFiles[2]),
    len(overheadFiles[3]),
    len(overheadFiles[4]),
    len(overheadFiles[5]),
    len(overheadFiles[6]),
    len(overheadFiles[7]),
    len(overheadFiles[8]),
    len(overheadFiles[9])
    ]

def getMinIndex(arr):
    minIndex = 0
    minNo = 9999
    for i in range(len(arr)):
        if(arr[i]<minNo):
            minNo = arr[i]
            minIndex = i   
    return minIndex

def Average(lst): 
    return sum(lst) / len(lst) 

def writeLine(row):
    try:
        pathFile = 'results/baseline_overheads/overheads_800.csv'
        with open(pathFile, 'ab') as mycsvfile:
            writer = csv.writer(mycsvfile, dialect='excel')
            writer.writerow(row)
    except Exception as e:
        print(e)
        pass


print(lengths)
smallIndex = getMinIndex(lengths)
smallestCsvLength = lengths[smallIndex]

with open(filePaths[smallIndex], 'r') as f:
    writeData = list(csv.reader(f, delimiter=","))
    #data[0][0].split(',')

for j in range(smallestCsvLength):
    avgOverhead = Average([
        overheadFiles[0][j][6],
        overheadFiles[1][j][6],
        overheadFiles[2][j][6],
        overheadFiles[3][j][6],
        overheadFiles[4][j][6],
        overheadFiles[5][j][6],
        overheadFiles[6][j][6],
        overheadFiles[7][j][6],
        overheadFiles[8][j][6],
        overheadFiles[9][j][6]
        ])
    print(avgOverhead)
    csvEl = writeData[j]
    csvEl[6] = str(avgOverhead)
    writeLine(csvEl)