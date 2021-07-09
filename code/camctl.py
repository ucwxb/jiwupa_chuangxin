import cv2#导入opencv包
import time

video_name = "test_video.avi"

video=cv2.VideoCapture(0)#打开摄像头
 
fourcc = cv2.VideoWriter_fourcc(*'XVID')#视频存储的格式
fps = video.get(cv2.CAP_PROP_FPS)#帧率
#视频的宽高
size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), \
        int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter('792011video.avi', fourcc, fps, size)#视频存储
start_time = time.time()
while out.isOpened():
    ret,img=video.read()#开始使用摄像头读数据，返回ret为true，img为读的图像
    if ret is False:#ret为false则关闭
        exit()
    cv2.namedWindow('video',cv2.WINDOW_AUTOSIZE)#创建一个名为video的窗口
    cv2.imshow('video',img)#将捕捉到的图像在video窗口显示
    cv2.waitKey(1)
    out.write(img)#将捕捉到的图像存储
    if time.time() - start_time > 10:
        break

