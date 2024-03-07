from websocket import *
from Classes import *
import configparser
import calibrate

#Load config
config = configparser.ConfigParser()
config.read("Backend/config.ini")

#calibration
calibrate.startCalibration()

#Start Websocket server
#asyncio.run(startWSS())