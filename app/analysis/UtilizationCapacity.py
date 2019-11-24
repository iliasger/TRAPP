import numpy as np
from app.logging import CSVLogger


class UtilizationCapacity(object):

    path_to_write = "volume"
    path_to_csv = "data/Capacity_Eichstatt.csv"
    chunkNo = 0  # changed at runtime for tracking of simulation horizon and ticks
    currentUtilSpan = {}

    @classmethod
    def getNpData(cls):
        #path_to_csv = "data/volume_tick.csv"
        path_to_csv = cls.path_to_csv
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

    @classmethod
    def getNpDataPath(cls, pathToCsv):
        #path_to_csv = "data/volume_tick.csv"
        path_to_csv = pathToCsv
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


    @classmethod
    def aggregateAll(cls):
        """Aggregate all the volume data by summing along the columns"""
        npData, edges = cls.getNpData()
        sumAlongCols = npData.sum(axis=0)
        CSVLogger.logEvent(cls.path_to_write, [edges])
        CSVLogger.logEvent(cls.path_to_write, [sum for sum in sumAlongCols])

    @classmethod
    def aggregateChunks(cls, num):
        """sum up the chunks of utilizations in capacity or volume files"""
        npData, edges = cls.getNpData()
        sumChunks = np.add.reduceat(npData, range(0, len(npData), num), axis=0)
        CSVLogger.logEvent(cls.path_to_write, [edges])
        for i in range(len(sumChunks)):
            CSVLogger.logEvent(cls.path_to_write, [sum for sum in sumChunks[i]])

    @classmethod
    def aggregateSpanInMemory(cls, num, chunkNo):
        cls.chunkNo = chunkNo
        npData, edges = cls.getNpData()
        sumChunks = np.add.reduceat(npData, range(0, len(npData), num), axis=0)
        edgelist = edges.split(',')
        edgeUtil = {}
        for va in range(len(edgelist)):
            edgeUtil[edgelist[va]] = sumChunks[chunkNo][va]
        cls.currentUtilSpan = edgeUtil
        return edgeUtil

    @classmethod
    def getAggregateSpanFromMemory(cls):
        return cls.currentUtilSpan

    @classmethod
    def aggregateAllCapacities(cls):
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

    @classmethod
    def utilizationFromVolumeCapacity(cls):
        capacity = cls.getNpData()
        volume = cls.getNpDataPath('data/a1-b0/volume.csv')
        print("helloworld")


    #print("aggregating data")
    #aggregateChunks(100)
    #aggregateAllCapacities()
    #chunk =  aggregateSpanInMemory(100, 2)
    #print(chunk)