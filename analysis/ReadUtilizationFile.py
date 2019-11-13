import numpy as np
from app.logging import CSVLogger

path_to_write = "volume"
chunkNo = 0  # changed at runtime for tracking of simulation horizon and ticks

def getNpData():
    #path_to_csv = "data/volume_tick.csv"
    path_to_csv = "data/Capacity_Eichstatt.csv"
    #data = np.genfromtxt(path_to_csv, dtype=int, delimiter=',', names=False)
    floatData = []
    with open(path_to_csv, 'r') as util_file:
        utilfiles=util_file.readlines()
    edges = utilfiles.pop(0)
    for rows in range(len(utilfiles)):  
        floatRow = map(lambda i : float(i), [x for x in utilfiles[rows].split(',')])
        floatData.append(floatRow)

    npData = np.array(floatData)
    return (npData, edges)


def aggregateAll():
    """Aggregate all the volume data by summing along the columns"""
    npData, edges = getNpData()
    sumAlongCols = npData.sum(axis=0)
    CSVLogger.logEvent(path_to_write, [edges])
    CSVLogger.logEvent(path_to_write, [sum for sum in sumAlongCols])


def aggregateChunks(num):
    """sum up the chunks of utilizations in capacity or volume files"""
    npData, edges = getNpData()
    sumChunks = np.add.reduceat(npData, range(0, len(npData), num), axis=0)
    CSVLogger.logEvent(path_to_write, [edges])
    for i in range(len(sumChunks)):
        CSVLogger.logEvent(path_to_write, [sum for sum in sumChunks[i]])

def aggregateChunksInMemory(num, chunkNo):
    npData, edges = getNpData()
    sumChunks = np.add.reduceat(npData, range(0, len(npData), num), axis=0)
    edgelist = edges.split(',')
    edgeUtil = {}
    for va in range(len(edgelist)):
        edgeUtil[edgelist[va]] = sumChunks[chunkNo][va]
    return edgeUtil

def aggregateAllCapacities():
    #path_to_csv = "data/volume_tick.csv"
    path_to_csv = [
        "data/MainCapacity1.csv",
        "data/MainCapacity2.csv"
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



#print("aggregating data")
#aggregateChunks(100)
#aggregateAllCapacities()
#chunk =  aggregateChunksInMemory(100, 2)
#print(chunk)