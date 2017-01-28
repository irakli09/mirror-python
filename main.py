import os
import time
import requests
import cv2
import settings

faceCascade = cv2.CascadeClassifier('cascade.xml')

cam = cv2.VideoCapture(0)
counter = 0
countdown = False
imageName = None
while True:
    s, img = cam.read()
    if s:  # frame captured without any errors
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if countdown:
            countdown = False
            imageName = 'images/' + str(time.time()) + '.png'
            cv2.imwrite(imageName, img)  # save image
            file = open(imageName,'rb')
            files = {'files': file}
            r = requests.post(settings.POST_URL,files=files,data={'device': settings.DEVICE})
            file.close()
            os.remove(imageName)
            print(r.text)
            print(r.status_code)
            counter = 0
            continue
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
                if not countdown:
                    while timer > 0:
                        print('Capture in ' + str(timer))
                        timer -= 1
                        time.sleep(1)
                    countdown = True

                # cv2.imshow("Faces found", img)
                # cv2.waitKey(0)
        else:
            counter = 0

