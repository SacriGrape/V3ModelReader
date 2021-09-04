from wand.image import Image
from wand.display import display

with Image(filename='test.png') as image:
    with image.clone() as clone:
        clone.depth = 1
        clone.edge(0.1)
        clone.save(filename="edge2.jpg")
