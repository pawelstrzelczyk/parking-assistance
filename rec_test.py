import numpy as np
import cv2 as cv
import imutils
import sys
import pytesseract
import time


cap = cv.VideoCapture(0)

if not cap.isOpened():
    print('could not open capture')
    exit(1)

while True:
    ret, frame = cap.read()
    image = imutils.resize(frame, width=500)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.bilateralFilter(gray, 11, 17, 17)
    edged = cv.Canny(gray, 170, 200)
    
    
    
    (cnts, _) = cv.findContours(edged.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    cnts=sorted(cnts, key = cv.contourArea, reverse = True)[:30]
    
    NumberPlateCnt = None
    count = 0
    # loop over contours
    for c in cnts:
        # approximate the contour
        peri = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.02 * peri, True)
        # if the approximated contour has four points, then assume that screen is found
        if len(approx) == 4:  
            NumberPlateCnt = approx 
            break

    # mask the part other than the number plate
    mask = np.zeros(gray.shape,np.uint8)
    if len(NumberPlateCnt) == 4:
        new_image = cv.drawContours(mask,[NumberPlateCnt],0,255,-1)
    
    #cv.imshow('new_image', new_image)
    new_image = cv.bitwise_and(image,image,mask=mask)
    
    
    
    config = ('-l eng --oem 1 --psm 3')

    print('image processed')
    # run tesseract OCR on image
    text = pytesseract.image_to_string(new_image, config=config)


    #cv.imshow('frame', frame)
    
    print(text)
    time.sleep(0.3)    
    if cv.waitKey(1) == ord('q'):
        break

    
cap.release()
cv.destroyAllWindows
