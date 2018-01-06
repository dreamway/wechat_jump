from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys

class ChessMatching(object):
    def __init__(self):
        self.matching_method = 'cv2.TM_CCOEFF_NORMED'
        self.template = cv2.imread('asserts/chess.png', 0)
        self.template_size = self.template.shape[::-1]
        self.output = True
        self.debug = False

    def matching(self, imgfile, templatefile='asserts/chess.png'):
        img = cv2.imread(imgfile, 0)
        method = eval(self.matching_method)
        #apply template matching
        res = cv2.matchTemplate(img, self.template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if self.output: 
            print("template size:", self.template_size) 
            print("min_val:",min_val)
            print("max_val:", max_val)
            print("min_loc:", min_loc)
            print("max_loc:", max_loc)
            print('method:', method)
        
        top_left = min_loc
        bottom_right = (top_left[0]+self.template_size[0], top_left[1]+self.template_size[1])
        if self.output:            
            print("top_left:", top_left)
            print("bottom_right:", bottom_right)

        if self.debug: #display
            cv2.rectangle(img, top_left, bottom_right, (0,255,0), 3)
            plt.subplot(121), plt.imshow(res, cmap='gray')
            plt.title('Matching result'), plt.xticks([]), plt.yticks([])
            plt.subplot(122), plt.imshow(img, cmap='gray')
            plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            plt.suptitle("TM_CCOEFF_NORMED")
            plt.show()

        #return the chess basecenter 
        return ((top_left[0]+bottom_right[0])/2, bottom_right[1])

if __name__ == '__main__':
    print("Usage: ChessMatching.py filename")
    chess_matching = ChessMatching()
    chess_basecenter = chess_matching.matching(sys.argv[1])
    print("chess_basecenter:", chess_basecenter)
    