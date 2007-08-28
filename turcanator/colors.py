import readmidi

HIT = 5555555555553333333333222222222
MISS = 92837492387493287492387492374


red = (255,0,0)
gold = (200,100,10)
green = (50, 250, 25)
blue = (20, 50, 255)
blue2= (50, 80, 255)
brackcolor = (0xFF,0x99,0x33)

colormap = {
        readmidi.PRESS : blue,
        readmidi.HOLD  : blue2,
        HIT : green,
        MISS : red,
}


# wfade and bfade are colors for
# when only one hand is being used

defaultFade = [0, 0, 0]


# alternating dim rows:




class dimA:
    white = [0xB3, 0xB3, 0xB3]
    black = [0x8e, 0x8e, 0x8e]
    #wfade = [0x53, 0x53, 0x53]
    wfade = bfade = defaultFade

class dimB:
    white = [0xc5, 0xc5, 0xc5]
    black = [0xa0, 0xa0, 0xa0]
    #wfade = [0x53, 0x53, 0x53]    
    wfade = bfade = defaultFade
    #wfade = [0x95, 0x95, 0x95]
    #bfade = [0x70, 0x70, 0x70]

class midiCursor:
    white = [255,255,255]
    black = [15,15,15]
    wfade = bfade = defaultFade


class computerCursor:
    white = [0xFF, 0xCC, 0x00]
    black = [0xFF, 0x99, 0x33]
    wfade = bfade = defaultFade


def keycolor(palette, keyNum, fade):
    if keyNum % 12 in (1, 3, 6, 8, 10):
        if fade: return palette.bfade 
        else: return palette.black 
        
    else:
        if fade: return palette.wfade 
        else: return palette.white

    
def colors(keys):
    res = {}
    for k,v in enumerate(keys):
        res[k] = colormap.get(v)
    return res
