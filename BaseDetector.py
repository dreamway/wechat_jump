import cv2
from matplotlib import pyplot as plt
import sys
import numpy as np
import math

class BaseDetector(object):
    def __init__(self):
        self.debug_imwrite = True
        self.debug_imshow = False
        self.debug_draw = False
        self.debug_output = False
        self.AREA_RATIO_CRITERIA = 1.0/200
        self.ROI_Rect = None
    
    def set_debug_imwrite(self, flag):
        self.debug_imwrite = flag

    def set_debug_output(self, flag):
        self.debug_output = flag

    def plt_show(self, image, title="image"):
        plt.subplot(111), plt.title(title)
        plt.imshow(image)
        plt.show()

    def detect(self, image, origin_loc):
        h, w, c = image.shape
        print("w:",w,", h:",h," ,c:",c)
        Y_OFFSET = 600
        self.ROI_Rect = (0, origin_loc[1]-Y_OFFSET, w, int(Y_OFFSET*1.5))  #left-top, width, height
        print("ROI_Rect:", self.ROI_Rect)
        imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    
        cv2.imwrite("gray.jpg", imgray)

        edges = cv2.Canny(imgray, 50, 150)
        if self.debug_imwrite:
            cv2.imwrite("canny.jpg", edges)

        kernel = np.ones((5,5), np.uint8)
        dilation = cv2.dilate(edges, kernel, iterations=1)
        cv2.imwrite("dilation.jpg", dilation)
        #erosion = cv2.erode(dilation, kernel, iterations=1)
        #self.plt_show(erosion, "erosion")
        #cv2.imwrite("erosion.jpg", erosion)

        img, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if self.debug_output:
            print("detected contours size: ", len(contours))
            print("contours length:",len(contours)) 
        
        if self.debug_imwrite:
            img2 = image.copy()
            img = cv2.drawContours(img2, contours, -1, (0, 255, 0), 3)
            cv2.imwrite("all_contours.jpg", img2)

        if self.debug_draw:
            self._draw_contours_by_hierarchy_info(contours, hierarchy, image)
            self._draw_contours_by_area(contours, edges, image)
        
        return self._detect_target_loc(contours, hierarchy, image, origin_loc)

    def _detect_target_loc(self, contours, hierarchy, image_base, origin_loc):
        """
        detect target loc by using hierarchy info(NO siblings) & Area & minAreaRect(rotated angle) and its relation of centroid & origin_loc
        """
        h, w, c = image_base.shape
        print("detect_target_loc, w:",w, ", h:", h, ", c:", c)
        AREA_CRITERIA = w*h*self.AREA_RATIO_CRITERIA
        AREA_CRITERIA = 2000
        target_loc = []
        for i in range(len(contours)):
            image = image_base.copy()
            cnt = contours[i]
            print("contour area: ", cv2.contourArea(cnt))
            if cv2.contourArea(cnt) < AREA_CRITERIA:
                print("contourArea is small, continue")
                continue

            x,y,w,h = cv2.boundingRect(cnt)
            print("bouding rect is: ", x, ", ", y, ", ", w, ", ", h)
            
            if self._feature_inside_ROI(x,y,w,h) == False:
                print("feature not inside ROI,boundingRect(",x,",",y,",",w,",",h,")", "ROI :",self.ROI_Rect)
                continue
            
            centroid = self._calc_centroid(cnt)
            print("ROI:", self.ROI_Rect)
            print("drawRectangle:",)
            img = cv2.rectangle(image, (2, self.ROI_Rect[1]), (2+self.ROI_Rect[2], self.ROI_Rect[1]+self.ROI_Rect[3]-4), (255,255,0), 2) #draw ROI Rect
            img = cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
            img = cv2.drawContours(image, [cnt], 0, (255, 0, 0), 3)
            img = cv2.circle(image, centroid, 10, (0, 0, 255), -1)
            minAreaRect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(minAreaRect)
            box = np.int0(box)            
            cv2.drawContours(image, [box], 0, (0,0,255), 2)
            rotated_angle = minAreaRect[2]                
            print("Rotated angle:", rotated_angle)
            predict_angle = self._angle_between(centroid, origin_loc)
            print("predict_angle:", predict_angle)

            fn = "detect_"+str(i)+".jpg"
            cv2.imwrite(fn, image)
            target_loc.append(centroid)

        if len(target_loc) == 1:
            return target_loc[0]
        elif len(target_loc) == 0:
            print("Warning: did not find the target loc.")
            return None
        elif len(target_loc) > 1:
            print("Warning: find more than one target loc. TODO: select the best one.")
            return None

    def _draw_contours_by_hierarchy_info(self, contours, hierarchy, image_base):
        """
        debug function: for showing the hierarchy info
        """
        for i in range(len(contours)):
            image = image_base.copy()
            if self.debug_output:
                print("contours",i," hierarchy[i][0], hierarchy[i][1]", hierarchy[0][i])

            contour_hierarchy_info = hierarchy[0][i]
            next_sibling = contour_hierarchy_info[0]
            prev_sibling = contour_hierarchy_info[1]
            child = contour_hierarchy_info[2]
            parent = contour_hierarchy_info[3]
            if next_sibling==-1 and prev_sibling==-1 and child==-1: #the standalone contour might be the good one
                cnt = contours[i]            
                x,y,w,h = cv2.boundingRect(cnt)
                img = cv2.rectangle(image, (x,y), (x+w, y+h), (0,255, 0), 2)
                img = cv2.drawContours(image, [cnt], 0, (255, 0, 0), 3)
                area = cv2.contourArea(cnt)
                print("No Sibling area size:", area)
                centroid = self._calc_centroid(cnt)
                print("centroid:", centroid)
                img = cv2.circle(image, centroid, 10, (0, 0, 255), -1)
                fn = "NoSibling"+str(i)+".jpg"
                cv2.imwrite(fn, img)            
            else:
                cnt = contours[i]
                x,y, w, h = cv2.boundingRect(cnt)
                img = cv2.rectangle(image, (x,y), (x+w, y+h), (255, 0, 0), 2)
                fn = "withSibling"+str(i)+".jpg"
                cv2.imwrite(fn, img)
                area = cv2.contourArea(cnt)
                print("withSibling area size:", area)

    def _draw_contours_by_area(self, contours,edges, image_base):
        w,h = edges.shape
        AREA_CRITERIA = w*h*self.AREA_RATIO_CRITERIA
        print("AREA_CRITERIA:", AREA_CRITERIA)
        for i in range(len(contours)):
            image = image_base.copy()
            area = cv2.contourArea(contours[i])
            if area < AREA_CRITERIA:
                continue
            
            cnt = contours[i]
            img = cv2.drawContours(image, [cnt], 0, (255,0,0), 3)
            centroid = self._calc_centroid(cnt)
            img = cv2.circle(image, centroid, 10, (255,0,0), 2) #draw contour centroid
            rect = cv2.minAreaRect(cnt)
            print("Rotated minAreaRect:", rect)
            print('Angle:', rect[2])
            box = cv2.boxPoints(rect)
            box = np.int0(box)        
            img = cv2.drawContours(image, [box], 0, (0,0, 255), 2) #draw Rotated minAreaRect
            fn = "contours_minAreaRect_"+str(i)+".jpg"
            cv2.imwrite(fn, img)

    def _calc_centroid(self, cnt):
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        return (cx,cy)

    def _angle_between(self, p1, p2):        
        ang1 = np.arctan2(*p1[::-1])
        ang2 = np.arctan2(*p2[::-1])
        return np.rad2deg((ang1-ang2)%(2*np.pi))

    def _feature_inside_ROI(self, x, y, w, h):
        print("x:", x, "self.rect[0]:",self.ROI_Rect[0], ", y:",y,", ROI_Rect[1]:", self.ROI_Rect[1])
        print("x+w:",x+w,"y+h:",y+h)
        if x > self.ROI_Rect[0] and y > self.ROI_Rect[1] and (x+w)<(self.ROI_Rect[0]+self.ROI_Rect[2]) and (y+h)<(self.ROI_Rect[1]+self.ROI_Rect[3]):
            return True
        return False
   
    def plot_baseimage_and_cmp_image(self, image_base, image_cmp):
        plt.subplot(121), plt.imshow(image_base, cmap='gray')
        plt.title('Base Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(image_cmp, cmap='gray')
        plt.title('Compare Image'), plt.xticks([]), plt.yticks([])
        plt.show()
        

def test(filename='data/jump.png', chess_basecenter=(338,1256)):
    image = cv2.imread(filename)
    base_detector = BaseDetector()    
    base_detector.set_debug_imwrite(True)
    base_detector.set_debug_output(True)
    target_loc = base_detector.detect(image, chess_basecenter)
    print("Target LOC: ", target_loc, " Chess_Loc:", chess_basecenter)
    dist = math.sqrt(math.pow(target_loc[0]-chess_basecenter[0],2)+math.pow(target_loc[1]-chess_basecenter[1],2))
    print("Jump Dist: ", dist)

    #TestCode
    A = (1,0)
    B = (1,-1)
    print(base_detector._angle_between(A,B))
    print(base_detector._angle_between(B,A))

def main(filename):    
    image = cv2.imread(filename)
    #TODO: Need to calc chess_basecenter

    base_detector = BaseDetector()
    #base_detector.plt_show(image)
    base_detector.set_debug_imwrite(True)
    base_detector.set_debug_output(True)

    fake_basecenter = (338,1256)
    base_detector.detect(image, fake_basecenter)

if __name__ == '__main__':
    print("usage: BaseDetection.py filename ")
    main(sys.argv[1])
    #test()
    