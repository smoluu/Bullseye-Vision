
import cv2
import numpy as np
import time
import requests

device = 1

#camera_URL = "https://192.168.0.25:6969/video"
URL = "http://192.168.0.101"
AWB = False
cap = cv2.VideoCapture(URL + ":81/stream")
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
#camera_width = 800
#camera_height = 600
#empty_img = np.zeros((camera_height,camera_width,3), dtype=np.uint8)

def set_resolution(url: str, index: int=1, verbose: bool=False):
    try:
        if verbose:
            resolutions = "10: UXGA(1600x1200)\n9: SXGA(1280x1024)\n8: XGA(1024x768)\n7: SVGA(800x600)\n6: VGA(640x480)\n5: CIF(400x296)\n4: QVGA(320x240)\n3: HQVGA(240x176)\n0: QQVGA(160x120)"
            print("available resolutions\n{}".format(resolutions))

        if index in [10, 9, 8, 7, 6, 5, 4, 3, 0]:
            requests.get(url + "/control?var=framesize&val={}".format(index))
        else:
            print("Wrong index")
    except:
        print("SET_RESOLUTION: something went wrong")

def set_quality(url: str, value: int=1, verbose: bool=False):
    try:
        if value >= 10 and value <=63:
            requests.get(url + "/control?var=quality&val={}".format(value))
    except:
        print("SET_QUALITY: something went wrong")

def set_quality(url: str, value: int=1, verbose: bool=False):
    try:
        if value >= 10 and value <=63:
            requests.get(url + "/control?var=quality&val={}".format(value))
    except:
        print("SET_QUALITY: something went wrong")
        
def set_awb(url: str, awb: int=1):
    try:
        requests.get(url + "/control?var=awb&val={}".format(1 if awb else 0))
    except:
        print("SET_QUALITY: something went wrong")
    return awb

#create window
cv2.namedWindow("Preview", cv2.WINDOW_NORMAL)

#create trackbars
thresh_blockSize = 255
thresh_c = 60
def nothing(x):
	pass
cv2.createTrackbar("thresh_blockSize", "Preview", thresh_blockSize, 255, nothing )
cv2.createTrackbar("thresh_c", "Preview", thresh_c, 255, nothing)

if __name__ == '__main__':
      
	
	set_resolution(URL, index=10)
	requests.get(URL + "/control?var=awb&val={}".format(1 if AWB else 0))

	if cap.isOpened():
		while (True):

			try:
				ret, frame_r = cap.read()
			except:
				print(Exception)

			#frame_r = cv2.imread("C:/Repos/Bullseye-Vision/Backend/frame1.jpg", cv2.IMREAD_COLOR)
			frame_l = cv2.flip(frame_r,1)

			# resize image

			#frame_r = cv2.resize(frame_r, (camera_width,camera_height))

			#grayscale image

			#gray = cv2.cvtColor(frame_r, cv2.COLOR_BGR2GRAY)
			#gray_3_channel = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

			# image thresholding

			#get trackbar value
			#thresh_blockSize = max(3,cv2.getTrackbarPos("thresh_blockSize", "Preview"))
			#thresh_c = cv2.getTrackbarPos("thresh_c","Preview")
			#convert to odd number
			#thresh_blockSize = thresh_blockSize if thresh_blockSize % 2 != 0 else thresh_blockSize + 1

			#thresh  = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
			#							 cv2.THRESH_BINARY_INV, thresh_blockSize, thresh_c)
			#convert to 3 channel for debug window
			#thresh_3_channel = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)


			#detect circles

			#	circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,20,
		    #	                        param1=50,param2=30,minRadius=0,maxRadius=0)
			#	for i in circles[0,:]:
		    #		# draw the outer circle
			#		cv2.circle(gray_3_channel,(i[0],i[1]),i[2],(0,255,0),2)
		    #		# draw the center of the circle
			#		cv2.circle(gray_3_channel,(i[0],i[1]),2,(0,0,255),3)

			#cancattenate debug images to 1 image
			#	numpy_horizontal_concat_0 = np.concatenate((frame_l,frame_r,thresh_3_channel), axis=1)
			#	numpy_horizontal_concat_1 = np.concatenate((gray_3_channel,empty_img,empty_img), axis=1)
			#	image = np.concatenate((numpy_horizontal_concat_0,numpy_horizontal_concat_1,), axis=0)

			#show images in window
			cv2.imshow('Preview', frame_r)

			key = cv2.waitKey(1)
               
			if key & 0xFF == ord('q'):
				break
                  
			elif key == ord('r'):
				idx = int(input("Select resolution index: "))
				set_resolution(URL, index=idx, verbose=True)
              
			elif key == ord('w'):
                
				val = int(input("Set quality (10 - 63): "))
				set_quality(URL, value=val)
                    
			time.sleep(0.1)  #set update rate
	else:
		print("Error: Could not open file: %s" % (URL))

      


cap.release()
cv2.destroyAllWindows()
