from pyzbar import pyzbar
import argparse
import cv2


ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='path to input image')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])

barcodes = pyzbar.decode(image)


for barcode in barcodes:
    data = barcode.data.decode('utf-8')
    text = '{} ({})'.format(data, barcode.type)
    print('[INFO] found {} {} '.format(barcode.type, data))
