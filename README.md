image_pylib
==========
This repository intents to build a general image processing python library. This is for personal usage.

## Usage
- have a look at showLable.py


## API
- read_img: read in a image
- read_ano:read in the annotation
- drawBox(thr=-1.0, showName = False): draw the boxes in annotation onto the image. `thr` is the threshold for the bounding box's score, `showName` means showing the class names
- save_img(imgName): save image to the path 'imgName'
- pureResize(width, height): resize image without padding 
- cleanAno(w0, h0): remove the bad boxes
- resize(width, height, scale=1.0): resize image with random padding
- resizeBBXs(r, x_d, y_d): resize boxes

