__author__ = 'vince_000'

import cv2
import os
import itertools
import cProfile
import matplotlib.pyplot as plt

workingDirectory = "D:\Timelapse Project\Suite Lounge III - Working Copy"
sampleSize = 2000

os.chdir(workingDirectory)

fileList = os.listdir(workingDirectory)[0:sampleSize]

# not used in this situation
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)

def calculate_diffs(fileList):
    # calculates the differences between successive images

    thisImage = cv2.imread(fileList[0], cv2.IMREAD_COLOR)
    height, width = thisImage.shape[:2]
    diffs=[]
    for path in fileList[1:len(fileList)]:
        nextImage = cv2.imread(path, cv2.IMREAD_COLOR)
        diffs.append(cv2.norm(thisImage, nextImage)/(height*width))
        thisImage = nextImage
    return diffs

# def calculate_image_distance(img_path_1, img_path_2):
#     return cv2.norm(
#         *map(lambda x: cv2.imread(x, cv2.IMREAD_COLOR), [img_path_1, img_path_2])
#     )

# print(calculate_diffs(fileList))

diffs = calculate_diffs(fileList)

plt.plot(diffs)
plt.show()



