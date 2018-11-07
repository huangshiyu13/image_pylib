import inspect
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time
import math
import random



def safeInt(ss):
    return int(float(ss))

class BBX:
    def __init__(self):
        pass

    def str2bbx(self, str):
        chrs = str.split(' ')

        self.name = chrs[0]

        self.x = safeInt(chrs[1])
        self.y = safeInt(chrs[2])
        self.w = safeInt(chrs[3])
        self.h = safeInt(chrs[4])
        self.score = float(chrs[5])

    def str2bbx_true(self, str):
        chrs = str.split(' ')

        self.name = chrs[0]

        self.x = safeInt(chrs[1])
        self.y = safeInt(chrs[2])
        self.w = safeInt(chrs[3])
        self.h = safeInt(chrs[4])
        self.score = 1

    def resize(self, scale, x_d, y_d):
        self.x = safeInt(self.x * scale) + x_d
        self.y = safeInt(self.y * scale) + y_d
        self.w = safeInt(self.w * scale)
        self.h = safeInt(self.h * scale)



class COLOR_CONF:
    def __init__(self,names = None,default_color = (255,0,0), default_font_size = 12, line_width = 1):
        self.colors = {}
        if names is not None:
            self.generate_colors(names)
        self.default_color = default_color
        self.default_font_size = default_font_size
        self.line_width = line_width
    def set_color(self,name,color):
        self.colors[name] = color

    def generate_colors(self,names):
        for i in range(len(names)):
            self.colors[names[i]] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def get_color(self,name):
        if name in self.colors:
            return self.colors[name]
        else:
            return self.default_color

