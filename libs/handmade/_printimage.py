import os
import sys
from .terminal import out
sys.path.append(os.path.abspath("libs"))
import imageio as iio
try:
    import numpy
except:
    raise importerror("numpy not installed ")
else:
    pass
def init_printer(self):
    self.true_color = 1
    self.color_codes = [(12,12,12),
               (197,15,31),
               (19,161,14),
               (193,156,0),
               (0,55,218),
               (136,23,152),
               (58,150,221),
               (204,204,204),
               (118,118,118),
               (231,72,86),
               (22,198,12),
               (249,241,165),
               (59,120,255),
               (180,0,158),
               (97,214,214),
               (242,242,242)]

    self.escape_codes = [40,
               41,
               42,
               43,
               44,
               45,
               46,
               47,
               100,
               101,
               102,
               103,
               104,
               105,
               106,
               107]

def closest(colors,color):
    colors = numpy.array(colors)
    color = numpy.array(color)
    try :
        distances = numpy.sqrt(numpy.sum((colors-color)**2,axis=1))
        index_of_smallest = numpy.where(distances==numpy.amin(distances))
        smallest_distance = colors[index_of_smallest]
    except:
        return [[0]]
    else:
        return index_of_smallest

def print_image_to_screen(self, path, top_offset=0):
    size = os.get_terminal_size()
    height = size.lines - top_offset
    width = size.columns/2
    
    image = iio.imread(path)
    imheight, imwidth, *_ = image.shape
    
    colors = []
    if height/imheight < width/imwidth:
        heightprint = height
        widthprint = int(heightprint*(imwidth/imheight)*2)
    else:
        widthprint = size.columns
        heightprint = int(widthprint*(imheight/imwidth)/2)
    
    #heightprint = height
    #widthprint = height*2
    width = imwidth/widthprint
    height = imheight/heightprint

    for i in range(heightprint): # height
        for j in range(widthprint): # width
            left = (width) * j
            up = (height) * i
            right = left + (width)
            down = up + (height)
            
            pixel = image[int(up):int(down)+1, int(left):int(right)+1]
            #cv2.imshow('test', pixel)
            #cv2.waitKey(0)
            average_color = numpy.mean(pixel, axis=(0,1))
            if len(pixel) == 0:
                #print('\033[42mERROR: Empty pixel.\033[0m')
                #print(pixel, i, j, size, left, up, right, down)
                pass
            colors.append(average_color)
            if not self.true_color:
                print(f'\033[{self.escape_codes[closest(self.color_codes, list(reversed(average_color)))[0][0]]}m'+' ', end='')
            else:
                
                out(f'\x1b[48;2;{int(average_color[0])};{int(average_color[1])};{int(average_color[2])}m ')
        print('\033[0m')

