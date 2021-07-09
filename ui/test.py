from PyQt5.Qt import QWidget, QColor, QPixmap, QIcon, QSize, QCheckBox
from PyQt5.QtWidgets import QVBoxLayout, QPushButton,QLabel, QGridLayout,QSlider,QFileDialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import sys
import os
import cv2
from CamWin import CamWin
class MainWidget(QWidget):
    
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.__CamWin = CamWin(self)
        self.fileName = None
        self.__InitView()
        

    def __InitView(self):
        self.setFixedSize(640,640)
        self.setWindowTitle("抗散射介质图像重建")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)

        btn_grid=QGridLayout()
        btn_grid.setContentsMargins(0,0,0,0)
        self.btn = QPushButton()
        self.btn.setStyleSheet("font-size:20px")
        self.btn.setText("选择文件")
        self.btn.clicked.connect(self.open_file)

        self.save_btn = QPushButton()
        self.save_btn.setStyleSheet("font-size:20px")
        self.save_btn.setText("保存图像")
        self.save_btn.setFixedWidth(100)
        self.save_btn.clicked.connect(self.save_img)

        btn_grid.addWidget(self.btn,0,0)
        btn_grid.addWidget(self.save_btn,0,1)

        self.label = QLabel()
        btn_grid.addWidget(self.label,0,2)

        self.sp=QSlider(Qt.Horizontal)
         
        self.sp.setMinimum(500)
        self.sp.setMaximum(1500)
        self.sp.setSingleStep(1)
        self.sp.setValue(1000)
        self.sp.setFixedWidth(100)
        self.alpha = self.sp.value() / 1000.0
        self.sp.valueChanged.connect(self.valuechange)
        btn_grid.addWidget(self.sp,1,0)

        self.sp_label = QLabel()
        btn_grid.addWidget(self.sp_label,1,1,1,2)


        main_layout.addLayout(btn_grid)

        main_layout.addWidget(self.__CamWin)

    def valuechange(self):
        # print(self.sp.value())
        if self.fileName:
            self.alpha = self.sp.value() / 1000.0
            # self.__CamWin.handle_img(self.alpha)
            cnr,visibility = self.__CamWin.handle_img(self.alpha)
            self.sp_label.setText("a=%.3f 衬噪比:%.3f"%(self.alpha,cnr))
            # self.sp_label.setText("a=%.3f"%(self.alpha))
    

    def open_file(self):
        self.fileName,_ = QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(), "All Files(*)")
        if self.fileName == '' or self.fileName == None:
            return

        self.label.setText(self.fileName)
        self.__CamWin.pre_handle_img(self.fileName)
        self.__CamWin.handle_img(self.alpha)
    
    def save_img(self):
        if self.fileName == None:
            return
        last_name = self.fileName.split('/')[-1]
        src_vid_name = last_name[0:last_name.index(last_name.split('.')[-1])-1]
        save_path = '%s_%.3f.jpg'%(src_vid_name,self.alpha)
        save_path = os.path.join(self.fileName[0:self.fileName.index(src_vid_name)],save_path)
        self.label.setText("已保存："+save_path)
        cv2.imwrite(save_path,self.__CamWin.res)
    
    def keyPressEvent(self, event):
        if(event.key() == Qt.Key_Left):
            self.sp.setValue(self.sp.value()-1)
        if(event.key() == Qt.Key_Right):
            self.sp.setValue(self.sp.value()+1)

def main():
    app = QApplication(sys.argv)
    mainWidget = MainWidget()
    mainWidget.show()
    exit(app.exec_())

if __name__ == '__main__':
    main()
