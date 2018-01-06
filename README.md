# WeChat Jump

## image capture
adb shell screencap -p /sdcard/jump.png
adb shell pull /sdcard/jump.png .

## screen push simulation
1. Enable *USB debugging*
2. adb shell input touchscreen swipe 100 200 200 300 1000
Now can see the chess jump. Good start point

## recognize the captured image & calc the distance
1. Chess shape & recording


2. 



## Setup the relationship between distance & tap ms, and learn it 
*TODO*

##Misc
1. random generate the swipe coordinates to avoid wechat system block
2.

#References
[1] http://blog.blecentral.com/2015/07/01/simulate-user-generated-events-in-android/

[2] http://blog.csdn.net/jgw2008/article/details/52913543, Android touch event

[3] https://jingyan.baidu.com/article/3c48dd3490f110e10be358dc.html
GIMP & alpha adding , foreground selection

[4]. https://jingyan.baidu.com/article/93f9803f062990e0e56f557a.html
Use Gimp & Mask to generate the foreground image

[5]. Python Template Matching:
http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html

