import image_test

# Dataset colorlabel names.
_ADE20K = 'ade20k'
_CITYSCAPES = 'cityscapes'
_MAPILLARY_VISTAS = 'mapillary_vistas'
_PASCAL = 'pascal'

#Model names
_Pascal_deeplab = 'models/deeplabv3_mnv2_dm05_pascal_trainval_2018_10_01.tar.gz'
_Pascal_mobilenet = 'models/deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz'

_Cityscapes_mn = 'models/deeplabv3_mnv2_cityscapes_train_2018_02_05.tar.gz'
_Cityscapes_mn_natrous = 'models/mobilev2_restride16_100000.tar.gz'
_Cityscapes_mn_nende = 'models/cityscape90000.tar'
_Cityscapes_mn_nende_natrous = 'models/mobilev2_noatandde60000.tar.gz'
_Cityscapes_mn_size321 = 'models/mobilev2_restride16_100000.tar.gz'
_Cityscapes_mn_stride32 = 'models/mobilev2_restride32_100000.tar.gz'

#single image inference     : model_name, picure, label_color, output_name, output_name_color
#image_test.image_inference(_Pascal_mobilenet, 'test_data/dog_person.jpg', _PASCAL, 'results/test', 'results/test_color')

#video inference            : (0 -> from camera) model_name, video, label_color, output_name
#image_test.video_inference(_Cityscapes_mn_size321,'test_data/short.mp4' , _CITYSCAPES, "results/testvideo")

#video inference with ball  : (0 -> from camera) model_name, video, label_color, output_name
image_test.video_inference_withball(_Cityscapes_mn_size321,'test_data/short.MP4' , _CITYSCAPES, "results/testvideo1")

#image inference with ball  : model_name, picure, label_color, output_name_color
#image_test.image_inference_withball(_Cityscapes_mn_size321, 'test_data/Norm.png', _CITYSCAPES,'results/test_color')
