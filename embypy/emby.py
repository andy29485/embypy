#!/usr/bin/env python3

from embypy import utils
from embypy import objects
from simplejson.scanner import JSONDecodeError

class Emby(objects.EmbyObject):
  def __init__(self, url, **kargs):
    """ create new emby connection object
    url       - url to the server (e.g. http://192.168.1.5:8096/)
    api_key   - key obtained from server dashboard
    device_id - device name to pass to emby
    """
    connector = utils.Connector(url, **kargs)
    super().__init__({'ItemId':'', 'Name':''}, connector)

  def info(self, obj_id=None):
    if obj_id:
      try:
        return self.process(obj_id)
      except JSONDecodeError:
        raise LookupError('Error object with that id does not exist', obj_id)
    else:
      return self.connector.getJson('/system/info/public')

  def search(self, query,
             sort_map = {'BoxSet':0,'Series':1,'Movie':2,'Audio':3,'Person':4},
             strict_sort = False):
    json  = self.connector.getJson('/Search/Hints/', searchTerm=query)
    items = []
    for item in json["SearchHints"]:
      item = self.process(item)
      if not strict_sort or item.type in sort_map:
        items.append(item)

    m_size   = len(sort_map)
    items    = sorted(items, key = lambda x : sort_map.get(x.type, m_size))

    return items

  def latest(self):
    json  = self.connector.getJson('/Users/{UserId}/Items/Latest')
    items = []
    for item in json:
      items.append(self.process(item))
    return items
