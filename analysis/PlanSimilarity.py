import os
import numpy
from scipy.stats import entropy
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import jaccard_similarity_score as jss

from AnalysisGraph import generateGraph

class PlanSimilarity(object):

    filePlans = []

    @classmethod
    def evaluate(cls):
        cls.initializeFile()
        cls._readPlans()

    @classmethod
    def initializeFile(cls):
        if(os.path.exists('analysis/similarity_analysis.csv')):
            os.remove('analysis/similarity_analysis.csv')
            with open('analysis/similarity_analysis.csv', 'a') as summary:
                summary.write('Plan file, plan diff, Entropy, Cosine, Hamming Similarity, Hamming Dist, Euclidean, Jaccard\n')

    @classmethod
    def _readPlans(cls):
        if os.path.exists("datasets/plans"):
            plans_folder = os.listdir("datasets/plans")
            for item in plans_folder:
                if item.endswith(".plans"):
                    with open("datasets/plans/"+item, "r") as planFile:
                        cls.filePlans = []
                        for line in planFile:
                            numPlans = cls.convertToArray(line)
                            cls.filePlans.append(numpy.asarray(numPlans))
                        csvDetail = cls.executePlans(item, cls.filePlans)
                        #write to file
                        with open('analysis/similarity_analysis.csv', 'a') as summary:
                            summary.write(csvDetail + '\n') 
                

    @classmethod
    def executePlans(cls, fileName, plans):
        entropy = cls.calculateEntropy()['similarity']
        cosine = cls.calculateCosineSimilarity()['similarity']
        jaccard = cls.JaccardSimilarity1()['similarity']
        euclidean = cls.calculateEuclideanDistance()['distance']
        hamming = cls.calculateHammingDistance()
        hammingSimilarity = hamming['similarity']
        hammingDist = hamming['distance']
        csv_details = ('%s , s1-s2, %f, %f, %f, %f, %f, %f \n' %(fileName, entropy[0], cosine[0], hammingSimilarity[0], hammingDist[0], euclidean[0], jaccard[0]))
        csv_details += ('%s , s1-s3, %f, %f, %f, %f, %f, %f \n' %(fileName, entropy[1], cosine[1], hammingSimilarity[1], hammingDist[1], euclidean[1], jaccard[0]))
        csv_details += ('%s , s2-s3, %f, %f, %f, %f, %f, %f \n' %(fileName, entropy[2], cosine[2], hammingSimilarity[2], hammingDist[2], euclidean[2], jaccard[0]))
        return csv_details  

    @classmethod
    def convertToArray(cls, planLine):
        planstring = planLine.split(':')[1].replace('\n', '')
        nodesStr = planstring.split(',')
        nodes = map(float, nodesStr)
        return nodes
    
    # print the plans for visualization purpose
    # plan2dArr: 2D numpy array containing plans
    # tipe: type in which elements of array should be typecasted
    @classmethod
    def printPlans(cls, plan2dArr, tipe):
        print('S1: %s' % plan2dArr[0].astype(tipe))
        print('S2: %s' % plan2dArr[1].astype(tipe))
        print('S3: %s' % plan2dArr[2].astype(tipe))


    @classmethod
    def calculateEntropy(cls):
        #cls.printPlans(cls.filePlans, int)
        plan0 = map(lambda x: 0.0001 if x == 0 else x, cls.filePlans[0]);
        plan1 = map(lambda x: 0.0001 if x == 0 else x, cls.filePlans[1]);
        plan2 = map(lambda x: 0.0001 if x == 0 else x, cls.filePlans[2]);
        # print("Entropy")
        # print('---------------------')
        # print('low entropy means low divergence between two distribution')
        # print('Hence more similarity')
        e1 = entropy(plan0, plan1)
        # print("entropy between s1 and s2", e1)
        e2 = entropy(plan0, plan2)
        # print("entropy between s1 and s3", e2)
        e3 = entropy(plan1, plan2)
        # print("entropy between s2 and s3", e3)
        maxE = max(e1, e2, e3)
        minE = min(e1, e2, e3)
        n1 = cls.normalize(e1, maxE, minE)
        n2 = cls.normalize(e2, maxE, minE)
        n3 = cls.normalize(e3, maxE, minE)
        # print("entropy percentage")
        # print('s1-s2| %f%% similar' % ((1 - n1) * 100))
        # print('s1-s3| %f%% similar' % ((1 - n2) * 100))
        # print('s2-s3| %f%% similar' % ((1 - n3) * 100))
        resObj = {
            #"similarity": (((1 - n1) * 100), ((1 - n2) * 100), ((1 - n3) * 100))
            "similarity": (e1,e2,e3)
        }
        return (resObj)


    @classmethod
    def normalize(cls, val, max, min):
        norm = (val - min) / (max - min)
        return norm

    @classmethod
    def calculateEuclideanDistance(cls):
        # cls.printPlans(cls.filePlans, int)
        d1 = euclidean_distances(cls.filePlans[0].reshape(1, -1), cls.filePlans[1].reshape(1,-1))
        d2 = euclidean_distances(cls.filePlans[0].reshape(1, -1), cls.filePlans[2].reshape(1,-1))
        d3 = euclidean_distances(cls.filePlans[1].reshape(1, -1), cls.filePlans[2].reshape(1,-1))
        # print('------------------------------------')
        # print('EUCLIDEAN DISTANCES BETWEEN 3 ARRAYS')
        # print('------------------------------------')
        # print('s1-s2| %f' % d1)
        # print('s1-s3| %f' % d2)
        # print('s2-s3| %f' % d3)
        resObj = {
            "distance": (d1.item(), d2.item(), d3.item())
        }
        return resObj

    @classmethod
    def calculateCosineSimilarity(cls):
        # cls.printPlans(cls.filePlans, int)
        d1 = cosine_similarity(cls.filePlans[0].reshape(1, -1), cls.filePlans[1].reshape(1,-1))
        d2 = cosine_similarity(cls.filePlans[0].reshape(1, -1), cls.filePlans[2].reshape(1,-1))
        d3 = cosine_similarity(cls.filePlans[1].reshape(1, -1), cls.filePlans[2].reshape(1,-1))
        # print('------------------------------------')
        # print('COSINE SIMILARITY BETWEEN 3 ARRAYS')
        # print('------------------------------------')
        # print('Cosine similarity [0-1].')
        # print('1 means two vactors are with same orientation')
        # print('0 means two vaectos are at 90 degrees and have similarity of 0')
        # print('------------------------------------')
        # print('s1-s2| %f' % d1)
        # print('s1-s3| %f' % d2)
        # print('s2-s3| %f' % d3)
        # print('------------------------------------')
        # print('s1-s2| %f%% similar' % (d1 * 100))
        # print('s1-s3| %f%% similar' % (d2 * 100))
        # print('s2-s3| %f%% similar' % (d3 * 100))
        resObj = {
            #"similarity": ((d1.item() * 100),(d2.item() * 100),(d3.item() * 100))
            "similarity": (d1.item(),d2.item(),d3.item())
        }
        return resObj


    @classmethod
    def calculateHammingDistance(cls):    
        # cls.printPlans(cls.filePlans, int)
        d1 = pairwise_distances(cls.filePlans[0].reshape(1, -1), cls.filePlans[1].reshape(1,-1), metric='hamming')
        d2 = pairwise_distances(cls.filePlans[0].reshape(1, -1), cls.filePlans[2].reshape(1,-1), metric='hamming')
        d3 = pairwise_distances(cls.filePlans[1].reshape(1, -1), cls.filePlans[2].reshape(1,-1), metric='hamming')
        maxd = max(d1,d2,d3)
        mind = min(d1,d2,d3)
        n1 = cls.normalize(d1, maxd, mind)
        n2 = cls.normalize(d2, maxd, mind)
        n3 = cls.normalize(d3, maxd, mind)
        # print('------------------------------------')
        # print('PAIRED DISTANCES BETWEEN 3 ARRAYS')
        # print('bitwise matching')
        # print('finds at which position the bits are different')
        # print('1 is maximum distance means string did not match on any position')
        # print('------------------------------------')
        # print('s1-s2| %f, %f%% matched' % (d1,(1-n1)*100) )
        # print('s1-s3| %f, %f%% matched' % (d2,(1-n2)*100) )
        # print('s2-s3| %f, %f%% matched' % (d3,(1-n3)*100) )
        resObj = {
            #"similarity": ( (1-d1)*100, (1-d2)*100, (1-d3)* 100 ),
            "similarity": ( (1-n1)*100, (1-n2)*100, (1-n3)* 100 ),
            "distance": ( d1, d2, d3 )
        }
        return resObj

    @classmethod
    def JaccardSimilarity1(cls):
        s1 = set(cls.filePlans[0])
        s2 = set(cls.filePlans[1])
        s3 = set(cls.filePlans[2])
        d1 = len(s1.intersection(s2)) / len(s1.union(s2))
        d2 = len(s1.intersection(s3)) / len(s1.union(s3))
        d3 = len(s2.intersection(s3)) / len(s2.union(s3))
        resObj = {
            "similarity" : (d1, d2, d3)
        }
        return resObj

    @classmethod
    def JaccardSimilarity(cls):
        # cls.printPlans(cls.filePlans, int)
        d1 = jss(cls.filePlans[0], cls.filePlans[1])
        d2 = jss(cls.filePlans[0], cls.filePlans[2])
        d3 = jss(cls.filePlans[1], cls.filePlans[2])
        # print('------------------------------------')
        # print('JACCARD SIMILARITY BETWEEN 3 ARRAYS')
        # print('------------------------------------')
        # print('Jaccard similarity [0-1].')
        # print('------------------------------------')
        # print('s1-s2| %f' % d1)
        # print('s1-s3| %f' % d2)
        # print('s2-s3| %f' % d3)
        # print('------------------------------------')
        # print('s1-s2| %f%% similar' % (d1 * 100))
        # print('s1-s3| %f%% similar' % (d2 * 100))
        # print('s2-s3| %f%% similar' % (d3 * 100))

PlanSimilarity.evaluate()
#generateGraph(2, "Entropy")
#generateGraph(3, "Cosine Similarity")
#generateGraph(4, 'Hamming Similarity')
#generateGraph(5, 'Hamming Distance')
#generateGraph(6, 'Euclidean Distance')