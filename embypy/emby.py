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
      return self.connector.getJson('/system/info/public', remote=False)

  def search(self, query,
             sort_map = {'BoxSet':0,'Series':1,'Movie':2,'Audio':3,'Person':4},
             strict_sort = False):
    if strict_sort:
      json = self.connector.getJson('/Search/Hints/',
                                    remote=False,
                                    searchTerm=query,
                                    IncludeItemTypes=','.join(sort_map.keys())
      )
    else:
      json = self.connector.getJson('/Search/Hints/',
                                    remote=False,
                                    searchTerm=query
      )
    items  = []
    for item in json["SearchHints"]:
      item = self.process(item)
      items.append(item)

    m_size = len(sort_map)
    items  = sorted(items, key = lambda x : sort_map.get(x.type, m_size))

    return items

  def latest(self, userId=None):
    json = self.connector.getJson('/Users/{UserId}/Items/Latest',
                                   remote=False, userId=userId
    )
    return self.process(json)

  def nextUp(self, userId=None):
    json = self.connector.getJson('/Shows/NextUp', pass_uid=True,
                                   remote=False,   userId=userId
    )
    return self.process(json)

  def update(self):
    keys = self.extras.keys()
    self.extras = {}
    for key in keys:
      try:
        func = getattr(self, key, None)
        if callable(func):
          func()
      except:
        pass

  def create_playlist(self, name, *song_ids):
    data = {'Name': name}

    ids = ','.join([item.id for item in self.process(song_ids)])
    if ids:
      data['Ids'] = ids

    return self.connector.post('/Playlists',
      data=data,
      pass_uid=True,
      remote=False
    )

  @property
  def albums(self):
    return self.extras.get('albums', []) or self.albums_force

  @property
  def albums_force(self):
    items = self.connector.getJson('/Users/{UserId}/Items',
                                   remote            = False,
                                   format            = 'json',
                                   SortOrder         = 'Ascending',
                                   Recursive         = 'true',
                                   IncludeItemTypes  = 'MusicAlbum',
                                   Fields            = 'Path,ParentId'
    )
    items = self.process(items)
    self.extras['albums'] = items
    return items

  @property
  def songs(self):
    return self.extras.get('songs', []) or self.songs_force

  @property
  def songs_force(self):
    items = self.connector.getJson('/Users/{UserId}/Items',
                                   remote            = False,
                                   format            = 'json',
                                   SortOrder         = 'Ascending',
                                   Recursive         = 'true',
                                   IncludeItemTypes  = 'Audio',
                                   Fields            = 'Path,ParentId'
    )
    items = self.process(items)
    self.extras['songs'] = items
    return items

  @property
  def playlists(self):
    return self.extras.get('playlists', []) or self.playlists_force

  @property
  def playlists_force(self):
    items = self.connector.getJson('/Users/{UserId}/Items',
                                   remote            = False,
                                   format            = 'json',
                                   SortOrder         = 'Ascending',
                                   Recursive         = 'true',
                                   IncludeItemTypes  = 'Playlist',
                                   Fields            = 'Path,ParentId'
    )
    items = self.process(items)
    self.extras['playlists'] = items
    return items

  @property
  def artists(self):
    return self.extras.get('artists', []) or self.artists_force

  @property
  def artists_force(self):
    items = self.connector.getJson('/Users/{UserId}/Items',
                                   remote            = False,
                                   format            = 'json',
                                   SortOrder         = 'Ascending',
                                   Recursive         = 'true',
                                   IncludeItemTypes  = 'MusicArtist',
                                   Fields            = 'Path,ParentId'
    )
    items = self.process(items)
    self.extras['artists'] = items
    return items

  @property
  def movies(self):
    return self.extras.get('movies', []) or self.movies_force

  @property
  def movies_force(self):
    items = self.connector.getJson('/Users/{UserId}/Items',
                                   remote            = False,
                                   format            = 'json',
                                   SortOrder         = 'Ascending',
                                   Recursive         = 'true',
                                   IncludeItemTypes  = 'Movie',
                                   Fields            = 'Path,ParentId'
    )
    items = self.process(items)
    self.extras['movies'] = items
    return items

  @property
  def episodes(self):
    return self.extras.get('episodes', []) or self.episodes_force

  @property
  def episodes_force(self):
    items = self.connector.getJson('/Users/{UserId}/Items',
                                   remote            = False,
                                   format            = 'json',
                                   SortOrder         = 'Ascending',
                                   Recursive         = 'true',
                                   IncludeItemTypes  = 'Episode',
                                   Fields            = 'Path,ParentId'
    )
    items = self.process(items)
    self.extras['episodes'] = items
    return items
