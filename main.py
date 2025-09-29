import cv2
import numpy as np


#image insertion

img = cv2.imread("Assets\z6.jpg")
img = cv2.resize(img,(500,500))



# making of the contour
image_copy=img.copy()
gray=cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
contours, hierarchy = cv2.findContours(binary, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE) 



# now we draw the contours on the image
image_copy= cv2.drawContours(image_copy, contours, -1, (255,0,0), thickness=4, lineType=cv2.LINE_AA)



# finding centre points of the circles (contours)
M1 = cv2.moments(contours[1])
M2 = cv2.moments(contours[2])
M3 = cv2.moments(contours[3])
cx1 = int(M1["m10"]/M1["m00"]) 
cx2 = int(M2["m10"]/M2["m00"])
cx3 = int(M3["m10"]/M3["m00"])
cy1 = int(M1["m01"]/M1["m00"])
cy2 = int(M2["m01"]/M2["m00"])
cy3 = int(M3["m01"]/M3["m00"])



# ordering centre points left to right
my_list = [[cx1,cy1], [cx2,cy2], [cx3,cy3]]
my_list = sorted(my_list, key = lambda k: [k[0]])
cx1 = int(my_list[0][0])
cy1 = int(my_list[0][1])
cx2 = int(my_list[1][0])
cy2 = int(my_list[1][1])
cx3 = int(my_list[2][0])
cy3 = int(my_list[2][1])

hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

pixel_centre1 = hsv_img[cx1, cy1]
hue_value1 = int(pixel_centre1[0])

pixel_centre2 = hsv_img[cx2, cy2]
hue_value2 = int(pixel_centre2[0])

pixel_centre3 = hsv_img[cx3, cy3]
hue_value3 = int(pixel_centre3[0])



# assigning color

if hue_value1 < 20:
    color1 = 'red'
elif 40 < hue_value1 < 140:
    color1 = 'blue'
else:
    color1 = 'red'


if hue_value2 < 20:
    color2 = 'red'
elif 40 < hue_value2 < 140 :
    color2 = 'blue'
else:
    color2 = 'red'


if hue_value3 < 20:
    color3 = 'red'
elif 40 < hue_value3 < 140:
    color3 = 'blue'
else:
    color3 = 'red'


# output
print(color1)
print(color2)
print(color3)



cv2.imshow('img', img)

cv2.waitKey(0)
cv2.destroyAllWindows


#it doesnt work for a few cases, I checked the BGR and HSV values at those points, its either black or white.
