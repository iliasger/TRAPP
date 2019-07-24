import os
import numpy
from sklearn.metrics.pairwise import manhattan_distances

class PlanSimilarity(object):
    @classmethod
    def evaluate(cls):
        cls._readPlans()

    @classmethod
    def _readPlans(cls):
        if os.path.exists("datasets/plans"):
            plans_folder = os.listdir("datasets/plans")
            for item in plans_folder:
                if item.endswith(".plans"):
                    with open("datasets/plans/"+item, "r") as planFile:
                        filePlans = []
                        for line in planFile:
                            numPlans = cls.convertToArray(line)
                            filePlans.append(numPlans)
                        cls.executePlans(line, filePlans)

    @classmethod
    def executePlans(cls, fileName, plans):
        #cls.logAverage(fileName, plans)
        cls.logManhattanDistance(fileName, plans)


    @classmethod
    def logAverage(cls,filename, filePlans):
        averages = []
        for planline in filePlans:
            avg = cls.getAverage(planline)
            averages.append(avg)
        print(filename, averages)

    @classmethod
    def logManhattanDistance(cls, filename, plans):
        dist = manhattan_distances(numpy.reshape(plans[0], (-1, 1)), numpy.reshape(plans[1], (-1, 1)))
        print(filename, dist)

    @classmethod
    def convertToArray(cls, planLine):
        planstring = planLine.split(':')[1].replace('\n', '')
        nodesStr = planstring.split(',')
        nodes = map(float, nodesStr)
        return nodes

    @classmethod
    def getAverage(cls, plan):
        #plan = cls.convertToArray(planLine)
        summ = sum(plan)
        avg = summ/len(plan)
        return avg