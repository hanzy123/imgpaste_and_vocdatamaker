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
python paste_img.py arg1 arg2 arg3 arg4 arg5 arg6

arg1:Where u want to save your paste_images
arg2:Where u saving your logo_examples
arg3:Where u saving your bg_images
arg4:Where u want to save your position_info.txt
arg5:Which Image size ratio Lower bound u want to set
arg6:Which Image size ratio up bound u want to set
arg7:How many pictures per logo u want to make

python paste_img.py /Users/mac/logo_detection/paste_img/new_img /Users/mac/logo_detection/paste_img/0_logo_dataset /Users/mac/logo_detection/dataset/FlickrLogos-32/classes/jpg/no-logo /Users/mac/logo_detection/paste_img/position_info.txt 0.2 0.5 100 
```

### generate_vocdataset.py
生成voc数据集

合成的图片存储目录格式
```
|---new_img
| |---adidas_0.jpg
| |---adidas_1.jpg
| |---adidas_2.jpg
| |---adidas_3.jpg
| |...
```

生成voc数据集类似的
`test.txt`,`train.txt`,`trainval.txt`,`val.txt`
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
voc_type_xml.py 参数：
```
```
python voc_type_xml.py arg1 arg2 arg3 

arg1:where do u want to save your xmls

arg2:where your images are

arg3:where your position_info_txt is

arg4:where_save_trainval.txt,train.txt,val.txt,test.txt

arg5:trainval_rate

arg6:train_rate
```
python voc_type_xml.py /Users/mac/logo_detection/paste_img/Annotations /Users/mac/logo_detection/paste_img/new_img /Users/mac/logo_detection/paste_img/position_info.txt /Users/mac/logo_detection/paste_img/ImageSets/Main 0.5 0.5