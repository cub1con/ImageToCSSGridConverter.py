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

# Writes the html file with imgName as filenmae
def createImageFile(image, imgName):
  name = "template.html"
  file = getTemplate(name)
  file = file.replace("%REPLACEIMG%", image)
  file = file.replace("%REPLACENAME%", imgName)
  writeTemplate(f"{imgName}.html", file)

# Writes the css file with the size parameters 
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

# Gets the text for the defined pixelspace
def getDivForPixels(pixels, fromH, toH, width, threadId):
  print(f"Creating thread {threadId} from {fromH} to {toH}")
  startTime = time.perf_counter()
  str = ""
  for h in range(fromH, toH):
    #print(f"T{threadId}: {h}", flush=True)
    for w in range(width):
      #print(f"h: {h} | w: {w}")
      #r, g, b, a = img.getpixel((w, h))      
      r, g, b, a = pixels[h, w]
      if a == 0:
        #print(f"Skipped {h, w}")  
        continue

      hexCode = f"#{r:02X}{g:02X}{b:02X}{a:02X}"
      str += f"<div style=\"background:{hexCode};grid-column:{w+1};grid-row:{h+1}\"></div>"
      #str += f"<div style=\"background-color:rgba({r},{g},{b},{a});grid-column:{w+1};grid-row:{h+1}\"></div>"
  
  print(f"Thread {threadId} finished {(toH - fromH) * width} pixel in {getTimeDifference(startTime, time.perf_counter())}")
  return str

# Program start
startTime = time.perf_counter()

imgName = "magala_small.png" # Filename
img = Image.open(imgName)  # Can be many different formats. Currently we support only RGBA images!
pixels = np.asarray(img) # Convert the image data to an numpy array
#pixels = np.array(img).reshape((img.height, img.width, 4)).astype(np.uint8)
print(imgName, img.format, img.size, img.mode)  # Print the name, format, size and color mode

cores = multiprocessing.cpu_count() # Get amount of cores
rowsPerThread = img.height // cores # Calculate rows per thread
lostPixel = img.height - (rowsPerThread * cores) # Calculate the rows lost by float division

print(f"Distributing workload on {cores} threads a {rowsPerThread} rows per core")

pool = ThreadPool(processes=cores) # Create a threadpool 
tasks = []
for c in range(cores): # Create for every core a thread
  to = (rowsPerThread * (c + 1)) # Calculate the last row
  if c + 1 == cores: # Check if this is the last core
    to += lostPixel # Add the lostPixel to the last thread
  tasks.append(pool.apply_async(getDivForPixels, (pixels, rowsPerThread * c, to, img.width, c))) # Add new job to the pool with information to calculate

return_val = ""
for t in tasks: # Get the return value of all jobs
  return_val += t.get()

print("Writing stylesheet")
createStyleFile(img.size)

print("Writing html file")
createImageFile(return_val, imgName)

print("Finished!")
print(f"Programm finished {img.height * img.width} pixel in {getTimeDifference(startTime, time.perf_counter())}")
