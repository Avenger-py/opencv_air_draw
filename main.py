import numpy as np
import cv2
import math
cap = cv2.VideoCapture(0)

def nothing():
    pass

'''
cv2.namedWindow('hsv')

cv2.createTrackbar('H_min', 'hsv', 0, 179, nothing)
cv2.createTrackbar('H_max', 'hsv', 0, 179, nothing)
cv2.createTrackbar('S_min', 'hsv', 0, 255, nothing)
cv2.createTrackbar('S_max', 'hsv', 0, 255, nothing)
cv2.createTrackbar('V_min', 'hsv', 0, 255, nothing)
cv2.createTrackbar('V_max', 'hsv', 0, 255, nothing)
'''

cv2.namedWindow('Dock')
# create trackbars for color change
cv2.createTrackbar('R', 'Dock', 0, 255, nothing)
cv2.createTrackbar('G', 'Dock', 0, 255, nothing)
cv2.createTrackbar('B', 'Dock', 0, 255, nothing)
cv2.createTrackbar('thickness', 'Dock', 0, 100, nothing)

points = []
draw = True
while 1:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (600, 400))
    frame1 = cv2.GaussianBlur(frame, (5, 5), 0)
    frame_hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    '''
    h_min = cv2.getTrackbarPos('H_min', 'hsv')
    h_max = cv2.getTrackbarPos('H_max', 'hsv')
    s_min = cv2.getTrackbarPos('S_min', 'hsv')
    s_max = cv2.getTrackbarPos('S_max', 'hsv')
    v_min = cv2.getTrackbarPos('V_min', 'hsv')
    v_max = cv2.getTrackbarPos('V_max', 'hsv')

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    '''
    lower = np.array([0, 188, 40])
    upper = np.array([103, 255, 255])
    mask = cv2.inRange(frame_hsv, lower, upper)
    print(f'mask shape = {mask.shape}')
    output = cv2.bitwise_and(frame1, frame1, mask=mask)

    indices = np.argwhere(mask==255)
    print(f'indices shape = {indices.shape}')
    x, y = np.mean(indices[:, 1]), np.mean(indices[:, 0])
    if not math.isnan(x) and not math.isnan(y):
        if draw:
            x, y = int(x), int(y)
            points.append((x, y))

    r = cv2.getTrackbarPos('R', 'Dock')
    g = cv2.getTrackbarPos('G', 'Dock')
    b = cv2.getTrackbarPos('B', 'Dock')
    t = cv2.getTrackbarPos('thickness', 'Dock')

    if len(points)>0:
        for point in points:
            cv2.circle(frame, center=point, radius=t, color=(b, g, r), thickness=-1)
    print(f'x = {x}, y = {y}')

    frame = cv2.flip(frame, 1)
    cv2.imshow('feed', frame)
    #cv2.imshow('feed_hsv', frame_hsv)
    #cv2.imshow('mask', mask)
    cv2.imshow('output', output)
    k = cv2.waitKey(20) & 0xFF
    if k == ord('e'): #erase
        points = []
    elif k== ord('d'): #draw mode
        draw = not draw
    elif k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()