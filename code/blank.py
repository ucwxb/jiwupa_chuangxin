import cv2
import numpy as np
import sys

import time
np.set_printoptions(threshold=sys.maxsize)
cap = cv2.VideoCapture('5.31_blue.avi')
# res_map = np.zeros((1080,1920))  #结果
res_map = np.zeros((480,640))  #结果
index = 0
# first_sum = np.zeros((1080,1920))
first_sum = np.zeros((480,640))
S_sum = 0
# I_sum_map = np.zeros((1080,1920))
I_sum_map = np.zeros((480,640))
start_ = time.time()
while(cap.isOpened()):
    ret, frame = cap.read()
    try:
        img_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  #rgb转灰度
    except:
        break
    # img_gray = np.zeros((frame.shape[0],frame.shape[1]),dtype='uint8')
    # for y_index in range(frame.shape[0]):
    #     for x_index in range(frame.shape[1]):
    #         b = frame[y_index,x_index,0]
    #         g = frame[y_index,x_index,1]
    #         r = frame[y_index,x_index,2]
    #         gray = np.power((np.power(r,2.2) + np.power(1.5*g,2.2) + np.power(0.6*r,2.2))/(1+np.power(1.5,2.2)+np.power(0.6,2.2)),1/2.2)
    #         # gray = np.power((np.power(r,2.2) + np.power(1.5*g,2.2) + np.power(0.6*r,2.2)),1/2.2)
    #         # print(gray-_img_gray[y_index,x_index])
    #         img_gray[y_index,x_index] = gray
    
    img_gray = np.array(img_gray,dtype='float64')  #存灰度图
    img_gray /= 10.0
    res = np.sum(img_gray)
    S_sum += res
    I_sum_map += img_gray
    first_sum += res*img_gray

    index += 1 #帧索引
S_sum *= 1.2
S_sum /= index
I_sum_map /= index
first_sum /= index

res_map = first_sum - S_sum*I_sum_map

min_res_map = np.min(res_map)
max_res_map = np.max(res_map)

res_map -= min_res_map
res_map /= (max_res_map-min_res_map)
res_map *= 25.5
res_map *= 10 #映射

res = np.array(res_map,dtype = np.uint8)
cv2.imwrite("5.31respic/5.31_blue_1.2.jpg",res)
# cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
