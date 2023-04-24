import wx
import sys
import time

import GazeParser.Configuration
from GazeParser.TrackingTools import getController
from psychopy import visual, event, gui, core

import datetime
import random

CAL_WINDOW_WIDTH  = 1920
CAL_WINDOW_HEIGHT = 1080

time.clock = time.perf_counter

class Logger:
    def __init__(self, name):
        try:
            self.fd = open(name, "w")
        except:
            print(f"failed to open/create file: {name}")
    
    def log(self, item):
        self.fd.write(f"{datetime.datetime.now()}: {item}")
    
    def close(self):
        self.fd.close();


class Controller:
    def __init__(self):
        self.tracker = getController(backend='PsychoPy', configFile='./Config/TrackerSettings.cfg')
        self.logger = Logger(".\controller.log")
        self.logger.log(f"Initialized controller\n")
        self.win = visual.Window(size=(CAL_WINDOW_WIDTH, CAL_WINDOW_HEIGHT),units='pix')
    
    def log(self, name):
        self.logger.log(name)

    def connect(self, ip, _portSend, _portRecv):
        self.log(f"Controller requesting connection to SimpleGazeTracker...\n")
        self.tracker.connect(ip, portSend=_portSend, portRecv=_portRecv)
        time.sleep(0.05)
        self.log(f"Controller connection established\n")

    def calibrate(self):
        calarea = [-400,-300,400,300]
        calTargetPos = [[   0,   0],
                        [-350,-250],[-350,  0],[-350,250],
                        [   0,-250],[   0,  0],[   0,250],
                        [ 350,-250],[ 350,  0],[ 350,250]]
        conf = GazeParser.Configuration.Config("./config/GazeParser-BenQ.cfg")

        self.tracker.setCalibrationScreen(self.win)
        self.tracker.setCalibrationTargetPositions(calarea, calTargetPos)
        self.tracker.openDataFile('datafile.csv', config=conf)

        self.log("starting calibration loop...\n")
        winOpen = True
        while winOpen:
            res = self.tracker.calibrationLoop()
            if res=='q':
                try:
                    self.win.close()
                    winOpen = False
                except:
                    self.log("Calibration loop failed with error\n")
            if self.tracker.isCalibrationFinished():
                self.log("Calibration loop completed successfully\n")
                break
        
    def record(self, numOfTrials):
        self.log(f"Starting recording for {numOfTrials} trials...")
        stim = visual.Rect(self.win, width=10, height=10, units='pix')
        marker = visual.Rect(self.win, width=2, height=2, units='pix', fillColor=(1,1,0),lineWidth=0.1)

        # To Be Removed
        fp = open("dataFileName_local.csv",'w')
        # End of to Be Removed

        trialClock = core.Clock()
        for trial in range(numOfTrials):
            self.log(f"\tStarting trial #{trial}\n")
            error = self.tracker.getSpatialError(message='Press space key')
            
            targetPositionList = [(100*random.randint(-3,3),100*random.randint(-3,3)) for i in range(10)]
            targetPositionList.insert(0,(0,0))
            currentPosition = 0
            previousPosition = 0
            stim.setPos(targetPositionList[currentPosition])
            marker.setPos(targetPositionList[currentPosition])
            
            waitkeypress = True
            while waitkeypress:
                if 'space' in event.getKeys():
                    waitkeypress = False
                
                stim.draw()
                self.win.flip()

            self.tracker.startRecording(message='trial'+str(trial+1))
            self.tracker.sendMessage('STIM %s %s'%targetPositionList[currentPosition])
            
            data = []
            trialClock.reset()
            while True: 
                currentTime = trialClock.getTime()
                currentPosition = int(currentTime)
                if currentPosition>=len(targetPositionList):
                    break
                targetPosition = targetPositionList[currentPosition]
                if previousPosition != currentPosition:
                    self.tracker.sendMessage('STIM %s %s'%targetPosition)
                    previousPosition = currentPosition
                
                preGet = trialClock.getTime()
                eyePos= self.tracker.getEyePosition()
                postGet = trialClock.getTime()
                if not eyePos[0] == None:
                    data.append((1000*preGet,1000*postGet,1000*(postGet-preGet),
                                targetPosition[0],targetPosition[1],eyePos[0],eyePos[1]))
                    marker.setPos((eyePos[0],eyePos[1]))
                else:
                    data.append((1000*preGet,1000*postGet,1000*(postGet-preGet),
                                targetPosition[0],targetPosition[1],-65536,-65536))
                
                keyList = event.getKeys()
                if 'space' in keyList:
                    self.tracker.sendMessage('press space')
                
                stim.setPos(targetPosition)
                stim.draw()
                marker.draw()
                self.win.flip()
                
            self.tracker.stopRecording(message='end trial')
            
            fp.write('trial%d\n' % (trial+1))
            if error[0] != None:
                fp.write('getSpatialError: %.2f,%.2f,%.2f\n' % (error[0],error[-1][0],error[-1][1]))
            else:
                fp.write('getSpatialError: None\n')

            fp.write('SentAt,ReceivedAt,Lag,TargetX,TargetY,EyeX,EyeY\n')

            for d in data:
                fp.write('%.1f,%.1f,%.1f,%d,%d,%.1f,%.1f\n' % d)
            fp.flush()

            self.log(f"\tTrial #{numOfTrials} finished successfully\n")

        self.log("Recording Completed\n")

    def close(self):
        self.tracker.closeDataFile()
        self.logger.close()
        self.log("Controller exits...")
        self.log("Closing controller\n")


controller = Controller()
controller.connect("127.0.0.1", 10003, 10004)
controller.calibrate()
controller.record(1)
controller.close()