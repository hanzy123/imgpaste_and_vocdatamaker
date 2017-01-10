# logo_detection
## usage
### paste_img.py
使用拼图的方式将logo贴在背景图片上生成数据集(类似BelgaLogos)

logo图片文件夹目录(图片后缀名需为png..好吧这里贪图方便写的渣了..)
```
|---0_logo_dataset
| |---adidas
| | |---adidas_0.png
| | |---adidas_1.png
| | |---adidas_2.png
| |---aldi
| | |---aldi_0.png
| | |---aldi_1.png
| | |---aldi_2.png
| | | ...
```
背景图片文件夹目录
```
|---no-logo
| |---160204.jpg
| |---242289.jpg
| |---263862.jpg
| |---292113.jpg
| |...
```

```
paste_img.py 参数：
```
```
python paste_img.py arg1 arg2 arg3 arg4

arg1:where u want to save your paste_images

arg2:where u saving your logo_examples

arg3:where u saving your bg_images

arg4:where u want to save your position_info.txt

python paste_img.py /Users/mac/logo_detection/paste_img/new_img /Users/mac/logo_detection/paste_img/0_logo_dataset /Users/mac/logo_detection/dataset/FlickrLogos-32/classes/jpg/no-logo /Users/mac/logo_detection/paste_img/position_info.txt
```

### voc_type_xml.py
生成voc数据集类似的xml文件用来训练

合成的图片存储目录格式
```
|---new_img
| |---adidas_0.jpg
| |---adidas_1.jpg
| |---adidas_2.jpg
| |---adidas_3.jpg
| |...
```
```
voc_type_xml.py 参数：
```
```
python voc_type_xml.py arg1 arg2 arg3

arg1:where do u want to save your xmls

arg2:where your images are

arg3:where your position_info_txt is

python voc_type_xml.py /Users/mac/logo_detection/paste_img/Annotations /Users/mac/logo_detection/paste_img/new_img /Users/mac/logo_detection/paste_img/position_info.txt
```
### make_voc_text.py
生成voc数据集类似的
```
test.txt,train.txt,trainval.txt,val.txt
```
存储xml文件的文件夹格式
```
|---Annotations
| |---adidas_0.xml
| |---adidas_1.xml
| |---adidas_2.xml
| |---adidas_3.xml
| |...
```
```
make_voc_text.py 参数：
```
```
python make_voc_text.py arg1 arg2 arg3 arg4

arg1:in which file u saving your xmls

arg2:in which file u want to save your txts

arg3:the trainval_rate is

arg4:the train_rate is

python make_voc_text.py /Users/mac/logo_detection/paste_img/Annotations /Users/mac/logo_detection/paste_img/ImageSets/Main 0.5 0.5
```