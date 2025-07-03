print("setting up")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import cv2 as cv
from tensorflow.keras.models import load_model
import numpy as np

from sudokuSolver import SudokuSolver
from utils import *

#declaring variables
size = (270,270)
confidence_threshold =  0.8
img_path = 'Resources/src_img1.png'
model_path = 'Model/recognizer.h5'

#importing image and image recognition model
model = load_model(model_path)
orignal_img = cv.imread(img_path)
orignal_img = cv.resize(orignal_img, size)

#pre-processing the image
img = preProcessing(orignal_img.copy())

#finding biggest contour
contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
biggest_contour = findBiggestContour(contours)


if(biggest_contour.size != 0):
    print("Sudoku found!!")
    biggest_contour = reorder(biggest_contour)

    img = applyWarpPerspective(img, biggest_contour, size)

    boxes = splitBoxes(img)

    sudokuGrid = makeSudokuGrid(boxes, model, confidence_threshold)

    solver = SudokuSolver(sudokuGrid)

    print("Given puzzle:")
    solver.print_grid()

    solver.solve()
    print("solved:")
    solver.print_grid()


    solved = overlaySolution(orignal_img, solver, sudokuGrid, biggest_contour)
    cv.imshow("Input", orignal_img)
    cv.imshow("Solved", solved)


else:
    print("Sudoku not found")   



cv.waitKey(0)