class IMGLIB:
    def __init__(self,color_conf = None):
        if color_conf is None:
            default_color = (255,0,0)
            self.color_conf = COLOR_CONF(default_color=default_color)
        else:
            self.color_conf = color_conf

        FontData = os.path.join(os.path.dirname(os.path.realpath(__file__)), "OpenSans-Regular.ttf")
        self.font = ImageFont.truetype(FontData, self.color_conf.default_font_size)

    def setBBXs(self, bboxs=None, names=None):
        self.bbxs = []
        for i, bbox in enumerate(bboxs):

            bbx = BBX()

            if names == None:
                bbx.name = None
            else:
                bbx.name = names[i]
            bbx.x = safeInt(bbox[0])
            bbx.y = safeInt(bbox[1])
            bbx.w = safeInt(bbox[2])
            bbx.h = safeInt(bbox[3])
            bbx.score = bbox[4]
            self.bbxs.append(bbx)

    def showBBXs(self):
        self.drawBox()
        self.img.show()

    def saveBBXs(self, fileName):
        f = open(fileName, 'w')
        for bbx in self.bbxs:
            f.write('%s %d %d %d %d %f\n' % (bbx.name, bbx.x, bbx.y, bbx.w, bbx.h, bbx.score))
        f.close()

    def drawOneBox(self, bbx, thr=-1.0, showName=False):
        if bbx.score >= thr:
            x = bbx.x
            y = bbx.y
            w = bbx.w
            h = bbx.h
            # print x,y,w,h
            line1 = ((x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y))

            fill_color = self.color_conf.get_color(bbx.name)
            # print line1
            # print fill_color
            # print self.color_conf.line_width
            self.draw.line(line1, fill=fill_color,width=self.color_conf.line_width)

            if bbx.name == None or showName == False:
                self.draw.text((x+self.color_conf.line_width, y), str(bbx.score), fill=fill_color, font=self.font)
            else:
                self.draw.text((x+self.color_conf.line_width, y), bbx.name + ' ' + str(bbx.score), fill=fill_color, font=self.font)

    def drawOneBoxTrue(self, bbx, showName=False):
        x = bbx.x
        y = bbx.y
        w = bbx.w
        h = bbx.h
        line1 = ((x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y))
        fill_color = self.color_conf.get_color(bbx.name)
        self.draw.line(line1, fill=fill_color,width=self.color_conf.line_width)
        if bbx.name == None or showName == False:
            self.draw.text((x+self.color_conf.line_width, y), 'True', fill=fill_color, font=self.font)
        else:
            self.draw.text((x+self.color_conf.line_width, y), bbx.name + '_True', fill=fill_color, font=self.font)

    def drawBox(self, thr=-1.0, showName=True, show_true = True):
        self.draw = ImageDraw.Draw(self.img)
        for bbx in self.bbxs:
            self.drawOneBox(bbx, thr, showName)

        if show_true and hasattr(self,'bbxs_true'):
            for bbx in self.bbxs_true:
                self.drawOneBoxTrue(bbx, showName)

    def read_img(self, fileName):
        self.img = Image.open(fileName).convert('RGB')

    def read_gray_img(self, fileName):
        self.img = Image.open(fileName).convert('L')

    def read_ano(self, fileName):

        f = open(fileName, 'r')
        lines = f.readlines()
        self.bbxs = []
        for line in lines[:]:
            nbbx = BBX()
            nbbx.str2bbx(line)
            self.bbxs.append(nbbx)

    def read_ano_true(self, fileName):

        f = open(fileName, 'r')
        lines = f.readlines()
        self.bbxs_true = []
        for line in lines[:]:
            nbbx = BBX()
            nbbx.str2bbx_true(line)
            self.bbxs_true.append(nbbx)

    def resizeBBXs(self, r, x_d, y_d):
        for bbx in self.bbxs:
            bbx.resize(r, x_d, y_d)

    def resize(self, width, height, scale=1.0):
        o_width, o_height = self.img.size
        t_width = safeInt(width * scale)
        t_height = safeInt(height * scale)

        o_ratio = o_width / float(o_height)
        n_ratio = width / float(height)

        if o_ratio > n_ratio:
            re_ration = t_width / float(o_width)
            a_height = safeInt(re_ration * o_height)
            a_width = t_width
            self.img = self.img.resize((a_width, a_height), Image.ANTIALIAS)
        else:
            re_ration = t_height / float(o_height)
            a_width = safeInt(re_ration * o_width)
            a_height = t_height
            self.img = self.img.resize((a_width, a_height), Image.ANTIALIAS)

        self.x_d = random.randint(0, abs(a_width - width))
        self.y_d = random.randint(0, abs(a_height - height))
        imgNew = Image.new("RGB", (width, height), "black")

        box = (0, 0, a_width, a_height)
        region = self.img.crop(box)

        imgNew.paste(region, (self.x_d, self.y_d))
        self.img = imgNew
        if hasattr(self,'bbxs'):
            self.resizeBBXs(re_ration, self.x_d, self.y_d)
        # self.drawBox()

    def cleanAno(self, w0, h0):
        newBBXS = []
        for bbox in self.bbxs:
            if bbox.x >= 0 and bbox.x <= w0 and bbox.y >= 0 and bbox.y <= h0 and bbox.w >= 20 and bbox.w <= w0 and bbox.h >= 30 and bbox.h <= h0:
                bbx = BBX()
                bbx.name = bbox.name
                bbx.x = bbox.x
                bbx.y = bbox.y
                bbx.w = bbox.w
                bbx.h = bbox.h
                bbx.score = bbox.score
                newBBXS.append(bbx)
        self.bbxs = newBBXS

    def save_img(self, imgName):
        self.img.save(imgName)

    def pureResize(self, width, height):
        re_ration = float(width)/self.img.size[0]
        self.img = self.img.resize((width, height), Image.ANTIALIAS)
        if hasattr(self,'bbxs'):
            self.resizeBBXs(re_ration, 0, 0)

    def flip(self, width):
        self.img = self.img.transpose(Image.FLIP_LEFT_RIGHT)
        newBBXS = []
        for bbox in self.bbxs:
            bbox.x = width - bbox.x - bbox.w
            newBBXS.append(bbox)
        self.bbxs = newBBXS



if __name__ == '__main__':
    pass

