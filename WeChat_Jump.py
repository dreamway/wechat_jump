import sys
from utils import cmd_simulator
from utils.utils import *
from BaseDetector import *
from ChessMatcher import *
import glob

def test():        
    chess_matcher = ChessMatcher()
    base_detector = BaseDetector()
    filelist = glob.glob('./data/*.png')
    for fn in filelist:
        print("Testing file:", fn)
        chess_basecenter = chess_matcher.matching(fn)
        print("chess_basecenter:", chess_basecenter)
        image = cv2.imread(fn)
        target_loc = base_detector.detect(image, chess_basecenter)
        print("target_loc", target_loc)
        dist = calc_distance(chess_basecenter, target_loc)
        print("dist:", dist)

def main():
    for i in range(40): 
        capturescreen_and_pull('test.jpg')
        chess_basecenter = chess_matcher.matching('data/test.jpg')
        print("chess_basecenter:", chess_basecenter)
        image = cv2.imread('data/test.jpg')
        target_loc = base_detector.detect(image, chess_basecenter)
        print("target_loc:", target_loc)
        #TODO: if target_loc is None?
        dist = calc_distance(chess_basecenter, target_loc)
        print("dist:", dist)



    
if __name__ == '__main__':
    #main()
    test()
    
