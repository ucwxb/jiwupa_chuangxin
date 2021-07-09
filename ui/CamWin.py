from PyQt5.QtWidgets import QWidget,QLabel
from PyQt5.Qt import QSize,QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage
import cv2
import numpy as np
class CamWin(QWidget):
    def __init__(self,Parent=None):
        super().__init__(Parent)

        self.__size = QSize(640,480)
        self.__InitView()
    

    def __InitView(self):
        #设置界面的尺寸为__size
        self.setFixedSize(self.__size)
        self.show_label =  QLabel(self)
        self.show_label.setFixedSize(self.__size)
        
        self.show_label.setAlignment(Qt.AlignCenter)

    def update_pic(self):
        img_rows,img_cols = self.res.shape
        QImg = QImage(self.res.data,img_cols,img_rows,QImage.Format_Indexed8)
        self.show_label.setStyleSheet('background-color: rgb(0, 0, 0)')
        self.show_label.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.show_label.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation
        ))
    
    def pre_handle_img(self,video_path):
        self.video_path = video_path
        cap = cv2.VideoCapture(self.video_path)
        ret, frame = cap.read()
        img_size = (frame.shape[0],frame.shape[1])

        self.index = 0
        self.first_sum = np.zeros(img_size)
        self.S_sum = 0
        self.I_sum_map = np.zeros(img_size)

        while(cap.isOpened()):
            ret, frame = cap.read()
            try:
                img_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  #rgb转灰度
            except:
                break
            img_gray = np.array(img_gray,dtype='float64')  #存灰度图
            img_gray /= 10.0
            res = np.sum(img_gray)
            self.S_sum += res
            self.I_sum_map += img_gray
            self.first_sum += res*img_gray

            self.index += 1 #帧索引
        cap.release()
    
    def handle_img(self,alpha = 1.0):

        S_sum = self.S_sum.copy()
        I_sum_map = self.I_sum_map.copy()
        first_sum = self.first_sum.copy()
        
        S_sum *= alpha
        S_sum /= self.index
        I_sum_map /= self.index
        first_sum /= self.index

        self.res_map = first_sum - S_sum*I_sum_map

        min_res_map = np.min(self.res_map)
        max_res_map = np.max(self.res_map)

        self.res_map -= min_res_map
        self.res_map /= (max_res_map-min_res_map)
        self.res_map *= 255

        self.res = np.array(self.res_map,dtype = np.uint8)

        self.update_pic()
        return self.cal_cnr([[0,self.res_map.shape[0]],[0,self.res_map.shape[1]]],self.res_map)
    
    def cal_cnr(self,xyxy,res_map):
        img = np.array(res_map,dtype='float64')  #存灰度图
        slice_img = img[xyxy[0][0]:xyxy[0][1],xyxy[1][0]:xyxy[1][1]]
        suop=0
        objsum=0
        sklp=0
        gbsum=0

        xfang = 0
        yfang = 0
        for i in slice_img:
            for j in i:
                if j>255/2:
                    suop=suop+j
                    objsum=objsum+1
                    xfang+=j*j
                else:
                    sklp=sklp+j
                    gbsum=gbsum+1
                    yfang+=j*j
        gobj=suop/objsum
        gb=sklp/gbsum
        xfang/=objsum
        yfang/=gbsum

        nesp=xfang-gobj*gobj
        pdnes=yfang-gb*gb

        # for i in range(xyxy[0][0],xyxy[0][1]):
        #     for j in range(xyxy[1][0],xyxy[1][1]):
        #         if img[i,j]>255/2:
        #             nes=nes+np.square(img[i,j]-gobj)
        #         else:
        #             dnes=dnes+np.square(img[i,j]-gb)
        # nesp=nes/objsum
        # pdnes=dnes/gbsum
        cnr=(gobj-gb)/np.sqrt(np.square(nesp)+np.square(pdnes))
        visibility=(gobj-gb)/(gobj+gb)
        return cnr,visibility

