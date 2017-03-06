from image_pylib import IMGLIB
import os  
import shutil
if __name__ == '__main__':
    imglib = IMGLIB()
   
    imageDir = 'image/'
   
    anoDir   = 'ano/'

    
    saveImgDir = 'saveDir/'
    thr = 0.99
    imageNames = []
    
    if os.path.isdir(saveImgDir):
        shutil.rmtree(saveImgDir)
    os.mkdir(saveImgDir)

    for file in os.listdir(imageDir):
        file_path = os.path.join(imageDir, file)  
        if os.path.isfile(file_path) and os.path.splitext(file_path)[1]=='.jpg':
            nameNow = os.path.splitext(file)[0]
            imageName = imageDir +'/'+nameNow+'.jpg'
            anoName = anoDir +'/'+nameNow+'.txt'
            saveImgName= saveImgDir +'/'+nameNow+'.jpg'
            imglib.read_img(imageName)
            imglib.read_ano(anoName)
            imglib.drawBox(thr,False)
            imglib.save_img(saveImgName)
            print imageName

