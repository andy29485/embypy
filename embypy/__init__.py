#!/usr/bin/env python3

import embypy.utils
import embypy.objects

class Emby(objects.EmbyObject):
  def __init__(self, url, **kargs):
    """ create new emby connection object
    url       - url to the server (e.g. http://192.168.1.5:8096/)
    api_key   - key obtained from server dashboard
    device_id - device name to pass to emby
    """
    connector = utils.Connector(url, **kargs)
    super().__init__({'ItemId':'', 'Name':''}, connector)

  def info():
    return self.connector.getJson('/system/info/public')

  def search(self, query):
    json  = self.connector.getJson('/Search/Hints/', searchTerm=query)
    items = []
    for item in json["SearchHints"]:
      items.append(self.process(item))
    return items

