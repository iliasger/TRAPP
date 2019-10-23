import numpy as np
from app.logging import CSVLogger

path_to_csv = "data/volume_tick.csv"
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
sumAlongCols = npData.sum(axis=0)

CSVLogger.logEvent("volume", [edges])
CSVLogger.logEvent("volume", [sum for sum in sumAlongCols])
