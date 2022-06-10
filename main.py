# Main.py
import cv2
import numpy as np
import os

import DetectChars
import DetectPlates
import PossiblePlate
import MainPage

SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False
plate = ""





def page():
    MainPage.Ui_CarParkSystem()

def test(image):
    imgOriginalScene = cv2.imread("LicPlateImages/{}".format(image))  # open image
    if imgOriginalScene is None:  # if image was not read successfully
        print("\nerror: image not read from file \n\n")  # print error message to std out
        os.system("pause")  # pause so user can see error message
        return  # and exit program


    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # detect plates

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)  # detect chars in plates

    if len(listOfPossiblePlates) == 0:  # if no plates were found
        print("\nno license plates were detected\n")  # inform user no plates were found
    else:  # else
        # if we get in here list of possible plates has at leat one plate


        listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)


        licPlate = listOfPossiblePlates[0]
        if len(licPlate.strChars) == 0:  # if no chars were found in the plate
            print("\nno characters were detected\n\n")  # show message
            return  # and exit program

    return licPlate.strChars


def main(image):
    global plate
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()  # attempt KNN training

    if blnKNNTrainingSuccessful == False:  # if KNN training was not successful
        print("\nerror: KNN traning was not successful\n")  # show error message
        return  # and exit program
    # end if

    imgOriginalScene = cv2.imread("LicPlateImages/{}".format(image))  # open image

    if imgOriginalScene is None:  # if image was not read successfully
        print("\nerror: image not read from file \n\n")  # print error message to std out
        os.system("pause")
        return


    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # detect plates

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)  # detect chars in plates

    cv2.imshow("imgOriginalScene", imgOriginalScene)  # show scene image

    if len(listOfPossiblePlates) == 0:  # if no plates were found
        print("\nno license plates were detected\n")  # inform user no plates were found
    else:  # else
        # if we get in here list of possible plates has at leat one plate


        listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)


        licPlate = listOfPossiblePlates[0]

        cv2.imshow("imgPlate", licPlate.imgPlate)  # show crop of plate and threshold of plate
        cv2.imshow("imgThresh", licPlate.imgThresh)

        if len(licPlate.strChars) == 0:  # if no chars were found in the plate
            print("\nno characters were detected\n\n")  # show message
            return  # and exit program
        # end if

        drawRedRectangleAroundPlate(imgOriginalScene, licPlate)  # draw red rectangle around plate
        plate = licPlate.strChars
        print("\nlicense plate read from image = " + licPlate.strChars + "\n")
        print("----------------------------------------")

        writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)  # write license plate text on the image

        cv2.imshow("imgOriginalScene", imgOriginalScene)

        cv2.imwrite("imgOriginalScene.png", imgOriginalScene)  # write image out to file

    # end if else

    cv2.waitKey(0)  # hold windows open until user presses a key

    return


# end main


def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):
    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)  # get 4 vertices of rotated rect




def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    ptCenterOfTextAreaX = 0
    ptCenterOfTextAreaY = 0

    ptLowerLeftTextOriginX = 0
    ptLowerLeftTextOriginY = 0

    sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
    plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape

    intFontFace = cv2.FONT_HERSHEY_SIMPLEX
    fltFontScale = float(plateHeight) / 30.0  # base font scale on height of plate area
    intFontThickness = int(round(fltFontScale * 1.5))  # base font thickness on font scale

    textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale,
                                         intFontThickness)  # call getTextSize


    ((intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight),
     fltCorrectionAngleInDeg) = licPlate.rrLocationOfPlateInScene

    intPlateCenterX = int(intPlateCenterX)
    intPlateCenterY = int(intPlateCenterY)

    ptCenterOfTextAreaX = int(intPlateCenterX)  # the horizontal location of the text area is the same as the plate

    if intPlateCenterY < (sceneHeight * 0.75):  # if the license plate is in the upper 3/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(
            round(plateHeight * 1.6))  # write the chars in below the plate
    else:  # else if the license plate is in the lower 1/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(
            round(plateHeight * 1.6))  # write the chars in above the plate
    # end if

    textSizeWidth, textSizeHeight = textSize  # unpack text size width and height

    ptLowerLeftTextOriginX = int(
        ptCenterOfTextAreaX - (textSizeWidth / 2))  # calculate the lower left origin of the text area
    ptLowerLeftTextOriginY = int(
        ptCenterOfTextAreaY + (textSizeHeight / 2))  # based on the text area center, width, and height

    # write the text on the image
    cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace,
                fltFontScale, SCALAR_YELLOW, intFontThickness)



if __name__ == "__main__":
    page()
