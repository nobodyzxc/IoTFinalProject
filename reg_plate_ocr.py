import cv2, sys
import numpy as np
import pytesseract

img = cv2.imread(sys.argv[1])

timeF = 10  # frame time

# 從攝影機擷取一張影像
ret, frame = 0, img

dst = cv2.pyrMeanShiftFiltering(frame, 10, 50)#濾波
gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)#灰度
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)#二值化

#cv2.imshow("ShiftFiltering", dst)
#cv2.imshow("threshold", thresh)

cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

def passGuard(lt, rd):
    a, b = lt
    c, d = rd
    return abs(a - c) > 10 and abs(b - d) > 10

def draw_border(img, point1, point2, point3, point4, line_length):

    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    x4, y4 = point4

    cv2.circle(img, (x1, y1), 3, (255, 0, 255), -1)    #-- top_left
    cv2.circle(img, (x2, y2), 3, (255, 0, 255), -1)    #-- bottom-left
    cv2.circle(img, (x3, y3), 3, (255, 0, 255), -1)    #-- top-right
    cv2.circle(img, (x4, y4), 3, (255, 0, 255), -1)    #-- bottom-right

    cv2.line(img, (x1, y1), (x1 , y1 + line_length), (0, 255, 0), 2)  #-- top-left
    cv2.line(img, (x1, y1), (x1 + line_length , y1), (0, 255, 0), 2)

    cv2.line(img, (x2, y2), (x2 , y2 - line_length), (0, 255, 0), 2)  #-- bottom-left
    cv2.line(img, (x2, y2), (x2 + line_length , y2), (0, 255, 0), 2)

    cv2.line(img, (x3, y3), (x3 - line_length, y3), (0, 255, 0), 2)  #-- top-right
    cv2.line(img, (x3, y3), (x3, y3 + line_length), (0, 255, 0), 2)

    cv2.line(img, (x4, y4), (x4 , y4 - line_length), (0, 255, 0), 2)  #-- bottom-right
    cv2.line(img, (x4, y4), (x4 - line_length , y4), (0, 255, 0), 2)

    return img

def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	# return the ordered coordinates
	return rect

def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	# return the warped image
	return warped


for i in cnts:

  #輪廓近似
  peri = cv2.arcLength(i, True)
  approx = cv2.approxPolyDP(i, 0.01*peri, True)

  if len(approx) == 4:
    beg_point = (max(approx[i][0][0] for i in range(4)),
                   max(approx[i][0][1] for i in range(4)))
    end_point = (min(approx[i][0][0] for i in range(4)),
                   min(approx[i][0][1] for i in range(4)))
    if passGuard(beg_point, end_point):
        beg_point = tuple(v + 10 for v in beg_point)
        end_point = tuple(v - 10 for v in end_point)
        color = (255, 255, 0)
        #image = cv2.rectangle(frame, beg_point, end_point, color, 2)
        points = np.array(sorted([[approx[i][0][0], approx[i][0][1]] for i in range(4)]))

        image = draw_border(frame, *points, 15)
        #xmax, ymax = beg_point
        #xmin, ymin = end_point
        #cropped_image = image[ymin:ymax, xmin:xmax]
        cropped_image = four_point_transform(frame, points)
        #cv2.imshow("result", cropped_image)

final = cropped_image
text = pytesseract.image_to_string(cropped_image, lang='eng')
print(text.strip())

# 釋放攝影機
# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()
cv2.imshow("target", image)
cv2.imshow("final", final)
cv2.waitKey(0)


#img_bgr ,scan_pic= pic_scan.pic_process(self.pic_path)
