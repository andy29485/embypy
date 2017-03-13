#!/usr/bin/env python3

import json
from requests import Session, adapters, exceptions
from requests.utils import urlparse, urlunparse
from ws4py.client.threadedclient import WebSocketClient

adapters.DEFAULT_RETRIES = 5

class WebSocket(WebSocketClient):
  def opened(self):
    pass #on_open

  def closed(self, code, reason=None):
     pass #on_close

  def received_message(self, m):
    pass #on_message

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
    if 'ws' in kargs and callable(kargs['ws']):
      self.ws = WebSocket(self.get_url(True), protocols=['http-only', 'chat'])
    else:
      self.ws = None

  def get_url(self, path='/', websocket=False):
    if websocket:
      scheme = {'http':'ws', 'https':'wss'}[self.scheme]
      return urlunparse((scheme, self.netloc, path, '', '', ''))
    else:
      return urlunparse((self.scheme, self.netloc, path, '', '', ''))

  def getJson(self, path, **query):
    url = self.get_url(path)

    query.update({'api_key':self.api_key, 'deviceId': self.device_id})
    try:
      return self.session.get(url, params=query, timeout=(4, 7)).json()
    except exceptions.Timeout:
      raise exceptions.Timeout('Timeout '+url)
    except ConnectionError:
      raise ConnectionError('emby server is probably down')
