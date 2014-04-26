"""
#####################################
## IT 441 Computer Graphics
## Instructor:Nitin Raje
## Implemented By: Shalin Shah
## ID : 201101179
#####################################
"""

from PIL import Image
from PIL import ImageChops
from PIL import ImageFilter
import webbrowser
from PIL import ImageDraw   

def genTriangle(data, steps, update_image, k):
    '''
    The triangle and it's subtriangle is calculated here.
    '''
    # draw triangles each step through
    update_image.line((data[0], data[1]))
    update_image.line((data[1], data[2]))
    update_image.line((data[0], data[2]))
    
    # next triangle formed by connecting the midpoints of each of the sides
    x1 = (data[0][0] + data[1][0]) / 2
    y1 = (data[0][1] + data[1][1]) / 2
    
    x2 = (data[1][0] + data[2][0]) / 2
    y2 = (data[1][1] + data[2][1]) / 2
    
    x3 = (data[2][0] + data[0][0]) / 2
    y3 = (data[2][1] + data[0][1]) / 2
    
    # updates data in next recursion
    data2 = ((x1, y1), (x2, y2), (x3, y3))
    
    # loop through until step limit is reached
    k += 1
    if k <= steps:
        genTriangle((data[0], data2[0], data2[2]), steps, update_image, k)
        genTriangle((data[1], data2[0], data2[1]), steps, update_image, k)
        genTriangle((data[2], data2[1], data2[2]), steps, update_image, k)

def draw(image):
    return ImageDraw.Draw(image)

# higher steps gives more detail
# test with values of 1 to 10
steps = 6

# the three x,y data points for the starting equilateral triangle
data = ((0, 400), (400, 400), (200, 0))

# picture canvas creation uses size tuple given in data[1]
size = data[1]
picture = Image.new('1', size, color="red")
update_image = draw(picture)

# draw the triangle and calculate next triangle corner coordinates
genTriangle(data, steps, update_image, 0)

# save the final image file and then view with an image viewer
imagename = "TRIANGLE_ORIGINAL.jpg"
picture.save(imagename);

im1 = Image.open("TRIANGLE_ORIGINAL.jpg")

im2 = im1.filter(ImageFilter.BLUR)
im2.save('TRIANGLE_BLURRED.jpg',"JPEG")

ImageChops.invert(im1)
im3 = im1.filter(ImageFilter.EMBOSS)
im3.save('TRIANGLE_EMBOSSED_INVERTED.jpg',"JPEG")

