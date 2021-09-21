import pyqrcode
import png
from pyqrcode import QRCode
from PIL import Image


def create_phys_ticket():
    s = "https://www.youtube.com/watch?v=xO2YQ4KFFxk&ab_channel=%D0%A3%D0%BC%D0%B0%D1%80%D0%A2%D0%B0%D1%82%D0%B0%D1%80"
    paths = "static/polls/images/"

    url = pyqrcode.create(s)
    url.png(paths + 'myqr.png', scale = 6)
    front_img = Image.open(paths + '1.png')
    back_img = Image.open(paths + '2.png')
    qr = Image.open(paths + 'myqr.png')
    front_img.paste(qr, (1575, 100), qr)
    front_img.save("new_img.png")
    back_img.paste(qr, (100, 100), qr)
    back_img.save("new_img2.png")

create_phys_ticket()