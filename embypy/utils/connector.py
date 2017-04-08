#!/usr/bin/env python3

import json
from requests import Session, adapters, exceptions
from requests.utils import urlparse, urlunparse
import asyncio
import websockets

adapters.DEFAULT_RETRIES = 5

class WebSocket:
  def __init__(self, url):
    self.on_message = None
    self.url        = url

  def connect(self):
    self.ws = await websockets.connect(url)
    asyncio.get_event_loop().run_until_complete(self.handler())

  async def handler(self, websocket, path):
    while True:
      message = await self.ws.recv()
      if self.on_message:
        await self.on_message(message)

  def close(self):
    self.ws.close()
    self.ws = None

class Connector:
  def __init__(self, url, **kargs):
    if ('api_key'  not in kargs or 'device_id' not in kargs) and \
       ('username' not in kargs or 'password'  not in kargs):
      raise ValueError('provide api key and device id or username/password')
    self.userid    = kargs.get('userid')
    self.api_key   = kargs.get('api_key')
    self.username  = kargs.get('username')
    self.password  = kargs.get('password')
    self.device_id = kargs.get('device_id')

    p            = urlparse(url)
    self.scheme  = p.scheme
    self.netloc  = p.netloc
    self.session = Session()

    #connect to websocket is user wants to
    if 'ws' in kargs:
      self.ws = WebSocket(self.get_url(True))
    else:
      self.ws = None

  def get_url(self, path='/', websocket=False):
    if websocket:
      scheme = {'http':'ws', 'https':'wss'}[self.scheme]
      return urlunparse((scheme, self.netloc, path, '', '', ''))
    else:
      return urlunparse((self.scheme, self.netloc, path, '', '', ''))

  def set_on_message(self, func):
    self.ws.on_message = func

  def getJson(self, path, **query):
    url = self.get_url(path)

    query.update({'api_key':self.api_key, 'deviceId': self.device_id})
    try:
      return self.session.get(url,params=query,timeout=27,verify=False).json()
    except exceptions.Timeout:
      raise exceptions.Timeout('Timeout '+url)
    except exceptions.ConnectionError:
      raise exceptions.ConnectionError('emby server is probably down')
