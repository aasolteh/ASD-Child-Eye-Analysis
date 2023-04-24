import numpy as np
from GazeParser import Converter
import os

os.chdir(r"../Data")

subDicts = {
    "names" : ["Koroush BahadorKhani", "Amir Parham"],
    "autism" : [False, True]
}

auGroup  = []
nauGroup = []
names    = list(subDicts.keys())[0]
aus      = list(subDicts.keys())[1]

for _ in range(len(subDicts[names])):
    if subDicts[aus][_] == True:
        auGroup.append(subDicts[names][_])
    else:
        nauGroup.append(subDicts[names][_])

auSubject  = auGroup[0]
nauSubject = nauGroup[0]

auPath  = os.getcwd() + '/' + auSubject
nauPath = os.getcwd() + '/' + nauSubject

auSentenceData = os.listdir(auPath)[1]
nauSentenceData = os.listdir(nauPath)[1]

Converter.TrackerToGazeParser(auPath + '/' + auSentenceData)
Converter.TrackerToGazeParser(nauPath + '/' + nauSentenceData)