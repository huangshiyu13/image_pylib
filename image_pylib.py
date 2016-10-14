import inspect
import os
from PIL import Image,ImageDraw,ImageFont
import numpy as np
import time
import math
import random

class BBX:
    def __init__(self):
        pass
    def str2bbx(self,str):
        chrs = str.split(' ')

        self.name = chrs[0]
        
        self.x = int(chrs[1])
        self.y = int(chrs[2])
        self.w = int(chrs[3])
        self.h = int(chrs[4])
        self.score=float(0)

    def resize(self, scale,x_d,y_d):
        self.x = int(self.x*scale)+x_d
        self.y = int(self.y*scale)+y_d
        self.w = int(self.w*scale)
        self.h = int(self.h*scale)

    
        
        

class IMGLIB:
    def __init__(self):
        pass
    def setBBXs(self,bboxs,name0):
        self.bbxs = []
        for bbox in bboxs:
            bbx = BBX()
            bbx.name = name0
            bbx.x = int(bbox[0])
            bbx.y = int(bbox[1])
            bbx.w = int(bbox[2])
            bbx.h = int(bbox[3])
            bbx.score = bbox[4]
            self.bbxs.append(bbx)

    def showBBXs(self):
        self.drawBox()
        self.img.show()
    def savaBBXs(self,fileName):
        f = open(fileName,'w')
        f.write('% bbGt version=3\n')
        for bbx in self.bbxs:
            f.write('%s %d %d %d %d 0 0 0 0 0 0 0\n'%(bbx.name,bbx.x,bbx.y,bbx.w,bbx.h))
        f.close()

    def drawOneBox(self,bbx):
        x = bbx.x
        y = bbx.y
        w = bbx.w
        h = bbx.h
        line1 = ((x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y))
        
        self.draw.line( line1, fill=(255,0,0))  
        
        font = ImageFont.truetype("OpenSans-Regular.ttf", 20)
        self.draw.text((x,y-25),bbx.name+' '+str(bbx.score), fill=(255,0,0),font=font)  
         

    def drawBox(self):
        self.draw = ImageDraw.Draw(self.img)  
        for bbx in self.bbxs:
            self.drawOneBox(bbx)

    def read_img(self, fileName):
        self.img = Image.open(fileName)

    def read_ano(self, fileName):
    
        f = open(fileName,'r')  
        lines = f.readlines()
        self.bbxs = []
        for line in lines[1:]:
            nbbx = BBX()
            nbbx.str2bbx(line)
            self.bbxs.append(nbbx)  
        
        #self.img.show()

    def resizeBBXs(self,r,x_d,y_d):
        for bbx in self.bbxs:
            bbx.resize(r,x_d,y_d)

    def resize(self, width, height,scale = 1.0):
        o_width, o_height = self.img.size
        t_width = int(width * scale)
        t_height= int(height* scale)

        o_ratio = o_width/float(o_height)
        n_ratio = width/float(height)
        
        if o_ratio > n_ratio:
            re_ration = t_width/float(o_width)
            a_height = int(re_ration*o_height)
            a_width = t_width
            self.img = self.img.resize((a_width,a_height),Image.ANTIALIAS)
        else:
            re_ration = t_height/float(o_height)
            a_width = int(re_ration*o_width)
            a_height = t_height
            self.img = self.img.resize( (a_width,a_height),Image.ANTIALIAS)

        self.x_d = random.randint(0, abs(a_width-width) )
        self.y_d = random.randint(0, abs(a_height-height) )
        imgNew = Image.new("RGB", (width, height), "black")

        box = (0,0,a_width,a_height) 
        region = self.img.crop(box) 
        
        imgNew.paste(region, (self.x_d,self.y_d) )
        self.img = imgNew
        self.resizeBBXs(re_ration,self.x_d,self.y_d)
        # self.drawBox()

    def save_img(self, imgName):
        self.img.save(imgName)

if __name__ == '__main__':
    
    imageName = '23.jpg'
    anoName = '23.txt'
    saveImgName= '23_resized.jpg'
    saveAnoName ='23_resized.txt'
    imgWidth = 960
    imgHeight= 720
    imglib = IMGLIB()

    imglib.read_img(imageName)
    imglib.read_ano(anoName)
    imglib.resize(imgWidth,imgHeight,0.85)
    imglib.drawBox()
    imglib.save_img(saveImgName)
    imglib.savaBBXs(saveAnoName)
    
