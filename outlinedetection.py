from PIL import Image, ImageFilter
from pathlib import Path
import matplotlib.pyplot as plt

def outlinedetect(path):
    image = Image.open(path)
    rgb_image = image.convert('RGBA')
    width, height = rgb_image.size

    x_cords = []
    y_cords = []
    print('Changing colors to white...')
    for x in range(width):
        for y in range(height):
            r, g, b, a = rgb_image.getpixel((x, y))
            if ((r, g, b, a) != (0, 0, 0, 0)):
                print(f'{r} {g} {b} {a}')
                rgb_image.putpixel((x, y), (255, 255, 255, 255))
    print('Creating outline...')
    edge_image = rgb_image.filter(ImageFilter.FIND_EDGES)
    width_edge, height_edge = edge_image.size

    print('Reading image file please wait...')
    for x in range(width_edge):
        for y in range(height_edge):
            r, g, b, a = edge_image.getpixel((x, y))
            if ((r, g, b, a) != (0, 0, 0, 0)):
                x_cords.append(x)
                y_cords.append(y)
                print(f'{r} {g} {b} {a}')
                edge_image.putpixel((x, y), (255, 255, 255, 255))

    return x_cords, y_cords
    '''
    # plotting points as a scatter plot
    plt.scatter(x_cords, y_cords, label= "star", color= "green",
                marker= "*", s=30)

    # x-axis label
    plt.xlabel('x - axis')
    # frequency label
    plt.ylabel('y - axis')
    # plot title
    plt.title('My scatter plot!')
    # showing legend
    plt.legend()
    
    # function to show the plot
    plt.show()
    '''