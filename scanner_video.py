from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time

print('[INFO] Camera starting up...')

vs = VideoStream(src=0).start()

time.sleep(2.0)

while True:

    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        data = barcode.data.decode('utf-8')
        text = '{} ({})'.format(data, barcode.type)
        print('[INFO] found {} {} '.format(barcode.type, data))
