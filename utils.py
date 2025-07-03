import cv2 as cv
import numpy as np

def preProcessing(img):
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.GaussianBlur(img, (3, 3), 1)
    img = cv.adaptiveThreshold(img, 255, 1, 1, 9, 2)
    return img

def findBiggestContour(contours):
    np.array([])
    max_area = 0
    for i in contours:
        area = cv.contourArea(i)
        if area > 50:
            peri = cv.arcLength(i, closed=True)
            corners = cv.approxPolyDP(i, 0.02*peri, closed=True)
            if(area > max_area and len(corners) == 4):
                biggest_contour = corners
                max_area = area

    return biggest_contour

def reorder(biggest_contours):
    corners = np.zeros((4,1,2), dtype=np.int32)
    biggest_contours = biggest_contours.reshape(4,2)

    add = biggest_contours.sum(axis=1)
    corners[0] = biggest_contours[np.argmin(add)]
    corners[3] = biggest_contours[np.argmax(add)]

    diff = np.diff(biggest_contours, axis=1)
    corners[1] = biggest_contours[np.argmin(diff)]
    corners[2] = biggest_contours[np.argmax(diff)]

    return corners

def applyWarpPerspective(img, biggest_Contour, size):
    pts1 = np.float32(biggest_Contour)
    pts2 = np.float32([[0,0], [270,0], [0,270], [270,270]])

    matrix = cv.getPerspectiveTransform(pts1, pts2)
    img = cv.warpPerspective(img, matrix, size)    

    return img

def splitBoxes(img):
    boxes = []
    rows = np.vsplit(img, 9)
    for row in rows:
        cols = np.hsplit(row, 9)
        for col in cols:
            boxes.append(col)

    return boxes

def makeSudokuGrid(boxes, model, confidence_threshold):
    numbers = []
    for image in boxes:
        image = np.asarray(image)
        image = image[4:-4, 4:-4]
        image = cv.resize(image, (30, 30))
        image = image/255.0
        image = image.reshape(1, 30, 30, 1)

        prediction = model.predict(image)
        classIndex = np.argmax(prediction, axis=1)
        probabilityValue = np.amax(prediction, axis=1)

        if(probabilityValue) > confidence_threshold:
            numbers.append(classIndex[0])
        else:
            numbers.append(0)

    numbers = np.reshape(numbers, (9,9))
    return numbers


def overlaySolution(orignal_img, solver, sudokuGrid, biggest_Contour):
    blank = np.zeros(orignal_img.shape, dtype='uint8')
    length = orignal_img.shape[0]/9
    for i in range(9):
        for j in range(9):
            if(sudokuGrid[i][j] == 0):
                cv.putText(blank, str(solver.grid[i][j]), (int(j*length+10), int((i+1)*length-5)), cv.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 1)

    pts1 = np.float32(biggest_Contour)
    pts2 = np.float32([[0,0], [270,0], [0,270], [270,270]])

    inv_matrix = cv.getPerspectiveTransform(pts2, pts1)
    blank = cv.warpPerspective(blank, inv_matrix, orignal_img.shape[:2])

    alpha = 0.7
    mask = np.any(blank != [0, 0, 0], axis=2)

    overlay = blank.astype(np.float32)
    base = orignal_img.astype(np.float32)

    blended = base.copy()
    blended[mask] = alpha * overlay[mask] + (1 - alpha) * base[mask]

    orignal = blended.astype(np.uint8)

    return orignal

