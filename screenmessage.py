import pygame, colorsys

class ScreenMessage(object):

    def __init__(self,size,message,x,y,centrex,font="sawasdee",rgb=(255,255,255)):
        self.size = size
        self.rgb = rgb
        self.message = message
        self.font = pygame.font.SysFont(font, self.size, True)
        self.textwidth, self.textheight = self.font.size(message)
        self.x = x
        self.y = y
        self.centrex = centrex

    def draw(self,view,xoffset,yoffset,screen):
        if self.centrex:
            x= (xoffset*-1)+((screen["w"] - self.textwidth)//2)
        else:
            x= (xoffset*-1) + self.x - self.textwidth
        y = (yoffset*-1) + self.y - self.textheight
        text = self.font.render(self.message, 1, self.rgb)
        view.blit(text, (x,y))


class FlashingMessage(object):

    def __init__(self,size,message,x,y,centrex,flashinterval,font="sawasdee",rgb=(255,255,255)):
        ScreenMessage.__init__(self,size,message,x,y,centrex,font,rgb)
        self.flashinterval = flashinterval
        self.flashcount = flashinterval
        self.on = True

    def draw(self,view,xoffset,yoffset,screen):
        #Set x y position of text
        if self.centrex:
            x= (xoffset*-1)+((screen["w"] - self.textwidth)//2)
        else:
            x= (xoffset*-1) + self.x - self.textwidth
        y = (yoffset*-1) + self.y - self.textheight


        if self.flashcount == 0:
            if self.on:
                self.on = False
            else:
                self.on = True
            self.flashcount = self.flashinterval
        else:
            self.flashcount -= 1

        if self.on:
            text = self.font.render(self.message, 1, self.rgb)
            textrect = text.get_rect()
        else:
            #Render nothing
            text = self.font.render("", 1, self.rgb)
        view.blit(text, (x,y))


class OnScreenMessage(object):

    def __init__(self,size,message,font="comicsans",rgb=(255,0,0),grad=20,cycle=True):
        self.size = size
        self.rgb = list(rgb)
        self.message = message
        self.font = pygame.font.SysFont(font, self.size, True)
        self.textwidth, self.textheight = self.font.size(message)
        self.grad = grad
        self.cycle = cycle

    def rgbgradient(r,g,b,count):
        l = 0.299*r + 0.587*g + 0.114*b


    def draw(self,view,xoffset,yoffset,screen):
        grad = self.grad #Set gradient

        x= (xoffset*-1)+((screen["w"] - self.textwidth)//2)
        y = (yoffset*-1)+(screen["h"]//2)-(self.textheight//2)
        newrgb = self.rgb
        lstepval = -10
        while grad != 0:
            hls = colorsys.rgb_to_hls(newrgb[0],newrgb[1],newrgb[2])
            if any(c < 0 for c in colorsys.hls_to_rgb(hls[0],hls[1]+lstepval,hls[2])):
                lstepval = 10
                newrgb = colorsys.hls_to_rgb(hls[0],hls[1]+lstepval,hls[2])
            elif any(c > 255 for c in colorsys.hls_to_rgb(hls[0],hls[1]+lstepval,hls[2])):
                lstepval = -10
                newrgb = colorsys.hls_to_rgb(hls[0],hls[1]+lstepval,hls[2])
            else:
                newrgb = colorsys.hls_to_rgb(hls[0],hls[1]+lstepval,hls[2])
            text = self.font.render(self.message, 1, (newrgb[0],newrgb[1],newrgb[2]))
            #Calculate the area to draw the gradient
            textrect = text.get_rect()
            step = (textrect.height / self.grad) * grad
            view.blit(text, (x,y),(textrect.x,textrect.y,textrect.width,step))
            grad -= 1
        #Make gradient cycle
        if self.cycle:
            self.rgb = newrgb
