# VIZDET

[![PyPI version](https://badge.fury.io/py/vizdet.svg)](https://badge.fury.io/py/vizdet)

![CI](https://github.com/tadejsv/vizdet/workflows/CI/badge.svg)

VIZDET - VIZualization for DEtection and Tracking. This library provides a simple interface to plot detection bounding boxes and their labels on an image. It enables the use of custom fonts, allowing you to create visually pleasing detection plots.

The purpose of this library is enable detection model creators to use an out-of-the-box library for presenting and visually evaluating their detection models, focusing their time on writing the detection models instead. Main features of vizdet are:

* Easy to use, enabling you to create detection plots with ease with minimal code
* Use of custom fonts to make the plots look beautiful and write special unicode characters and characters from non-latin scipts
* Customizable graphical parameters - customize plots according to your taste
* Out of the box options cover the main usecases for object detection, as well as (multi) object tracking - just plug in the detection/tracking results from your model, and you're ready to go
* Lightweight, with the only dependency being OpenCV (and Numpy)

![Road example](_assets/example_image.png)

## Installation instructions

This module requires the freetype OpenCV module, which is not included in the PyPI repository package, so
I recommend you install the requirements with conda (create a [conda environment first](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands)):

``` sh
conda install libopencv opencv py-opencv -c conda-forge
```

From here you can install the package with pip, as usual

``` sh
pip install vizdet
```

## Quickstart

Let's create our first detection plot. Download [this image](https://github.com/tadejsv/vizdet/raw/main/tests/unit/highway.png) and place it in your working directory. Then, execute this script (you'll also need to install matplotlib to visualize the results)

``` python
import cv2
import matplotlib.pyplot as plt
from vizdet import BBoxes, InfoBox

# Prepare our detection results
boxes = [
    [1267, 762, 1418, 889],
    [1225, 604, 1327, 693],
    [1789, 682, 1919, 790],
    [1595, 389, 1726, 514],
    [1670, 416, 1820, 566],
    [904, 440, 1043, 615],
    [504, 623, 876, 1142],
    [922, 611, 1213, 1107]
]
labels = ['car', 'car', 'car', 'truck', 'truck', 'truck', 'truck', 'truck']
info_title = '# Objects'
info_desc = ['3 cars', '5 trucks']

# Read image
img = cv2.imread('highway.png')

# Prepare objects to draw
bboxes = BBoxes(font_height=40, box_thickness=5, padding=10)
infobox = InfoBox(width=250, font_height_desc=40, font_height_title=50, padding=15)

# Draw detection results on the image
bboxes.draw(img, boxes, labels=labels)
infobox.draw(img, (1650, 20), info_desc, info_title)

# Plot results
plt.imshow(img[::-1])
```

The result should be similar to the image above (but with bounding box colors being different). We drew the detection boxes, as well as an information box given some information what is on the image - all with just the detection result from `boxes` and some custom text for the information box.

All the drawing is done by the `BBoxes` and `InfoBox` classes, which offer arguments to customize the visual appearance. The default font (FiraGO) is used, but this could also be modified. Note that this looks much better than what you would get with the default OpenCV Hershey font.

The result ( `img` ) is a simply numpy array - not some custom plot object that you would get with Matplotlib or similar libraries. This enables you to further customize the image using other tools, if you would like, or to compose multiple images into a video and so on. The possibilities are endless ; )

### Labels as integers

A common situation is that your labels are actually integers, corresponding to some class names from a list. This is handled natively by vizdet. In this case your `labels` would be an integer list and you would also have a `classes` list of string class names:

``` python
labels = [0, 0, 0, 1, 1, 1, 1, 1]
classes = ['car', 'truck']
```

Then, all you need to do is to change the `bboxes` definition to

``` python
bboxes = BBoxes(
    labels_list=classes, font_height=40, box_thickness=5, padding=10
)
```

### Showing probabilities

You migh also want to display probabilities (confidences) for each object. So say that you have the probabilities in a `probs` list

``` python
probs = [0.9978, 0.9951, 0.9974, 0.9757, 0.9766, 0.9937, 0.9936, 0.9923]
```

Then, to display them on the plot just modify the ` `bboxes.draw` ` function call to

``` python
bboxes.draw(img, boxes, labels=classes, labels_conf=probs)
```

The result should look like the image below

![Road example probs](_assets/example_probs.png)

## License

This source code of this project is released under the Apache 2.0 License, which is available in the `LICENSE` file.

The project also contains the [FiraGO](https://github.com/bBoxType/FiraGO) font, which is distributed under the SIL Open Font License. The `test` directory also includes the [FiraMono](https://fonts.google.com/specimen/Fira+Mono) font, also released under the SIL Open Font License. A copy of the Open Font License is included in the `OFL.txt` file.
