import numpy as np
from app.logging import CSVLogger

#path_to_csv = "data/volume_tick.csv"
path_to_csv = "data/capacity1_3000cars_800tiks.csv"
path_to_write = "volume"
#data = np.genfromtxt(path_to_csv, dtype=int, delimiter=',', names=False)

edges = []
floatData = []
with open(path_to_csv, 'r') as util_file:
    utilfiles=util_file.readlines()
edges = utilfiles.pop(0)
for rows in range(len(utilfiles)):  
    floatRow = map(lambda i : float(i), [x for x in utilfiles[rows].split(',')])
    floatData.append(floatRow)

npData = np.array(floatData)

def aggregateAll():
    """Aggregate all the volume data by summing along the columns"""
    sumAlongCols = npData.sum(axis=0)
    CSVLogger.logEvent(path_to_write, [edges])
    CSVLogger.logEvent(path_to_write, [sum for sum in sumAlongCols])


def aggregateChunks(num):
    """sum up the chunks of utilizations in capacity or volume files"""
    sumChunks = np.add.reduceat(npData, range(0, len(npData), num), axis=0)
    CSVLogger.logEvent(path_to_write, [edges])
    for i in range(len(sumChunks)):
        CSVLogger.logEvent(path_to_write, [sum for sum in sumChunks[i]])


def aggregateAllCapacities():
    #path_to_csv = "data/volume_tick.csv"
    path_to_csv = [
        "data/capacity1_3000cars_800tiks.csv",
        "data/capacity2_3000cars_800tiks.csv",
        "data/capacity3_3000cars_800tiks.csv"
        ]
    path_to_write = "MainCapacity"
    aggregatedData = []
    for findex in range(len(path_to_csv)):
        edges = []
        floatData = []
        with open(path_to_csv[findex], 'r') as util_file:
            utilfiles=util_file.readlines()
        edges = utilfiles.pop(0)
        for rows in range(len(utilfiles)):  
            floatRow = map(lambda i : float(i), [x for x in utilfiles[rows].split(',')])
            floatData.append(floatRow)

        npData = np.array(floatData)
        if len(aggregatedData) == 0:
            aggregatedData = npData
        else:
            aggregatedData = np.maximum(aggregatedData, npData)

    CSVLogger.logEvent(path_to_write, [edges])
    for i in range(len(aggregatedData)):
        CSVLogger.logEvent(path_to_write, [sum for sum in aggregatedData[i]])



print("aggregating data")
#aggregateChunks(100)
aggregateAllCapacities()