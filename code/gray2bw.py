import cv2
pic = cv2.imread("5.30respic_eng/black_1.jpg")
_,res = cv2.threshold(pic, 255/2, 255,cv2.THRESH_BINARY)
cv2.imshow("win",res)
cv2.waitKey(0)
# cv2.imwrite("./new_1_bw.jpg",res)
# dst = cv2.adaptiveThreshold(pic, maxval, thresh_type, type, Block Size, C)

