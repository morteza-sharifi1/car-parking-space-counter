

import cv2
import pickle


width, height = (50-5),(40-25)

poslist = []

try:
    with open('CarParkPos', 'rb') as f:
        poslist = pickle.load(f)
except:
    poslist = []

def mouseClick(events,x,y,flags,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        poslist.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(poslist):
            x1,y1 = pos
            if x1<x<x1+width and y1<y<y1+height:
                poslist.pop(i)

with open('CarParkPos', 'wb') as f:
    pickle.dump(poslist, f)


while True:
    img = cv2.imread('carparkImg.png')
    cv2.rectangle(img, (5,25), (50,40), (255,255,0),2)

    for pos in poslist:
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255,255,0),2)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', mouseClick)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()








