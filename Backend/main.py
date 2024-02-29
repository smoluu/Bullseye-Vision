from websocket import *
from Classes import *
import configparser
import calibrate

#Load config
config = configparser.ConfigParser()
config.read("backend/config.ini")

calibrate.startCalibration()
#Start Websocket server
#asyncio.run(startWSS())