from PIL import Image, ImageDraw, ImageFont
import numpy as np

dic = {
    "radiant_building_damage": {
        "x": 234.91,
        "y": 987.95,
        "width": 86.18,
        "height": 33.29,
    }
}


img = Image.new("RGBA", (1920, 1080), color=(25, 25, 25, 255))
net = Image.open("data/temp/net.png")

new_width = 1000
new_height = int(new_width * net.height / net.width)
net = net.resize((new_width, new_height), Image.ANTIALIAS)

img.paste(net, (200, 200), net)


# img = np.array(img)
# net = np.array(net)

# img[200 : 200 + net.shape[0], 200 : 200 + net.shape[1]] = net

# img = Image.fromarray(img, mode="RGBA")

fnt = ImageFont.truetype("/home/marc/.local/share/fonts/HelveticaNeueLTStd-Blk.otf", 50)
d = ImageDraw.Draw(img)
d.text((200, 200), "Hello world", font=fnt, fill=(255, 255, 255, 255))

img.show()

img.save("test_img.png", quality=50)
