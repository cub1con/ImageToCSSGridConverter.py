#hello <3
#HI !!!

import multiprocessing
from multiprocessing.pool import ThreadPool
from PIL import Image

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


def fillTemplate(template, key, content):
  return template.replace(key, content)


def getTemplate(templateName):
  return open(templateName).read()


def writeTemplate(template, content):
  open('build/' + template, 'w').write(content)

def getDivForPixels(pixels, fromH, toH, width, threadId):
  print(f"Creating thread {threadId} from {fromH} to {toH}")
  str = ""
  for h in range(fromH, toH):
    print(f"T{threadId}: {h}", flush=True)
    for w in range(width):
      #print(f"h: {h} | w: {w}")
      #r, g, b, a = img.getpixel((w, h))      
      r, g, b, a = pixels[w, h]
      if a == 0:
        print(f"Skipped {w, h}")  
        continue

      str = str + (
        f"<div style=\"background-color:rgba({r},{g},{b},{a});grid-column:{w+1}/{w+2};grid-row:{h+1}/{h+2}\"></div>\n"
      )
  return str

imgName = "magala_small.png"
img = Image.open(imgName)  # Can be many different formats.
pixels = img.load()
print(img.format, img.size, img.mode)  # Get the format, size and color mode

cores = multiprocessing.cpu_count() #//2
rowsPerCore = img.height // cores
distributed = rowsPerCore * cores
loss = img.height - distributed

pool = ThreadPool(processes=cores)

tasks = []
for c in range(cores):
  to = (rowsPerCore * (c + 1))
  if c + 1 == cores:
    to = to + loss
  tasks.append(pool.apply_async(getDivForPixels, (pixels, rowsPerCore * c, to, img.width, c)))

return_val = ""
for t in tasks:
  return_val += t.get()

createStyleFile(img.size)
createImageFile(return_val, imgName)
