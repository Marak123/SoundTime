from PIL import Image
from io import BytesIO

class Tools:

    def __init__(self) -> None:
        pass

    def cropPathImage(self, name_file: str):
        im = Image.open(name_file)
        im1 = im.crop((0, 60, im.width, im.height - 60))
        im1.save(name_file)

    def cropByteImage(self, byte_image, name_file: str):
        im = Image.open(byte_image)
        im1 = im.crop((0, 60, im.width, im.height - 60))
        im1.save(name_file)