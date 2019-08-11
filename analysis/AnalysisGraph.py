"""
Histogram demo from
http://docs.astropy.org/en/stable/visualization/histogram.html
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt

def generateGraph(featureIndex, featureLable):
    plotData = processData(featureIndex)
    drawGraph(plotData, featureLable)


# feature index of similarity_analysis.csv i.e which measure to plot (entropy, euclidean, hamming, etc) 
def processData(featureIndex):
    plotData = [[],[],[]]
    featureIndex
    if(os.path.exists('analysis/similarity_analysis.csv')):
        with open('analysis/similarity_analysis.csv', 'r') as summary:
            for line in summary:
                elements = line.split(',')
                if len(elements) > 5:
                    colData = elements[featureIndex]
                    if colData.strip() != 'nan': 
                        if(elements[1].strip() == 's1-s2'):
                            plotData[0].append(float(colData))
                        elif(elements[1].strip() == 's1-s3'):
                            plotData[1].append(float(colData))
                        elif(elements[1].strip() == 's2-s3'):
                            plotData[2].append(float(colData))
    return plotData

def drawGraph(plotData, graphLable):
    #np.random.seed(0)

    n_bins = 10
    #x = np.random.randn(1000, 3) 
    x =  np.array(plotData).transpose()

    #fig, axes = plt.subplots(nrows=2, ncols=2)
    #ax0, ax1, ax2, ax3 = axes.flatten()
    #ax3 = axes.flatten()
    fig, axes = plt.subplots(nrows=1, ncols=1)
    ax0 = axes

    #colors = ['#44000d', '#83142c', '#ad1d45']
    colors = ['#00a898', '#5ebf8c', '#b6d887' ]
    labels = ['s1-s2', 's1-s3', 's2-s3']
    ax0.hist(x, n_bins, normed=1, histtype='bar', color=colors, label=labels)
    ax0.legend(prop={'size': 10})
    ax0.set_title(graphLable)

    fig.tight_layout()
    plt.show()

