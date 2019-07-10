#!/usr/bin/env python3

import socket
import selectors
import types
import time
import config
from imutils.video import VideoStream
import imutils
import pyzbar

sel = selectors.DefaultSelector()
print('[INFO] Camera starting up...')
vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:

    vs = VideoStream(src=0).start()
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        raw_data = barcode.data.decode('utf-8')


def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print('[INFO] Starting connection', connid, 'to', server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connid=connid,
                                     msg_total=sum(len(d) for d in raw_data),
                                     recv_total=0,
                                     messages=list(raw_data),
                                     outb=b'')
        sel.register(sock, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print('[INFO]', repr(recv_data), 'from connection', data.connid)
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
start_connections(host, int(port), len(raw_data))


try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                service_connection(key, mask)
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
