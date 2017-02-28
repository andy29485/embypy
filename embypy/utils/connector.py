#!/usr/bin/env python3

import json
from requests import Session
from requests.utils import urlparse, urlunparse
from ws4py.client.threadedclient import WebSocketClient

class WebSocket(WebSocketClient):
  def opened(self):
    pass #on_open

  def closed(self, code, reason=None):
     pass #on_close

  def received_message(self, m):
    pass #on_message

class Connector:
  def __init__(self, url, **kargs):
    if 'api_key' in kargs and 'device_id' in kargs:
      self.api_key   = kargs['api_key']
      self.device_id = kargs['device_id']
      self.username  = None
      self.password  = None
    elif 'username' in kargs and 'password' in kargs:
      self.api_key   = None
      self.device_id = None
      self.username  = kargs['username']
      self.password  = kargs['password']
    else:
      raise ValueError('provide api key and device id or username/password')

    p = urlparse(url)
    self.scheme    = p.scheme
    self.netloc    = p.netloc
    self.session   = Session()

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
    return self.session.get(url, params=query).json()
