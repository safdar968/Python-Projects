import cv2
import numpy as np


def get_masked_pad(img, perX, perY):
    height, width = img.shape
    perX = int(perX * width / 100)
    perY = int(perY * height / 100)
    x1 = perX - 100
    x2 = perX + 100
    y1 = perY - 50
    y2 = perY + 50

    mask = np.zeros((height, width, 1), np.uint8)
    masked = cv2.rectangle(mask, (x1, y1), (x2, y2), (255), -1)
    masked = cv2.bitwise_and(img, img, mask=masked)
    return masked

    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian


def check_blur(gray):
    score = cv2.Laplacian(gray, cv2.CV_64F).var()
    ret = 1
    print('score {}'.format(int(score)))
    # if the focus measure is less than the supplied threshold,
    # then the image should be considered "blurry"
    # blur score limits can be tuned according to situation
    if score < 80 or score > 110:
        ret = 0
    return ret


def get_pad(gray, perX, perY):
    gray_masked = get_masked_pad(gray, perX, perY)
    _, thresh = cv2.threshold(gray_masked, 220, 255, 0)
    _, contours, _ = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cx = None
    cy = None
    for i in contours:
        # these limits can be tuned according to required pad area
        if(cv2.contourArea(i) > 1700 and cv2.contourArea(i) < 2800):
            M = cv2.moments(i)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            print(cv2.contourArea(i))

            # k number is used to check circularity of pad
            # k=pi/4 indicates perfect square
            # NOTE: not implemented
            # perimeter = cv2.arcLength(i, True)
            # area = cv2.contourArea(i)
            # k = np.pi * 4 * (area / (perimeter * perimeter))

    return cx, cy


def get_needles(gray):
    _, invThreshold = cv2.threshold(gray, 50, 255, 0)
    inverted = cv2.bitwise_not(invThreshold)
    mask1 = np.zeros((480, 640, 1), np.uint8)
    masked1 = cv2.rectangle(mask1, (30, 30), (610, 450), (255), -1)
    inverted = cv2.bitwise_and(inverted, inverted, mask=masked1)
    thresh = cv2.erode(inverted, None, iterations=3)
    thresh = cv2.dilate(thresh, None, iterations=2)
    _, cnts, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cc = sorted(cnts, key=cv2.contourArea)
    c1 = cc[-1]
    c2 = cc[-2]
    if(c1[c1[:, :, 0].argmax()][0][0] < 333):
        needle1x = c1[c1[:, :, 0].argmax()][0][0]
        needle2x = c2[c2[:, :, 0].argmin()][0][0]
        needle1y = c1[c1[:, :, 1].argmax()][0][1]
        needle2y = c2[c2[:, :, 1].argmax()][0][1]

    if(c1[c1[:, :, 0].argmax()][0][0] > 333):
        needle2x = c1[c1[:, :, 0].argmin()][0][0]
        needle1x = c2[c2[:, :, 0].argmax()][0][0]
        needle2y = c1[c1[:, :, 1].argmax()][0][1]
        needle1y = c2[c2[:, :, 1].argmax()][0][1]

    return needle1x, needle1y, needle2x, needle2y


def main():

    perX = 50       #expected approximate x location of the pad in %ge from the left edge of the image 
    perY = 80       #expected approximate y location of the pad in %ge from the top edge of the image
    
    image = cv2.imread('9.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    #step-1 Get ROI based on expected location of pad
    masked_pad = get_masked_pad(gray, perX, perY)
    
    #step-2 Check whether image is OK (no blurr no motion)
    status = check_blur(masked_pad)
    if(status == 1):
        print("Good")
    else:
        print('bad')
        
        
    needle1x, needle1y, needle2x, needle2y = get_needles(gray)
    print(needle1x, needle1y, needle2x, needle2y)
    cv2.circle(image, (needle1x, needle1y), 3, (0), 2)
    cv2.circle(image, (needle2x, needle2y), 3, (0), 2)

    center = get_pad(gray, perX, perY)
    print(center)
    if(center[0] is not None and center[1] is not None):
        cv2.circle(image, center, 3, (0), 2)
    else:
        print('pad not found')
    
    dict = {'needle1_x': needle1x, 'needle1_y': needle1y, 'needle2_x':
            needle2x, 'needle2_y': needle2y, 'pad_x': center[0], 'pad_y':
            center[1], 'status': status}

    print(dict)
    
    # show the image
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
