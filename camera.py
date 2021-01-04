import cv2, sys, time, json
import numpy as np
from reg_plate_ocr import ocr
import requests

ip = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
port = sys.argv[2] if len(sys.argv) > 2 else '4747'

#cap = cv2.VideoCapture('http://{}:{}/mjpegfeed'.format(ip, port))
cap = cv2.VideoCapture('http://{}:{}/video'.format(ip, port))

frame_rate = 1
prev = 0

pass_list = []

def check(plates, results)
    for uid in plates:
        for plate in results:
            if plate in plates[uid]:
                return (uid, plate)
    return False

while True:

    time_elapsed = time.time() - prev

    ret, frame = cap.read()

    if ret and time_elapsed > 1./frame_rate:
        prev = time.time()
        results = ocr(frame)
        if results:
            plates = json.load(open('data.json'))
            results = results.split()
            access = check(plates, results)
            if access:
                print(f"========= ACESS {plate} PASSS =========")
                if plate not in pass_list:
                    pass_list.append(plate)
                    user, plate = access
                    r = requests.post(
                            "http://localhost:8501/access",
                            data={'user': user, 'plate': plate})
                    print(r.status_code, r.reason)
            else:
                print(f"error '{plate}'")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
