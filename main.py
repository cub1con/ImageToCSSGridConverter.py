#hello <3
#HI !!!
# Tutorial:
# - Download the folder
# - Change imgName in row 61 to the filename
# - Open command line in folder (shift + mouse right in folder)
# - Run 'python3 main.py'

import multiprocessing
from multiprocessing.pool import ThreadPool
from PIL import Image
import numpy as np
import time

def createImageFile(image, imgName):
  name = "template.html"
  file = getTemplate(name)
  file = file.replace("%REPLACEIMG%", image)
  file = file.replace("%REPLACENAME%", imgName)
  writeTemplate(name, file)


def createStyleFile(size):
  name = "style.css"
  file = getTemplate(name)
  file = file.replace("%REPLACECOL%", str(size[0] + 1))
  file = file.replace("%REPLACEROW%", str(size[1] + 1))
  file = file.replace("%REPLACEWIDTH%", str(size[0]))
  file = file.replace("%REPLACEHEIGHT%", str(size[1]))
  writeTemplate(name, file)

def getTimeDifference(time1, time2):
  return f"{time2 - time1:0.4f} Seconds"

def fillTemplate(template, key, content):
  return template.replace(key, content)


def getTemplate(templateName):
  return open(templateName).read()


def writeTemplate(template, content):
  open('build/' + template, 'w').write(content)

def getDivForPixels(pixels, fromH, toH, width, threadId):
  print(f"Creating thread {threadId} from {fromH} to {toH}")
  startTime = time.perf_counter()
  str = ""
  for h in range(fromH, toH):
    print(f"T{threadId}: {h}", flush=True)
    for w in range(width):
      #print(f"h: {h} | w: {w}")
      #r, g, b, a = img.getpixel((w, h))      
      r, g, b, a = pixels[h, w]
      if a == 0:
        #print(f"Skipped {h, w}")  
        continue

      str = str + (
        f"<div style=\"background-color:rgba({r},{g},{b},{a});grid-column:{w+1}/{w+2};grid-row:{h+1}/{h+2}\"></div>\n"
      )
  
  print(f"Thread {threadId} finished {(toH - fromH) * width} pixel in {getTimeDifference(startTime, time.perf_counter())} ")
  return str


startTime = time.perf_counter()
imgName = "magala_small.png" # Filename
img = Image.open(imgName)  # Can be many different formats. Currently we support only RGBA images!
pixels = np.asarray(img) # Convert the image data to an numpy array
#pixels = np.array(img).reshape((img.height, img.width, 4)).astype(np.uint8)
print(imgName, img.format, img.size, img.mode)  # Print the name, format, size and color mode

cores = multiprocessing.cpu_count() #//2
rowsPerCore = img.height // cores
distributed = rowsPerCore * cores
loss = img.height - distributed

pool = ThreadPool(processes=cores)

print(f"Distributing workload on {cores} threads a {rowsPerCore} rows per core")

tasks = []
for c in range(cores):
  to = (rowsPerCore * (c + 1))
  if c + 1 == cores:
    to = to + loss
  tasks.append(pool.apply_async(getDivForPixels, (pixels, rowsPerCore * c, to, img.width, c)))

return_val = ""
for t in tasks:
  return_val += t.get()

print("Writing stylesheet")
createStyleFile(img.size)

print("Writing html file")
createImageFile(return_val, imgName)

print("Finished!")
print(f"Programm finished {img.height * img.width} pixel in {getTimeDifference(startTime, time.perf_counter())}")
