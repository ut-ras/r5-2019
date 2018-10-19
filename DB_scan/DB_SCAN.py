#!/usr/bin/python3
#Author: Matthew Yu and Timothy Bertotti

#DBSCAN
#parameters
import cv2
import numpy as np
import sys

#global const episilon
episilon = 3   #3pixels
minSize = 30
height = 0
width = 0

#M - Mask
#e - epsilon tuning var
#minSize - minSize tuning var
def DB_SCAN(M, e, minSize):
    id = 1
    for row in range(0, height):
        for col in range(0, width):
            if M[row][col] == 255:
                ctr = Fill(M, row, col, e, id)
                print(id,"\t", ctr)
                if ctr < minSize:
                    Fill(M, row, col, e, 0, id)
                else:
                    id = id + 1
    return M

def Fill(M, row, col, e, id, oldId=255):
    ctr = 1
    M[row][col] = id*25
    for row2 in range(-e, e):
        for col2 in range(-e, e):
            if (row2*row2 + col2*col2) <= (e*e):
                if(row+row2) >= 0 and (row+row2) < height and (col+col2) >= 0 and (col+col2) < width and M[row+row2][col+col2] == oldId:
                    ctr = ctr + Fill(M, row+row2, col+col2, e, id)
    return ctr

maskName = sys.argv[1]
img = cv2.imread(maskName,0)
width, height = np.shape(img)
print("width:\t",width,"\theight:\t",height)

ret,thresh_img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
print(thresh_img, "\n")
M = DB_SCAN(thresh_img, episilon, minSize)
#cv2.imshow("res", thresh_img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
cv2.imwrite(maskName + '_tested.png', M)
