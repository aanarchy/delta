#!/usr/bin/env python3

import socket
import selectors
import types
import config
from imutils.video import VideoStream
import imutils
from pyzbar.pyzbar import decode
import time

sel = selectors.DefaultSelector()
print('[INFO] Camera starting up...')
vs = VideoStream(src=0).start()
time.sleep(2.0)


def start_connections(host, port, num_conns, raw_data):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
#       print('[INFO] Starting connection', connid, 'to', server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connid=connid,
                                     msg_total=len(raw_data),
                                     recv_total=0,
                                     data=raw_data,
                                     outb=b'')
        sel.register(sock, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print('[INFO]', str(recv_data),
                  'from connection', data.connid)
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print('[INFO] Closing connection', data.connid)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.data:
            data.outb = data.data.pop(0)
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


host = config.host
port = config.port

"""while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    barcodes = decode(frame)

    for barcode in barcodes:
        barcode_data = barcode.data
        print(barcode_data)
        if barcode_data is not None:
            data = [barcode_data]
            start_connections(host, port, len(data), data)"""
try:
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        barcodes = decode(frame)
        events = sel.select(timeout=1)
        for barcode in barcodes:
            barcode_data = barcode.data
#           print(barcode_data)
            if barcode_data is not None:
                data = [barcode_data]
                start_connections(host, port, len(data), data)
                if events:
                    for key, mask in events:
                        service_connection(key, mask)
                if not sel.get_map():
                    break

except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
