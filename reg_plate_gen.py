import sys, io
from PIL import ImageFont, ImageDraw, Image

plate = "1113-GB" if len(sys.argv) < 2 else sys.argv[1]

def gen_plate(plate):
    image = Image.new('RGB', (300, 150), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    # use a truetype font
    font = ImageFont.truetype("reg-plate.ttf", 75)
    draw.text((10, 37.5), plate, (0, 0, 0), font=font)
    image.save(plate + '.png')
    return plate + '.png'

if __name__ == '__main__':
    gen_plate(plate)
