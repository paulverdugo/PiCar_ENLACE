import numpy as np
import cv2


# initializa HOG descriptor/person detector (Histograms of Oriented Gradients)
hog=cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# open webcam videostream
cap=cv2.VideoCapture(0)

out=cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'MJPG'),15.,(320,240))

while True:
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
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
out.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
