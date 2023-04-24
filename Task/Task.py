from controller import Controller
from psychopy import visual, event, core
import numpy as np
import glob

CAL_WINDOW_WIDTH  = 1200
CAL_WINDOW_HEIGHT = 1000

 
# paths_of_images = ['1/', '2/', '3/']
paths_of_images = ['4/', '6/'] 
# paths_of_images = ['6/'] 

def eval_distance(point1, point2):  
    diff = np.array(point1) - np.array(point2) 
    return np.linalg.norm(diff)

def wait_for_space(): 
    waitkeypress = True
    while waitkeypress: 
        if 'space' in event.getKeys(): 
            waitkeypress = False

    
def run_neuro(): 
    startMessage    = visual.TextStim     (controller.win, alignHoriz = 'left', pos = (-150, -150), height = 20, text = 'Please press space for first trial', units = 'pix')
    continueMessage = visual.TextStim      (controller.win, alignHoriz = 'left', pos = (-150, -150), height = 20, text = 'Please press space for next trial', units = 'pix')
    alarmMessage    = visual.TextStim     (controller.win, alignHoriz = 'left', pos = (-150, -150), height = 30, text = 'Read the word loudly', units = 'pix', color = 'red')

    trialClock = core.Clock()

    controller.tracker.startRecording(message='starting task')

    controller.win.flip()
    startMessage.draw()
    controller.win.flip()
    wait_for_space()
    numOfPath = 1
    for path in paths_of_images:
        controller.log(f"\tPath of Image: #{numOfPath+1}\n")
        images = glob.glob(path + "*.png")
        numOfImage = 1
        controller.win.flip()
        for image in images:
            controller.log(f"\tImage of Path: #{numOfImage+1}\n")
            controller.tracker.sendMessage(message='Start Image Name in Path= ' + image)
            imageStimulus = visual.ImageStim(controller.win, image = image, pos = [0,0])  
            resetTimer = True
            waitkeypress = True
            imageStimulus.draw()
            while waitkeypress:
                if 'space' in event.getKeys():
                    waitkeypress = False
                    numOfImage += 1
                    
            controller.tracker.sendMessage(message='End Image Name in Path= ' + image)
            controller.win.flip()
            wait_for_space()
                    
                    
        numOfPath += 1
    controller.tracker.stopRecording(message='end trial')
    controller.log("Recording Completed\n")

if __name__ == "__main__":
    controller = Controller()
    controller.connect("127.0.0.1", 10003, 10004)
    controller.calibrate()
    run_neuro()
    core.quit()