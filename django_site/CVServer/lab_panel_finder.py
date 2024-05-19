import cv2
import colorspacious as cs
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from CVServer.rectangles import find_rectangle

UPPER_BOUND_L2 = 3e-7
LOWER_BOUND_L2 = 1.6e-7
STEP = 0.2e-7
SHOW_DEBUG = False

def rgb_to_lab(rgb_tuple):
    rgb_array = np.array(rgb_tuple)
    lab = cs.cspace_convert(rgb_array, "sRGB255", "CIELab")
    return lab

def color_difference(rgb1, rgb2):
    lab1 = rgb_to_lab(rgb1)
    lab2 = rgb_to_lab(rgb2)
    delta_e = cs.deltaE(lab1, lab2, input_space="CIELab")
    return delta_e

def lab_ballz_finder(img):
    balls = find_balls(img)            
    # balls = None
    if not balls:
        # balls = [[300,300], [300,500], [600,300], [600,500]]
        balls = [[200,300], [200, 600], [500,300], [500,600]]
    # print(balls)
    for ball in balls:
        cv2.circle(img, ball, 10, (255,0,0))
    cv2.imwrite('image.jpg', img)    
    return balls

def find_maxima(scale_space, k_xy=5, k_s=1):
    """
    Extract the peak x,y locations from scale space

    Input
      scale_space: Scale space of size HxWxS
      k: neighborhood in x and y
      ks: neighborhood in scale

    Output
      list of (x,y) tuples; x<W and y<H
    """
    if len(scale_space.shape) == 2:
        scale_space = scale_space[:, :, None]

    H, W, S = scale_space.shape
    maxima = []
    for i in range(H):
        for j in range(W):
            for s in range(S):
                # extracts a local neighborhood of max size
                # (2k_xy+1, 2k_xy+1, 2k_s+1)
                neighbors = scale_space[max(0, i - k_xy):min(i + k_xy + 1, H),
                                        max(0, j - k_xy):min(j + k_xy + 1, W),
                                        max(0, s - k_s):min(s + k_s + 1, S)]
                mid_pixel = scale_space[i, j, s]
                num_neighbors = np.prod(neighbors.shape) - 1
                # if mid_pixel > all the neighbors; append maxima
                if np.sum(mid_pixel < neighbors) == num_neighbors:
                    maxima.append((i, j, s))
    return maxima


def find_balls(img):  
    lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # print(lab_img.shape)
    # plt.imshow(lab_img[:, :, 0])
    # plt.show()

    # plt.imshow(lab_img[:, :, 1])
    # plt.show()

    # plt.imshow(lab_img[:, :, 2])
    # plt.show()

    # color = np.array([0, 130, 130])
    color = np.array([60, 150, 105])

    no_luminance = lab_img
    no_luminance[:,:,0] = 0
    dist = np.exp(-np.linalg.norm(no_luminance-color, axis=2)*0.25)
    # dist = np.linalg.norm(no_luminance-color, axis=2)

    # plt.imshow(dist)
    # plt.show()

    kernel = np.ones((5,5),np.float32)/25
    dist = cv2.filter2D(dist,-1,kernel)
    
    # plt.imshow(dist)
    # plt.show()
    first = True
    # mask = cv2.inRange(dist, 30, 90)
    lower_bound = LOWER_BOUND_L2
    upper_bound = UPPER_BOUND_L2
    points = []

    while first or len(points) >= 20:
        first = False
        mask = cv2.inRange(dist, lower_bound, upper_bound)

        kernel = np.ones((10,10),np.float32)
        mask = cv2.filter2D(mask,-1,kernel)

        # plt.imshow(mask)
        # plt.show()

        # Find contours
        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    
        # Extract contours depending on OpenCV version        

        # Iterate through contours and filter by the number of vertices 
        points=[cv2.boundingRect(cnt) for cnt in cnts]    
        lower_bound += STEP
        # upper_bound -= STEP
    if SHOW_DEBUG:
        plt.imshow(mask)
        plt.show()
    # for x, y, w, h in points:
    #     cv2.rectangle(img, (x,y), (x+w,y+h), (0, 255, 0), 3)
    
    corners = find_rectangle([[x[0]+(x[2]//2),x[1]+(x[3]//2)] for x in points])    

    if SHOW_DEBUG:
        show_corners(img, corners)
    return corners

def load_image(path):
    img = cv2.imread(path)
    return img

def show_corners(img, corners):
    if corners:
        for corner in corners:
            cv2.circle(img, corner, 10, (255, 0, 0), 3)

    plt.imshow(img)
    plt.show()

    
if __name__ == "__main__":
    # for i in range(1,60):
    img = load_image(f'./purple_markers.jpg')
    corners = find_balls(img)
    print(corners)
    show_corners(img, corners)

    # find_balls('drawn_ball.jpg')