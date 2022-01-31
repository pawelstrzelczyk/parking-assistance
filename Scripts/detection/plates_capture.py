import numpy as np
import cv2 as cv
import imutils
import pytesseract
import time


def capture():
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print('could not open capture')
        exit(1)

    for i in range(30):
        ret, frame = cap.read()
        image = imutils.resize(frame, width=500)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        gray = cv.bilateralFilter(gray, 11, 17, 17)
        edged = cv.Canny(gray, 170, 200)

        (cnts, _) = cv.findContours(edged.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:30]

        number_plate_cnt = []
        # loop over contours
        for c in cnts:
            # approximate the contour
            peri = cv.arcLength(c, True)
            approx = cv.approxPolyDP(c, 0.02 * peri, True)
            # if the approximated contour has four points, then assume that screen is found
            if len(approx) == 4:
                number_plate_cnt = approx
                break

        # mask the part other than the number plate
        mask = np.zeros(gray.shape, np.uint8)
        if len(number_plate_cnt) == 4:
            cv.drawContours(mask, [number_plate_cnt], 0, 255, -1)

        # cv.imshow('new_image', new_image)
        new_image = cv.bitwise_and(image, image, mask=mask)

        alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        options = "-c tessedit_char_whitelist={}".format(alphanumeric)
        options += " --psm {}".format(7)

        # run tesseract OCR on image
        text = pytesseract.image_to_string(new_image, config=options)
        text = text.strip()

        # cv.imshow('frame', frame)
        time.sleep(0.3)
        if len(text) == 7:
            cap.release()

            return text
        else:
            return ""
