from controller import Controller
from psychopy import visual, event, core
import numpy as np
from matplotlib import pyplot as plt

CAL_WINDOW_WIDTH  = 1200
CAL_WINDOW_HEIGHT = 1000
    
delay = []
init  = []

def wait_for_space():
    waitkeypress = True
    while waitkeypress:
        if 'space' in event.getKeys():
            waitkeypress = False

def run_neuro():
    trialClock = core.Clock()
    controller.tracker.startRecording(message='starting task')
    waitkeypress = True
    while waitkeypress:
        if 'q' in event.getKeys():
            waitkeypress = False

        initTime  = trialClock.getTime()
        eyePos    = controller.tracker.getEyePosition()
        finalTime = trialClock.getTime()
        delay.append(finalTime - initTime)
        init.append(initTime)


    controller.tracker.stopRecording(message='end trial')
    controller.log("Recording Completed\n")
    return delay, init

if __name__ == "__main__":
    controller = Controller()
    controller.connect("127.0.0.1", 10003, 10004)
    controller.calibrate()
    delay, init = run_neuro()
    delay = np.array(delay)
    delay = 1000 * delay
    init = np.array(init)
    init = np.diff(init)
    init = 1 / init
    plt.hist(delay, bins = 100)
    plt.xlabel("delay (ms)")
    plt.title("Delay of Camera")
    plt.figure()
    plt.hist(init, bins = 100)
    plt.xlabel("# of frames")
    plt.title("Camera Frame Rate")
    plt.show()
