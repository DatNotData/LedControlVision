import cv2 as cv
import numpy as np

def nothing(x=0):
    pass

cam = cv.VideoCapture(0)

set_win = 'settings'

cv.namedWindow(set_win)

cv.createTrackbar('h_min',set_win,0,255,nothing)
cv.createTrackbar('h_max',set_win,0,255,nothing)
cv.createTrackbar('s_min',set_win,0,255,nothing)
cv.createTrackbar('s_max',set_win,0,255,nothing)
cv.createTrackbar('v_min',set_win,0,255,nothing)
cv.createTrackbar('v_max',set_win,0,255,nothing)

hsv_min = np.array([0,0,0])
hsv_max = np.array([255,255,255])

def update_hsv():
    hsv_min[0] = cv.getTrackbarPos('h_min',set_win)
    hsv_min[1] = cv.getTrackbarPos('s_min',set_win)
    hsv_min[2] = cv.getTrackbarPos('v_min',set_win)
    
    hsv_max[0] = cv.getTrackbarPos('h_max',set_win)
    hsv_max[1] = cv.getTrackbarPos('s_max',set_win)
    hsv_max[2] = cv.getTrackbarPos('v_max',set_win)

def settings_load():
    settings_file = open('settings.txt','r')
    data = settings_file.read().split(',')

    data = [int(data[i]) for i in range(6)]

    cv.setTrackbarPos('h_min',set_win, data[0])
    cv.setTrackbarPos('s_min',set_win, data[1])
    cv.setTrackbarPos('v_min',set_win, data[2])
    
    cv.setTrackbarPos('h_max',set_win, data[3])
    cv.setTrackbarPos('s_max',set_win, data[4])
    cv.setTrackbarPos('v_max',set_win, data[5])

    settings_file.close()


def settings_save():
    settings_file = open('settings.txt','w')
    for i in hsv_min:
        settings_file.write(str(i)+',')
    for i in hsv_max:
        settings_file.write(str(i)+',')
    settings_file.close()

def get_target(binary):
    edged = cv.bilateralFilter(binary, 11, 17, 17)
    edged = cv.Canny(edged, 30, 200)
    image, cnts, _= cv.findContours(edged.copy(),
                                    cv.RETR_TREE,
                                    cv.CHAIN_APPROX_SIMPLE)
    
    try:
        cnts = sorted(cnts, key = cv.contourArea, reverse = True)
        
        num = [0,0];
        total = 0

        for cnt in cnts[0]:
            for i in cnt:
                num[0] += i[0]
                num[1] += i[1]
                total+=1

        ret = [int(i/total) for i in num]
        return(ret[0], ret[1])
 
    except:
        return (None, None)

def value_in_range(value, minimum, maximum):
    if value < minimum:
        value = minimum

    if value > maximum:
        value = maximum

    return value

def send_data(x):
    f = open('buffer.txt','w')
    f.write(str(x))
    f.close()

# start of main

settings_load()

found = False # if target is found
start = (0,0) # innitial position of cursor when found
value = 0 # some value that we are going to adjust
temp = 0 # temporary place to store value

while True:
    update_hsv()
    settings_save()

    ret, img = cam.read()
    
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    binary = cv.inRange(hsv, hsv_min, hsv_max)
    binary = cv.erode(binary, None, iterations=10)
    binary = cv.dilate(binary, None, iterations=10)


    center = get_target(binary)

    if center[0] != None and center[1] != None:
        cv.circle(img,center,10,(0,255,255),thickness=-2,lineType=8,shift=0)

        value = temp + (start[1] - center[1]) / 2

        if found == False:
            found = True
            start = center
            
    else:
        found = False
        temp = value

    value = value_in_range(value, 0, 255)

    print(value)
    send_data(value)
    
    cv.imshow('image', img)
    cv.imshow('binary', binary)

    
    cv.waitKey(1)

