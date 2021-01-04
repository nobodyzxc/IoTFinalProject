import sys
from PIL import ImageFont, ImageDraw, Image

plate = "1113-GB" if len(sys.argv) < 2 else sys.argv[1]

def gen_plate(plate, output):
    image = Image.new('RGB', (300, 150), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    # use a truetype font
    font = ImageFont.truetype("reg-plate.ttf", 75)
    draw.text((10, 37.5), plate, (0, 0, 0), font=font)
    if output:
        image.save(plate + '.png')
    else:
        output = io.BytesIO()
        img.save(output, format='png')
        return output.getvalue()

gen_plate(plate, plate + '.png')
