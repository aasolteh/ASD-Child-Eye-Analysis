import GazeParser
import os
from GazeParser import Graphics
import matplotlib.pyplot as pyplot
import numpy

def plotScatter(data):
    # if isinstance(data, GazeParser.GazeData):
    #     xy = data.getFixCenter()
    #     dur = data.getFixDur()
    # else:
    #     xy = numpy.zeros((2, len(data)))
    #     dur = numpy.zeros(len(data))
    #     for i in range(len(data)):
    #         xy[i, :] = data[i].center
    #         dur[i] = data[i].duration
    xy = data
    dur = len(data)
    pyplot.plot(xy[:, 0], xy[:, 1], 'k-')
    for idx in range(xy.shape[0]):
        pyplot.text(xy[idx, 0], xy[idx, 1], str(idx+1))
    pyplot.scatter(xy[:, 0], xy[:, 1], s=dur, c=dur, alpha=0.7)

dataPath   = "../Data/"
auSubject  = "Amir Parham"
nauSubject = "Koroush BahadorKhani"
auPath     = dataPath + auSubject + '/'
nauPath    = dataPath + nauSubject + '/'

auData, a = GazeParser.load(auPath + 'datafile_4.db')
nauData, b = GazeParser.load(nauPath + 'datafile_46.db')

newData = auData
print(type(newData))
start = nauData[0].getMsgTime(12)
end = nauData[0].getMsgTime(13)
Graphics.quickPlot(nauData[0], period=(start, end), style='XY')
pyplot.show()
# plotScatter(y)
# pyplot.show()
# Graphics.drawScatterPlot(newData[0])
# pyplot.show()