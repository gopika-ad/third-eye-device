import cv2

url = "http://10.119.244.142:81/stream"

cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Cannot receive frame")
        break

    cv2.imshow("ESP32", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
