#import weblib
import piddlePIL
from piddlePIL import *

timeX = 100
timeY = 25
timeH = 20
timeW = 80
maxX = timeX + (timeW * 7)
maxY = timeY + (timeY * 14)
canvas = c = PILCanvas(size=(maxX+1,maxY+1))


## begin and end times (in weeks)
now = 4
tasks = [
    {"label":"zikeshop",       "bars": [(0,   3,   cornflower)]},
    {"label":"admin stuff",    "bars": [(3,   3.5, cornflower),
                                        (16,  18,  cornflower)]},
    {"label":"zike docs",      "bars": [(5,   8,   lightblue),
                                        (18,  20,  cornflower)]},
    {"label":"blogdrive",      "bars": [(5,   8,   lightblue),
                                        (14,  16,  cornflower)]},
    {"label":"ransacker",      "bars": [(4,   4.5, cornflower)]},
    {"label":"zs ultra",       "bars": [(10,  12,  cornflower)]},
    {"label":"ASI 20 hours",   "bars": [(0,   10,  red)]},
    {"label":"ASI 20 hours",   "bars": [(0,   10,  gold)]},
    {"label":"bug tracker",    "bars": [(3.5, 4,   cornflower)]},
    {"label":"zikestuff",      "bars": [(4.5, 5,   cornflower)]},
    {"label":"linkwatcher",    "bars": [(8,   8.5, cornflower),
                                        (12,  14,  cornflower)]},
    {"label":"body-for-life",  "bars": [(10,  26,  gold)]},
    {"label":"manifestation",  "bars": [(16,  20,  red)]},
    {"label":"monty",          "bars": [(20,  22,  red)]},
    
    ]


## shading:
c.drawRect(0,0,timeX,maxY, fillColor=gainsboro)
c.drawRect(0,0,maxX,timeY, fillColor=gainsboro)
c.drawRect(0,0,timeX,timeY, fillColor=silver)

## the grid goes on bottom:
for x in range(timeX,maxX,timeW):
    c.drawLine(x,0,x,maxY)

for y in range(timeY,maxY,timeH*2):
    c.drawLine(0,y, maxX,y)

## draw in the "past" shading:
c.drawRect(timeX,timeY, timeX + (now * (timeW/4)), maxY,
           edgeColor=slategray, fillColor=slategray)

## draw the charts:
for i in range(len(tasks)):

    c.drawString(tasks[i]["label"], 5, timeY + 15 + (i * timeH),
                 Font(face="sansserif",size=12,bold=1))

    for bar in tasks[i].get("bars", []):
        begin, end, color = bar
        c.drawRect(timeX + ((timeW / 4) * begin),
               timeY + (i * timeH),
               timeX + ((timeW / 4) * end),
               timeY + ((i+1) * timeH),
               edgeColor=black,
               fillColor=color)


## column titles:
times = ["feb","mar","apr","may","jun", "jul", "aug"]
for i in range(len(times)):
    c.drawString(times[i],
                 timeX + (timeW * (i+1)) - (timeW/2)-10, # roughly center it
                 20,
                 Font(face="sansserif",size=12,bold=1))

## redraw the border
c.drawRect(timeX,timeY,maxX,maxY)

## show the image

#weblib.response.contentType = "image/gif"
canvas.save("w:/gantt", format="jpg")
#weblib.response.write(open("w:/gantt.gif","rb").read())
