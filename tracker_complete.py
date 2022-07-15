from Imports.camera import Camera
from Imports import front_wheels, back_wheels
from Imports import Servo
import picar
from time import sleep
import cv2
import numpy as np
import picar
import os

cam = Camera()
cam.to_position(90,120)
# Show image captured by camera, True to turn on, you will need #DISPLAY and it also slows the speed of tracking

scan_enable         = True
rear_wheels_enable  = True
front_wheels_enable = True
pan_tilt_enable     = True

cv2.startWindowThread()
cap=cv2.VideoCapture(0)
out=cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'MJPG'),15.,(320,240))

SCREEN_WIDTH = 160
SCREEN_HIGHT = 120
cap.set(3,SCREEN_WIDTH)
cap.set(4,SCREEN_HIGHT)
CENTER_X = SCREEN_WIDTH/2
CENTER_Y = SCREEN_HIGHT/2
SIZE_MIN = SCREEN_HIGHT/10
SIZE_MAX = SCREEN_HIGHT/2

#camera follow mode:
#0 = step by step(slow, stable), 
#1 = calculate the step(fast, unstable)
follow_mode = 0

CAMERA_STEP = 2
CAMERA_X_ANGLE = 20
CAMERA_Y_ANGLE = 20

MIDDLE_TOLERANT = 5
PAN_ANGLE_MAX   = 170
PAN_ANGLE_MIN   = 10
TILT_ANGLE_MAX  = 120
TILT_ANGLE_MIN  = 120
FW_ANGLE_MAX    = 90+30
FW_ANGLE_MIN    = 90-30

#scan_pos [pan,tilt]
SCAN_POS = [[90, TILT_ANGLE_MIN], [160, TILT_ANGLE_MIN], [20, TILT_ANGLE_MIN], [125, TILT_ANGLE_MIN], [55, TILT_ANGLE_MIN]]

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
pan_servo = Servo.Servo(1)
tilt_servo = Servo.Servo(2)
picar.setup()

fw.offset = 0
pan_servo.offset = 10
tilt_servo.offset = 0

bw.speed = 0
fw.turn(90)
pan_servo.write(90)
tilt_servo.write(120)

motor_speed = 60




def main():
    pan_angle = 90              # initial angle for pan
    tilt_angle = 120             # initial angle for tilt
    fw_angle = 90
    scan_count = 0
    while True:
        x = 0             # x initial in the middle
        y = 0             # y initial in the middle
        h = 0             # rectangle height initial to 0(no person if h < height)

        for _ in range(10):
            xC,yC,height=tracker()
            print(xC,yC,height)
            
            if h > SIZE_MIN:
                x = xC
                y = yC
                h = height
                break

        print(x, y, h)
        
        # scan:
        if h < SIZE_MIN:
            
            bw.stop()
            if scan_enable:
                #bw.stop()
                pan_angle = SCAN_POS[scan_count][0]
                tilt_angle = SCAN_POS[scan_count][1]
                if pan_tilt_enable:
                    pan_servo.write(pan_angle)
                    tilt_servo.write(tilt_angle)
                scan_count += 1
                if scan_count >= len(SCAN_POS):
                    scan_count = 0
            else:
                sleep(0.1)
            
            pass
        elif h < SIZE_MAX:
            if follow_mode == 0:
                if abs(x - CENTER_X) > MIDDLE_TOLERANT:
                    if x < CENTER_X:                              # Ball is on left
                        pan_angle += CAMERA_STEP
                        #print("Left   ", )
                        if pan_angle > PAN_ANGLE_MAX:
                            pan_angle = PAN_ANGLE_MAX
                    else:                                         # Ball is on right
                        pan_angle -= CAMERA_STEP
                        #print("Right  ",)
                        if pan_angle < PAN_ANGLE_MIN:
                            pan_angle = PAN_ANGLE_MIN
                if abs(y - CENTER_Y) > MIDDLE_TOLERANT:
                    if y < CENTER_Y :                             # Ball is on top
                        tilt_angle += CAMERA_STEP
                        #print("Top    " )
                        if tilt_angle > TILT_ANGLE_MAX:
                            tilt_angle = TILT_ANGLE_MAX
                    else:                                         # Ball is on bottom
                        tilt_angle -= CAMERA_STEP
                        #print("Bottom ")
                        if tilt_angle < TILT_ANGLE_MIN:
                            tilt_angle = TILT_ANGLE_MIN
            else:
                delta_x = CENTER_X - x
                delta_y = CENTER_Y - y
                #print("x = %s, delta_x = %s" % (x, delta_x))
                #print("y = %s, delta_y = %s" % (y, delta_y))
                delta_pan = int(float(CAMERA_X_ANGLE) / SCREEN_WIDTH * delta_x)
                #print("delta_pan = %s" % delta_pan)
                pan_angle += delta_pan
                delta_tilt = int(float(CAMERA_Y_ANGLE) / SCREEN_HIGHT * delta_y)
                #print("delta_tilt = %s" % delta_tilt)
                tilt_angle += delta_tilt

                if pan_angle > PAN_ANGLE_MAX:
                    pan_angle = PAN_ANGLE_MAX
                elif pan_angle < PAN_ANGLE_MIN:
                    pan_angle = PAN_ANGLE_MIN
                if tilt_angle > TILT_ANGLE_MAX:
                    tilt_angle = TILT_ANGLE_MAX
                elif tilt_angle < TILT_ANGLE_MIN:
                    tilt_angle = TILT_ANGLE_MIN
                
            if pan_tilt_enable:
                pan_servo.write(pan_angle)
                tilt_servo.write(tilt_angle)
            sleep(0.01)
            fw_angle = 180 - pan_angle
            if fw_angle < FW_ANGLE_MIN or fw_angle > FW_ANGLE_MAX:
                fw_angle = ((180 - fw_angle) - 90)/2 + 90
                if front_wheels_enable:
                    fw.turn(fw_angle)
                if rear_wheels_enable:
                    bw.speed = motor_speed
                    bw.backward()
            else:
                if front_wheels_enable:
                    fw.turn(fw_angle)
                if rear_wheels_enable:
                    bw.speed = motor_speed
                    bw.forward()
        else:
                    bw.stop()

def tracker():
    # initializa HOG descriptor/person detector (Histograms of Oriented Gradients)
    hog=cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # capture frame by frame
    ret,frame=cap.read()
    print(frame)
    # resize for faster detection
    frame=cv2.resize(frame,(320,240)) # 640,480

    # greyscale for faster detection
    gray=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

    # detect people, returns outline box
    boxes,weights=hog.detectMultiScale(frame,winStride=(8,8))
    print(boxes, weights)
    boxes=np.array([[x,y,x+w,y+h] for (x,y,w,h) in boxes])
    xC=0
    yC=0
    height=0
    for (xA,yA,xB,yB) in boxes:
        # display boxes in picture
        cv2.rectangle(frame,(xA,yA),(xB,yB),(0,255,0),2)
        #find center of rectangle   
        xC=int(xA+((xB-xA)/2))
        yC=int(yA+((yB-yA)/2))
        center=(xC,yC)
        # find height
        height=yB-yA
        print(xC,yC,height)
        #show center of rectangle
        cv2.circle(frame,center,2,(255,255,255),2)
        
            
    # write output video
    out.write(frame.astype('uint8'))

    # display image
    cv2.imshow('frame',frame)

    return xC,yC,height


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        cam.to_position(90,120)
        destroy()