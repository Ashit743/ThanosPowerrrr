from cv2 import cv2 as cv
import handTrackingModule as htm
import subprocess
import re

# Initializing the modules
cap = cv.VideoCapture(0)
detect = htm.HandDetector(maxHands=1)

# Make this True to count the left hand
_LEFT_HAND = False

# Initializing the finger tips
tipIDs = [4, 8, 12, 16, 20]
path1 = "C:\Program Files\Google\Chrome\Application\chrome.exe"
path2 = "C:\Program Files\iTunes\iTunes.exe"
path3 = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
path4 = "C:\Program Files\Sublime Text\sublime_text.exe"

paths= {path1:1,path2:2,path3:3,path4:4}
pathsdup = paths.copy()
pathsClose = []

def drawNumber(frame, noFinger):
    font = cv.FONT_HERSHEY_DUPLEX
    text = str(noFinger)
    cv.putText(frame, text, (0, 470), font, 4, (0, 0, 255), 3)
while (cap.isOpened()):
    isSuccess, frame = cap.read()

    if isSuccess:
        frame = detect.findHands(frame)

        # Fliping the frame horrizontally
        frame = cv.flip(frame, 1)

        lmList_1 = detect.findPosition(frame, handNo=0, boxDraw=False)
        fW = cap.get(3)
        fH = cap.get(4)

        # Checking the Finger of Hand 1
        if len(lmList_1) != 0:
            fingerCheck = []

            if not _LEFT_HAND:
                # For thumb
                if lmList_1[4][1] > lmList_1[3][1]:
                    fingerCheck.append(True)
                else:
                    fingerCheck.append(False)
            else:
                # For thumb
                if lmList_1[4][1] < lmList_1[3][1]:
                    fingerCheck.append(True)
                else:
                    fingerCheck.append(False)

            # For other fngers
            for id in range(1, 5):
                if lmList_1[tipIDs[id]][2] < lmList_1[tipIDs[id] - 2][2]:
                    fingerCheck.append(True)
                else:
                    fingerCheck.append(False)

            totalFingers = fingerCheck.count(True)
            if totalFingers==1:
                try:
                    subprocess.Popen(list(paths.keys())[list(paths.values()).index(1)])
                    pathsClose.append(list(paths.keys())[list(paths.values()).index(1)])
                    paths.pop(list(paths.keys())[list(paths.values()).index(1)])

                except Exception as e:
                    pass

            if totalFingers==2:
                try:
                    subprocess.Popen(list(paths.keys())[list(paths.values()).index(2)])
                    pathsClose.append(list(paths.keys())[list(paths.values()).index(2)])
                    paths.pop(list(paths.keys())[list(paths.values()).index(2)])
                except Exception as e:
                    pass

            if totalFingers==3:
                try:
                    subprocess.Popen(list(paths.keys())[list(paths.values()).index(3)])
                    pathsClose.append(list(paths.keys())[list(paths.values()).index(3)])
                    paths.pop(list(paths.keys())[list(paths.values()).index(3)])
                except Exception as e:
                    pass

            if totalFingers==4:
                try:
                    subprocess.Popen(list(paths.keys())[list(paths.values()).index(4)])
                    pathsClose.append(list(paths.keys())[list(paths.values()).index(4)])
                    paths.pop(list(paths.keys())[list(paths.values()).index(4)])
                except Exception as e:
                    pass

            if totalFingers==5:
                try:
                    for i in pathsClose:
                        if i not in paths.keys():
                            paths[i]=pathsdup.get(i)
                        pattern = r"[\w]*.exe"
                        group=re.findall(pattern,i)
                        subprocess.call(["taskkill","/F","/IM",group[0]])
                    pathsClose=[]
                except Exception as e:
                    pass
            print(paths)
            drawNumber(frame, totalFingers)

            # Calculating the FPS
        detect.addFPS(frame)

        cv.imshow("Video", frame)
        if cv.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv.destroyAllWindows()