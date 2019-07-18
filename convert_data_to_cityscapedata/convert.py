from pathlib import Path
import convert_color_to_label as cl
import os,glob
from os import rename
from shutil import copyfile

#get path to photos
path = Path().absolute()
original_path = str(path).replace('\\', '/')+'/original/'
color_path = str(path).replace('\\', '/')+'/color/'
#test_path = str(path).replace('\\', '/')+'/test/'
store_path_image = str(path).replace('\\', '/')+'/tsinghua1/'
store_path_label = str(path).replace('\\', '/')+'/tsinghua2/'

#get files from folders
#seg_images
num = 0
for filename in sorted(glob.glob(os.path.join(color_path, '*.png'))):
    print(filename)
    #rename(filename, filename.replace(' 'and'.png','')+'_labelTrainIds.png')
    train, error = cl.convert_to_trainID(filename)
    copyfile(filename, store_path_label+'tsinghua_'+str(num)+'_gtFine_color.png')
    train.save(store_path_label+'tsinghua_'+str(num)+'_gtFine_labelTrainIds.png')
    #error.save(store_path+'elsalab_'+str(num)+'_error.png')
    num = num+1
#original images
num = 0
for filename in sorted(glob.glob(os.path.join(original_path, '*.png'))):
    print(filename)
    #rename(filename, filename.replace(' 'and'.png','')+'_labelTrainIds.png')
    copyfile(filename, store_path_image+'tsinghua_'+str(num)+'_leftImg8bit.png')
    num = num+1