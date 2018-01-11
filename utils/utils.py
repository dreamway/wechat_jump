import math

def calc_distance(p1, p2):
    dist = math.sqrt(math.pow(p2[0]-p1[0],2)+math.pow(p2[1]-p1[1],2))
    return dist

if __name__ == '__main__':
    p1 = (1, 1)
    p2 = (1, 3)
    print("calc_dist:", calc_distance(p1, p2))
    