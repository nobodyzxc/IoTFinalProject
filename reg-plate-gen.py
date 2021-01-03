import sys
from PIL import ImageFont, ImageDraw, Image

image = Image.new('RGB', (300, 150), (255, 255, 255))

plate = "1113-GB" if len(sys.argv) < 2 else sys.argv[1]

draw = ImageDraw.Draw(image)
# use a truetype font
font = ImageFont.truetype("reg-plate.ttf", 75)
draw.text((10, 37.5), plate, (0, 0, 0), font=font)

# image.show()

image.save(plate + '.png')
