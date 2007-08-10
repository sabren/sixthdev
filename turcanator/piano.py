
import sys, pygame


#def drawKey(surf, keyNum, shade):
#    pygame.draw.rect(surf, [200,150,100]

#def drawGenericPiano(surf, x, y, keyw, keyh, keycount, shades={}):
#    for keyNum in range(keycount):
#        drawKey(surf, keyNum, shades.get(keyNum) or )


class Rectangle(object):
    def __init__(self, w,h, color=None, x=0,y=0):
        self.rect = (x,y,w,h)
        self.color = color or self.defaultColor()
    def defaultColor(self):
        return (255,255,255)
    def translate(self, dx,dy):
        x,y,w,h = self.rect
        return self.__class__(w, h, self.color, x+dx, y+dy)
    def shade(self, color):
        x,y,w,h = self.rect
        return self.__class__(w, h, color, x, y)
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(*self.rect))
        

class WhiteKey(Rectangle):
    def draw(self, surface):
        x,y,w,h = self.rect
        pygame.draw.rect(surface, [200,200,200], pygame.Rect(*self.rect))
        pygame.draw.rect(surface, self.color, pygame.Rect(x,y,w-1,h))

class BlackKey(Rectangle):
    def defaultColor(self):
        return [0,0,0]
    def draw(self, surface):
        x,y,w,h = self.rect
        pygame.draw.rect(surface, [255,255,255], pygame.Rect(x-1,y,w+1,h))
        pygame.draw.rect(surface, [150,150,150], pygame.Rect(x+2,y,w-4,h))
        pygame.draw.rect(surface, self.color, pygame.Rect(x,y,w,h*2.0/3.0))


def keyClass(keyNum):
    if keyNum % 12 in (1, 3, 6, 8, 10):
        return BlackKey
    else:
        return WhiteKey


pygame.init()
screen = pygame.display.set_mode([700, 300])
screen.fill([100,100,200])


#drawGenericPiano(screen, 10, 10, 5, 10, 60)

red = (255,0,0)
gold = (255,180,10)
green = (20, 250, 25)

colors = {4: red, 12:red,14:gold, 29:green, 31:green, 34:green}
Rectangle(602,28,[0,0,0],49,49).draw(screen)
keyw, keyh = 10, 25
for k in range(60):
    (keyClass(k)(keyw,keyh)
     .shade(colors.get(k))
     .translate(50+keyw*k,50)
     .draw(screen))


pygame.display.flip()



# -----
while pygame.event.poll().type != pygame.QUIT:
    pygame.time.delay(10)

pygame.display.quit()

