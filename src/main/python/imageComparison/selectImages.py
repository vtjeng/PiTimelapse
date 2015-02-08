__author__ = 'vince_000'

import cv2
import os
import itertools
import cProfile
import matplotlib.pyplot as plt
import pickle
import re

workingDirectory = "D:\Timelapse Project\Suite Lounge III - Working Copy"
# startingSample = 10000
# sampleSize = 20

os.chdir(workingDirectory)

def isImageName(s):
    # matches image names of the form "image (314159).jpg" with an arbitrary number of digits
    imageFileNamePattern = re.compile("image \([0-9]+\)\.jpg")
    return bool(imageFileNamePattern.match(s))

fileList = filter(
    isImageName,
    os.listdir(workingDirectory)
)

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

repoDirectory = os.path.join(
    "C:\\Users",
    "vince_000",
    "Dropbox (Personal)",
    "Documents",
    "Programming",
    "PiTimelapse",
    )

dumpFilePath = os.path.join(
    "src",
    "main",
    "python",
    "imageComparison",
    "diffs.pickle"
)

dumpFile = open(os.path.join(repoDirectory,dumpFilePath), 'wb')
pickle.dump(diffs, dumpFile)
dumpFile.close()

plt.plot(diffs)
plt.axhline(y=0.0035,xmin=0,xmax=sampleSize,c="blue",linewidth=0.5,zorder=0)
plt.show()



