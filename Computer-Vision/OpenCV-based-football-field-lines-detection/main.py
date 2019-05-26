import cv2
import numpy as np
video = cv2.VideoCapture("video path")
while True:
    ret, orig_frame = video.read()
    if not ret:
       video = cv2.VideoCapture("/videopath")
       continue
    # orig_frame = cv2.imread('1.png')
    frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    low_white = np.array([0, 20, 110])
    up_white = np.array([360, 90, 178])
    mask = cv2.inRange(hsv, low_white, up_white)
    edges = cv2.Canny(mask, 20, 50)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 115, maxLineGap=50)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
    frame = cv2.resize(frame, (800, 600))
    cv2.imshow("frame", frame)
    edges = cv2.resize(edges, (800, 600))
    cv2.imshow("edges", edges)
    key = cv2.waitKey(5)
    if key == 27:
        break
video.release()
cv2.destroyAllWindows()