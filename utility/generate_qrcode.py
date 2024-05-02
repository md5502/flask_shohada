import qrcode
img = qrcode.make('https://pypi.org/project/qrcode/')
type(img)  # qrcode.image.pil.PilImage
img.save("some_file.png")