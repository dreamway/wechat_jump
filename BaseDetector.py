import cv2
from matplotlib import pyplot as plt
import sys
import numpy as np

class BaseDetector(object):
    def __init__(self):
        self.debug_imwrite = False
        self.debug_imshow = False
        self.debug_output = False
        self.AREA_WIDTH_RATIO_CRITERIA = 1.0/5
        self.AREA_HEIGHT_RATIO_CRITERIA = 1.0/10
    
    def set_debug_imwrite(self, flag):
        self.debug_imwrite = flag

    def set_debug_output(self, flag):
        self.debug_output = flag

    def detect(self, image, origin_loc):
        imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    
        edges = cv2.Canny(imgray, 100, 200)
        if self.debug_imwrite:
            cv2.imwrite("canny.jpg", edges)
        
        img, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        if self.debug_output:
            print("detected contours size: ", len(contours))
            print("contours length:",len(contours)) 
        
        if self.debug_imwrite:
            img2 = image.copy()
            img = cv2.drawContours(img2, contours, -1, (0, 255, 0), 3)
            cv2.imwrite("all_contours.jpg", img2)

        if self.debug_imwrite:
            self._draw_contours_by_hierarchy_info(contours, hierarchy, image)
            self._draw_contours_by_area(contours, edges, image)
            
        return self._detect_target_loc(contours, hierarchy, image, origin_loc)

    def _detect_target_loc(self, contours, hierarchy, image_base, origin_loc):
        """
        detect target loc by using hierarchy info(NO siblings) & Area & minAreaRect(rotated angle) and its relation of centroid & origin_loc
        """
        #TODO
        pass


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
        AREA_CRITERIA = w*h*self.AREA_WIDTH_RATIO_CRITERIA*self.AREA_HEIGHT_RATIO_CRITERIA
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
    base_detector.detect(image, chess_basecenter)

def main(filename):    
    image = cv2.imread(filename)
    #TODO: Need to calc chess_basecenter

    base_detector = BaseDetector()
    base_detector.set_debug_imwrite(True)
    base_detector.set_debug_output(True)

    fake_basecenter = (338,1256)
    base_detector.detect(image, fake_basecenter)

if __name__ == '__main__':
    print("usage: BaseDetection.py filename ")
    #main(sys.argv[1])
    test()
    