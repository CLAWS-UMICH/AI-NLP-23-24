import numpy as np 
import os 
import cv2 
import matplotlib.pyplot as plt

colors = {"Red": [255, 0, 0],
          "Blue": [0, 0, 255],
          "Green": [0, 255, 0],
          "Yellow": [255, 255, 0],
          "Orange": [255, 123, 0],
          "Brown": [105, 55, 55],
          "Grey": [123, 123, 123]
        }
def dist(a, b):
    sum_sq = 0
    for i in range(len(a)):
        sum_sq = (a[i] - b[i]) * (a[i] - b[i])
    return np.sqrt(sum_sq)
def get_color(filepath):
    frame = cv2.imread(filepath) 
    average = frame.mean(axis=0).mean(axis=0).astype(int)

    min_dist = 255 * 4
    b_col = None
    for col, rgb in colors.items():
        c_dist = dist(rgb, average)
        if (min_dist > c_dist):
            min_dist = c_dist
            b_col = col

    return b_col


if __name__ == "__main__":
    a = get_color('rockyardrock3.png')
    print(a)