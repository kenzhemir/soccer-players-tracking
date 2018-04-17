#!/usr/bin/python

import os, sys

cd = os.path.dirname(os.path.abspath(__file__))
os.chdir(cd)

sys.path.insert(0, os.path.join(cd, 'libs'))

import random
from socketIO_client import SocketIO


socketio = None

names = ['Ronaldo', 'Messi', 'ball', 'referee']
width, height = 1000, 1000
objects = []
for name in names:
  lx = random.randint(0, width - 100)
  ly = random.randint(0, height - 100)
  rx = random.randint(lx + 100, width)
  ry = random.randint(ly + 100, height)
  objects.append({
      'name': name,
      'lx': lx,
      'ly': ly,
      'rx': rx,
      'ry': ry
  })

def listener(data):
  print('received => ', len(data))
  socketio.emit('OR', objects)
  print('sent => ', objects)


def connected():
  print('connected')


def reconnected():
  print('reconnected')


def disconnected():
  print('disconnected')


if __name__ == '__main__':
  socketio = SocketIO('localhost', 5000)
  socketio.on('connect', connected)
  socketio.on('reconnect', reconnected)
  socketio.on('disconnect', disconnected)
  socketio.on('video_stream', listener)
  socketio.emit('join', 'OR')
  socketio.wait()
  socketio.emit('leave', 'OR')