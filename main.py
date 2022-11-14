# Tutorial:
# - Download the folder
# - Change imgName in row 68 to the filename
# - Open command line in folder (shift + mouse right in folder)
# - Run 'python3 main.py'

import multiprocessing
from PIL import Image
import numpy as np
import time
from queue import Queue
from threading import Thread

# Writes the html file with imgName as filenmae
def createImageFile(image, imgName):
    name = "template.html"
    file = getTemplate(name)
    file = file.replace("%REPLACEIMG%", image)
    file = file.replace("%REPLACENAME%", imgName)
    file = file.replace("%REPLACECSS%", imgName)
    writeTemplate(f"{imgName}.html", file)

# Writes the css file with the size parameters
def createStyleFile(size, imgname):
    name = "style.css"
    file = getTemplate(name)
    file = file.replace("%REPLACECOL%", str(size[0] + 1))
    file = file.replace("%REPLACEROW%", str(size[1] + 1))
    file = file.replace("%REPLACEWIDTH%", str(size[0]))
    file = file.replace("%REPLACEHEIGHT%", str(size[1]))
    writeTemplate(f"{imgName}.css", file)


def getTimeDifference(time1, time2):
    return f"{time2 - time1:0.4f} Seconds"

def fillTemplate(template, key, content):
    return template.replace(key, content)

def getTemplate(templateName):
    return open(templateName).read()

def writeTemplate(template, content):
    open('build/' + template, 'w').write(content)

# Gets the text for the defined pixelspace
def getDivForPixels(tuple):
    pixels, fromH, toH, width, threadId = tuple
    print(f"Creating thread {threadId} from {fromH} to {toH}")
    startTime = time.perf_counter()
    strList = list()
    for h in range(fromH, toH):
        #print(f"T{threadId}: {h}", flush=True)
        for w in range(width):
            r, g, b, a = pixels.obj[h, w]

            if a == 0:  # Skip transparent pixel
                continue

            strList.append(
                f"<a style=\"background:#{r:02X}{g:02X}{b:02X}{a:02X};grid-column:{w+1};grid-row:{h+1}\"/>")

    print(f"Thread {threadId} finished {(toH - fromH) * width} pixel in {getTimeDifference(startTime, time.perf_counter())}")
    return ''.join(strList)

# Program start
startTime = time.perf_counter()

imgName = "magala.png"  # Filename - Can be many different formats. Currently we support only RGBA images!
img = Image.open(imgName)
pixels = np.asarray(img)  # Convert the image data to an numpy array
# Print the name, format, size and color mode
print(imgName, img.format, img.size, img.mode)

cores = multiprocessing.cpu_count()  # Get amount of cores
rowsPerThread = img.height // cores  # Calculate rows per thread
# Calculate the rows lost by float division
lostPixel = img.height - (rowsPerThread * cores)

print(f"Distributing workload on {cores} threads a {rowsPerThread} rows per core")

que = Queue()

tasks = []
for c in range(cores):  # Create for every core a thread
    to = (rowsPerThread * (c + 1))  # Calculate the last row
    if c + 1 == cores:  # Check if this is the last core
        to += lostPixel  # Add the lostPixel to the last thread
    t = Thread(target=lambda q, arg1: q.put(getDivForPixels(arg1)), args=(que, (pixels.data, rowsPerThread * c, to, img.width, c)))
    t.start()
    tasks.append(t)  # Add new job to the pool with information to calculate

for t in tasks:  # Get the return value of all jobs
    t.join()

return_val = ""
while not que.empty():
    return_val += que.get()

print("Writing stylesheet")
createStyleFile(img.size, imgName)

print("Writing html file")
createImageFile(return_val, imgName)

print("Finished!")
print(f"Programm finished {img.height * img.width} pixel in {getTimeDifference(startTime, time.perf_counter())}")
