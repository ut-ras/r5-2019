#DBSCAN
#parameters
import cv2
import numpy as np
#global const episilon
episilon = 3;   #3pixels


#M - Mask
#e - epsilon tuning var
#minSize - minSize tuning var
def DB_SCAN(M, e, minSize):
    id = 1
    for row in range(0, height):
        for col in range(0, width):
            if M[row][col] == -1:
                if Fill(M, row, col, e, id) < minSize:
                    Fill(M, row, col, e, 0, id)
                else:
                    id = id + 1
    return M

def Fill(M, row, col, e, id, oldId=-1):
    ctr = 1
    M[row][col] = id
    for row2 in range(-e, e):
        for col2 in range(-e, e):
            if (row2*row2 + col2*col2) <= (e*e):
                if(row+row2) >= 0 and (row+row2) < height and (col+col2) >= 0 and (col+col2) < width and M[row+row2][col+col2] == oldId:
                    ctr = ctr + Fill(row+row2, col+col2, id, M)
    return ctr

img = cv2.imread('test.png',0)
ret,thresh_img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
M = DB_SCAN(thresh_img, e, 5)
for row in M:
    for col in M[row]:
        print(M)
    print("\n")
