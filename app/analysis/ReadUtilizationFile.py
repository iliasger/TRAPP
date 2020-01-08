import numpy as np
from app.logging import CSVLogger

"""
    NOTE : This class is for the purpose of running standalone.
    `UtilizationCapacity.py` is the file which a copy of this file
    that is integrated in TRAPP.
"""
class UtilizationCapacity(object):

    path_to_write = "volume"
    chunkNo = 0  # changed at runtime for tracking of simulation horizon and ticks
    currentUtilSpan = {}

    @classmethod
    def getNpData(cls):
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

    @classmethod
    def getNpDataCustom(cls, pathToCsv):
        """ This method is the copy of getNpData except that
            it takes the file path from the argument
         """
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
        volPath = 'data/a1-b0/volume.csv'
        utlPath = 'streets'
        capacity, edges = cls.getNpData()
        volume = cls.getNpDataCustom(volPath)[0]
        utilization = np.divide(volume, capacity, out=np.zeros_like(volume), where=capacity!=0)
        CSVLogger.logEvent(utlPath, [edges])
        for i in range(len(utilization)):
            CSVLogger.logEvent(utlPath, [sum for sum in utilization[i]])
        print("aggregated")

    @classmethod
    def evaluateUtilization(cls):
        """ This method evaluate the street utilization by summing 
        volume file along y axis and then dividing by capacity along y axis
        street utilization = volume/capacity
        """
        npData, edges = cls.getNpData()
        totalCapacity = npData.sum(axis=0)
        npVolume, edges = cls.getNpDataCustom("data/volume.csv")
        totalVolume =  npVolume.sum(axis=0)
        streetUtilization = np.divide(totalVolume, totalCapacity, out=np.zeros_like(totalVolume), where=totalCapacity!=0)
        CSVLogger.logEvent("streetUtilization", [edges])
        CSVLogger.logEvent("streetUtilization", [sum for sum in streetUtilization])        




UtilizationCapacity.evaluateUtilization()
#UtilizationCapacity.utilizationFromVolumeCapacity()
    #print("aggregating data")
    #aggregateChunks(100)
    #aggregateAllCapacities()
    #chunk =  aggregateSpanInMemory(100, 2)
    #print(chunk)