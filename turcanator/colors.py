import readmidi

red = (255,0,0)
gold = (200,100,10)
green = (50, 250, 25)
blue = (20, 50, 255)
blue2= (60, 200, 255)
brackcolor = (0xFF,0x99,0x33)

colormap = {
        readmidi.PRESS : blue,
        readmidi.HOLD  : blue2,
}

class dim:
    white = [150,150,150]
    black = [100,100,100]
    white = [0xBB, 0xBB, 0xBB]
    black = [0xAA, 0xAA, 0xAA]


class bright:
    white = [255,255,255]
    black = [15,15,15]


class playing:
    white = [0xFF, 0xCC, 0x00]
    black = [0xFF, 0x99, 0x33]


def keycolor(palette, keyNum):
    if keyNum % 12 in (1, 3, 6, 8, 10):
        return palette.black
    else:
        return palette.white
    
def colors(keys):
    res = {}
    for k,v in enumerate(keys):
        res[k] = colormap.get(v)
    return res
