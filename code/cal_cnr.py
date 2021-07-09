import cv2
import numpy as np
import sys

import time

xyxy = [[]]
img = cv2.imread("")
img = np.array(img,dtype='float64')  #存灰度图
suop=0,objsum=0
sklp=0,gbsum=0
for i in range(xyxy[0][0],xyxy[0][1]):
    for j in range(xyxy[1][0],xyxy[1][1]):
        if img[i,j]>255/2:
            suop=suop+img[i,j]
            objsum=objsum+1
        else:
             sklp=sklp+img[i,j]
             gbsum=gbsum+1
gobj=suop/objsum
gb=sklp/gbsum
nes=0,dnes=0

for i in range(xyxy[0][0],xyxy[0][1]):
    for j in range(xyxy[1][0],xyxy[1][1]):
        if img[i,j]>255/2:
            nes=nes+(img[i,j]-gobj)^2
        else:
            dnes=dnes+(img[i,j]-gb)^2
nesp=nes/objsum
pdnes=dnes/gbsum
cnr=(gobj-gb)/np.sqrt(nesp^2+pdnes^2)
visibility=(gobj-gb)/(gobj+gb)
print("cnr:",cnr,"vis",visibility)
