import time
import requests
import cv2
import settings

faceCascade = cv2.CascadeClassifier('cascade.xml')

cam = cv2.VideoCapture(0)
counter = 0
while True:
    s, img = cam.read()
    if s:  # frame captured without any errors
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # # Draw a rectangle around the faces
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if len(faces):
            counter += 1
            if counter > 10:
                timer = 3
                while timer > 0:
                    print('Capture in ' + str(timer))
                    timer -= 1
                    time.sleep(1)
                cv2.imwrite('images/' + str(time.time()) + '.png', img)  # save image
                files = {'file': ('images/' + str(time.time()) + '.png', settings.DEVICE)}
                r = requests.post(settings.POST_URL,files=files)
                print(r.text)
                print(r.status_code)
                # cv2.imshow("Faces found", img)
                # cv2.waitKey(0)
                counter = 0
        else:
            counter = 0