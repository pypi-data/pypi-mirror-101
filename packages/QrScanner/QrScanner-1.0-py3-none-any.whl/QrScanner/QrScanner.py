import pyzbar.pyzbar as pyzbar
import cv2

def Scan():
    i = 0
    cap = cv2.VideoCapture(0)
    while i<4:
        _,frame = cap.read()
        decoded = pyzbar.decode(frame)
        for obj in decoded:
            print(obj.data)
            i = i+1
        cv2.imshow("QRCode",frame)
        cv2.waitKey(5)
        cv2.destroyAllWindows
Scan()

