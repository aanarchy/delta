#!/usr/bin/env python3

import socket
import selectors
import types
from datetime import datetime, timedelta
import config
from app.models import User
from app import db


host = config.host
port = config.port
sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()
#   print('[INFO] Accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            id = int(recv_data)
            user = User.query.filter_by(id=id).first()
            if user is not None:
                if (datetime.now() - user.last_seen) >= config.cooldown:
                    if user.status == 'Logged in':
                        user.status = 'Logged out'
                        data.outb += '{} has logged out.'.format(
                                     user.username).encode('utf-8')
                    elif user.status == (user.status == 'Logged out'
                                         and (datetime.now()
                                              - config.late_time)
                                         >= timedelta(seconds=0)
                                         and config.late):
                        user.status = 'Late'
                        data.outb += '{} is late.'.format(
                                     user.username).encode('utf-8')
                    else:
                        user.status = 'Logged in'
                        data.outb += '{} has logged in.'.format(
                                     user.username).encode('utf-8')
                    user.last_seen = datetime.now()
                    db.session.commit()
        else:
            print('[INFO] Closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('[INFO] Sending', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print('[INFO] Listening on', (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("[EXIT] Caught keyboard interrupt, exiting")
finally:
    sel.close()
