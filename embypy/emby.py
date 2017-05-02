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
        obj = objects.EmbyObject({"Id":obj_id}, self.connector)
        return self.process(obj.update().object_dict)
      except JSONDecodeError:
        raise LookupError('Error object with that id does not exist', obj_id)
    else:
      return self.connector.getJson('/system/info/public')

  def search(self, query):
    json  = self.connector.getJson('/Search/Hints/', searchTerm=query)
    items = []
    for item in json["SearchHints"]:
      items.append(self.process(item))
    return items

  def latest(self):
    json  = self.connector.getJson('/Users/{UserId}/Items/Latest')
    items = []
    for item in json:
      items.append(self.process(item))
    return items
