import time
import RPi.GPIO as GPIO
#from picamera import PiCamera
import os
import sys

if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))
    #camera=PiCamera()
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.IN)
    while True:
        motion_input=GPIO.input(11)
        if True: #motion_input == 1:
            path = root+"/Recorded_Videos/" + str(time.time()).replace(".", "_") + ".h264"
            # camera.start_recording(path)
            # camera.wait_recording(3)
            # camera.stop_recording()
            cmd = "raspivid -o " + path + " -t 5000"
            os.system(cmd)
            #sys.exit()
