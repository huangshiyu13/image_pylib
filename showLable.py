from image_pylib import IMGLIB
import os  
import shutil
if __name__ == '__main__':
    imglib = IMGLIB()
    # imageDir = '/Users/shiyuhuang/Downloads/ATOCAR/ATOCAR_CNN/results/d_net/result2ReverseImg/800/'
    imageDir = '/Users/shiyuhuang/Downloads/ATOCAR/DATA/dangerousFinal/test/'
    # anoDir   = '../../DATA/dangerousFinal/allNowAno/'
    # anoDir   = '../../DATA/Caltech/Caltech/train/annotations/'
    # anoDir   = '../../DATA/syntheticData/new/CroppedAno/'
    anoDir   = '/Users/shiyuhuang/Downloads/ATOCAR/DATA/dangerousFinal/rpn_test_res/'

    # saveImgDir = '/Users/shiyuhuang/Downloads/ATOCAR/ATOCAR_CNN/results/d_net/result2ReverseImg/800Show/'
    saveImgDir = '/Users/shiyuhuang/Downloads/ATOCAR/ATOCAR_CNN/results/rpn/rpn_test_resShow/'
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

