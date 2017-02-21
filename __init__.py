#!/usr/bin/env python3

import asyncio
#import websocket
import inspect
import json
from requests.utils import urlparse, urlunparse
from requests import Session

class Connector:
  def __init__(self, api_key, device_id, url):
    p = urlparse(url)
    self.api_key   = api_key
    self.device_id = device_id
    self.scheme    = p.scheme
    self.netloc    = p.netloc
    self.session   = Session()

  def getJson(self, path, **query):
    query.update({'api_key':self.api_key, 'deviceId': self.device_id})
    url = urlunparse((self.scheme, self.netloc, path, '', '', ''))
    return self.session.get(url, params=query).json()

class EmbyObject:
  def __init__(self, object_dict, connector):
    self.id        = object_dict["ItemId"]
    self.name      = object_dict["Name"]
    self.connector = connector

  def process(self, object_dict):
    if object_dict['Type'] == 'Series':
      return Series(object_dict, self.connector)
    if object_dict['Type'] == 'Movie':
      return Movie(object_dict, self.connector)
    if object_dict['Type'] == 'Episode':
      return Episode(object_dict, self.connector)

  def getPrimaryImageUrl(self):
    path = '/Items/' + self.id + '/Images/Primary'
    return urlunparse((self.connector.scheme,
                       self.connector.netloc, path,
                       '', '', ''
    ))


class Series(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
    self.year = object_dict["ProductionYear"]

class Movie(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

class Episode(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)


class Emby(EmbyObject):
  WS_URL = 'ws://{netloc}?api_key={api_key}&deviceId={device_id}'

  def __init__(self, url, api_key, device_id):
    """ create new emby connection object
    url       - url to the server (e.g. http://192.168.1.5:8096/)
    api_key   - key obtained from server dashboard
    device_id - device name to pass to emby
    """
    parsed_url  = urlparse(url)
    self.loop   = asyncio.get_event_loop()
    connector   = Connector(api_key, device_id, url)
    super().__init__({'ItemId':'', 'Name':''}, connector)
    self.url    = self.WS_URL.format(netloc    = parsed_url.netloc,
                                          api_key   = api_key,
                                          device_id = device_id
    )
    #self.ws = websocket.WebSocketApp(self.url,
    #                                 on_message = self.on_message,
    #                                 on_error   = self.on_error,
    #                                 on_close   = self.on_close
    #)

  def on_message(self, ws, message): #TODO
    print(message)

  def on_error(self, ws, error):     #TODO
    print(error)

  def on_close(self, ws):            #TODO
    print("### closed ###")

  def on_open(self, ws):             #TODO
    print("### opened ###")

  def info():
    return self.connector.getJson('/system/info/public')

  def search(self, query):
    json  = self.connector.getJson('/Search/Hints/', searchTerm=query)
    items = []
    for item in json["SearchHints"]:
      items.append(self.process(item))
    return items


