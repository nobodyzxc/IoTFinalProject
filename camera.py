import cv2, sys
import numpy as np

ip = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
port = sys.argv[2] if len(sys.argv) > 2 else '4747'

#cap = cv2.VideoCapture('http://{}:{}/mjpegfeed'.format(ip, port))
cap = cv2.VideoCapture('http://{}:{}/video'.format(ip, port))

while(True):
    ret, frame = cap.read()

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
