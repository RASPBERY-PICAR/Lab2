# import struct

# a = 1234

# bytes = struct.pack('i', a)
# b = struct.unpack('i', bytes)
# print(b)


import numpy as np
import cv2
cap = cv2.VideoCapture(0)
while(1):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
print(type(frame))
cap.release()
cv2.destroyAllWindows()
