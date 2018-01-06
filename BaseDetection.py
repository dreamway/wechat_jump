import cv2
from matplotlib import pyplot as plt
import sys
import numpy as np

def detect_base(image):
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    
    edges = cv2.Canny(imgray, 100, 200)
    cv2.imwrite("edges.png", edges)
    img, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print("detected contours size: ", len(contours))
    img = cv2.drawContours(edges, contours, -1, (0, 255, 0), 3)
    #imshow(image)
    cv2.imwrite("contours.png", edges)
    #print("hierarchy:", hierarchy)
    print("contours length:",len(contours))
    #draw_contours_by_hierarchy_info(contours, hierarchy, image)
    draw_contours_by_area(contours, edges)

def draw_contours_by_hierarchy_info(contours, hierarchy, image_base):
    for i in range(len(contours)):
        image = image_base.copy()
        print("contours",i," hierarchy[i][0], hierarchy[i][1]", hierarchy[0][i])
        contour_hierarchy_info = hierarchy[0][i]
        next_sibling = contour_hierarchy_info[0]
        prev_sibling = contour_hierarchy_info[1]
        child = contour_hierarchy_info[2]
        parent = contour_hierarchy_info[3]
        if next_sibling==-1 and prev_sibling==-1 and child==-1:
            cnt = contours[i]
            #img = cv2.drawContours(edges, [cnt], 0, (0,255,0), 3) #maybe the drawing is wrong
            x,y,w,h = cv2.boundingRect(cnt)
            img = cv2.rectangle(image, (x,y), (x+w, y+h), (0,255, 0), 2)
            fn = "NoSibling"+str(i)+".png"
            cv2.imwrite(fn, img)
            area = cv2.contourArea(cnt)
            print("No Sibling area size:", area)
        else:
            cnt = contours[i]
            x,y, w, h = cv2.boundingRect(cnt)
            img = cv2.rectangle(image, (x,y), (x+w, y+h), (255, 0, 0), 2)
            fn = "withSibling"+str(i)+".png"
            cv2.imwrite(fn, img)
            area = cv2.contourArea(cnt)
            print("withSibling area size:", area)

def draw_contours_by_area(contours,edges):
    print(edges.shape)
    w,h = edges.shape
    AREA_CRITERIA = w*1.0/5 * h*1.0/10
    print("AREA_CRITERIA:", AREA_CRITERIA)
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area < AREA_CRITERIA:
            continue
        
        cnt = contours[i]
        img = cv2.drawContours(edges, [cnt], 0, (255,0,0), 3)
        fn = "contours_by_area"+str(i)+".png"
        cv2.imwrite(fn,img)
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        img = cv2.drawContours(image, [box], 0, (0,0, 255), 2)
        fn = "minAreaRect_"+str(i)+".png"
        cv2.imwrite(fn, img)
        img = None
        image = None

def show_image_and_canny(image, edges):
    plt.subplot(121), plt.imshow(image, cmap='gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(edges, cmap='gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.show()
    

def imshow(image):
    cv2.imshow("image",image)
    cv2.waitKey()

def main(filename):
    image = cv2.imread(filename)
    detect_base(image)

if __name__ == '__main__':
    print("usage: BaseDetection.py filename")
    main(sys.argv[1])
    