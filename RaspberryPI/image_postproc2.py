from PIL import Image
import math

def stitch_pic(imgcount):
    if imgcount == 0:
        print('None stitched')
        return
    images = []
    col = math.ceil(imgcount / 2)
    row = 0
    if imgcount < 2:
        row = 1
    else:
        row = 2
    for i in range(imgcount):
        path = './images2/image'+str(i)+'.jpg'
        images.append(Image.open(path))

    width = images[0].size[0]
    height = images[0].size[1]
    result = Image.new('RGB', (width * col, height * row))

    for i in range(len(images)):
        result.paste(im=images[i], box=((i%col) * width, math.floor(i/col) * height)) 

    result.save('./images2/results.jpg')
    return

#stitch_pic(2)
