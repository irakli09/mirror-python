import os
import time
import requests
import cv2
import settings
import winsound

faceCascade = cv2.CascadeClassifier('cascade.xml')

cam = cv2.VideoCapture(0)

counter = 0
countdown = False
imageName = None
countTimer = 0
while True:
    # cam.set(1, cam.get(1) - 1)
    s, img = cam.read()
    if countTimer > 0:
        countTimer -= 1
        continue

    # if countTimer > 0:
    #     countTimer -= 1
    #     continue

    if s:  # frame captured without any errors
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # if countdown:
        #     print('gadaigo')
        #     countdown = False

            # continue
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
                # timer = 3
                # counter = 0
                # if not countdown:
                imageName = 'images/' + str(time.time()) + '.png'
                cv2.imwrite(imageName, img)  # save image
                file = open(imageName, 'rb')
                files = {'files': file}
                r = requests.post(settings.POST_URL, files=files, data={'device': settings.DEVICE})
                file.close()
                os.remove(imageName)
                print(r.text)
                counter = 0
                # while timer > 0:
                #     time.sleep(1)
                #     if timer > 1:
                #         Freq = 2000  # Set Frequency To 2500 Hertz
                #         Dur = 500  # Set Duration To 1000 ms == 1 second
                #     else:
                Freq = 2000  # Set Frequency To 2500 Hertz
                Dur = 1500  # Set Duration To 1000 ms == 1 second
                winsound.Beep(Freq, Dur)
                # print('Capture in ' + str(timer))
                        # timer -= 1
                    # countdown = True
                countTimer = 100
        else:
            counter = 0

