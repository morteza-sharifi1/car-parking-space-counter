import numpy as np
import cv2
import cvzone
import pickle


poslist = []

cap = cv2.VideoCapture('park.mp4')


with open('CarParkPos', 'rb') as f:
    poslist = pickle.load(f)


width, height = 50 - 5, 40 - 25

def checkParkSpace(imgPro):
    spaceCounter = 0
    for pos in poslist:
        
        x,y = pos
        # cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 255, 0), 2)
        cv2.imshow('Image', img)
        imgCrop = imgPro[y:y+height, x:x+width]
        cv2.imshow(str(x*y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x,y+height-2), scale=1, thickness=2,
            offset=0, colorR=(0,0,255))

        if count < 500:
            color = (0,255,0)
            thickness = 4
            spaceCounter += 1
        else:
            color = (0,0,255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
    cvzone.putTextRect(img,f'FREE{str(spaceCounter)}/{len(poslist)}', (400,80),  scale=2, thickness=4,
            offset=20, colorR=(0,200,0))


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlue = cv2.GaussianBlur(imgGray, (3,3), 1)
    imgThresh = cv2.adaptiveThreshold(imgBlue, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 25,16)
    imgMedian = cv2.medianBlur(imgThresh, 5)
    kernel = np.zeros((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    
    checkParkSpace(imgDilate)
    


    # cv2.imshow('Image', img)
    # cv2.imshow('ImgBlur', imgBlur)
    # cv2.imshow('ImageThreshold', imgThresh)
    # cv2.imshow('ImgMedian', imgMedian)
    # cv2.imshow('imgDilate', imgDilate)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break