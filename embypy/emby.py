#!/usr/bin/env python3

from embypy import utils
from embypy import objects
from simplejson.scanner import JSONDecodeError

class Emby(objects.EmbyObject):
  '''Emby connection class, an object of this type should be created
  to communicate with emby
  '''
  def __init__(self, url, **kargs):
    '''create new emby connection object

    :param url: url to the server (e.g. http://127.0.0.1:8096/)
    :type url:  str
    :param api_key: key obtained from server dashboard
    :type api_key: str
    :param device_id: device id to pass to emby
    :type decice_id:  str

    TODO - other params from connector
    '''
    connector = utils.Connector(url, **kargs)
    super().__init__({'ItemId':'', 'Name':''}, connector)

  def info(self, obj_id=None):
    '''Get info about object id

    `obj_id` if not provided, server info is retured(as a dict).
    Otherwise, an object with that id is returned
    (or objects if `obj_id` is a list).
    '''
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
    '''Sends a search request to emby, returns results

    `query` is the search string to send to emby

    `sort_map` is a dict of strings to ints. Strings should be item types, and
    the ints are the priority of those types(for sorting).
    lower valued(0) will appear first.

    `strict_sort` if True, then only item types in the keys of sortmap will be
    included in the results

    `returns` a list of emby objects
    '''
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
    '''returns list of latest items

    if `userId` is provided, then the list returned is
    the one that that use will see.
    '''
    json = self.connector.getJson('/Users/{UserId}/Items/Latest',
                                   remote=False, userId=userId
    )
    return self.process(json)

  def nextUp(self, userId=None):
    '''returns list of items marked as `next up`

    if `userId` is provided, then the list returned is
    the one that that use will see.
    '''
    json = self.connector.getJson('/Shows/NextUp', pass_uid=True,
                                   remote=False,   userId=userId
    )
    return self.process(json)

  def update(self):
    '''
    reload all cached information

    This is a slow process, and will remove the cache before updating.
    Thus it is recomended to use the `*_force` properties, which will
    only update the cache after data is retrived.
    '''
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
    '''create a new playlist
    `name`     - name of new playlist
    `song_ids` - [optional] list of song ids to add to playlist
    '''
    data = {'Name': name}
    ids = ','.join([item.id for item in self.process(song_ids)])
    if ids:
      data['Ids'] = ids

    # TODO - return playlist not status
    return self.connector.post('/Playlists',
      data=data,
      pass_uid=True,
      remote=False
    )

  @property
  def albums(self):
    '''returns list of all albums.

    If a cached list is avalible, that is returned

    see: albums_force
    '''
    return self.extras.get('albums', []) or self.albums_force

  @property
  def albums_force(self):
    '''returns list of albums, focing a refresh

    Upon completion of a retrival, the cache is updated.
    '''
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
    '''returns list of all songs.

    If a cached list is avalible, that is returned

    see: songs_force
    '''
    return self.extras.get('songs', []) or self.songs_force

  @property
  def songs_force(self):
    '''returns list of songs, focing a refresh

    Upon completion of a retrival, the cache is updated.
    '''
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
    '''returns list of all playlists.

    If a cached list is avalible, that is returned

    see: playlists_force
    '''
    return self.extras.get('playlists', []) or self.playlists_force

  @property
  def playlists_force(self):
    '''returns list of playlists, focing a refresh

    Upon completion of a retrival, the cache is updated.
    '''
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
    '''returns list of all song artists.

    If a cached list is avalible, that is returned

    see: artists_force
    '''
    return self.extras.get('artists', []) or self.artists_force

  @property
  def artists_force(self):
    '''returns list of song artists, focing a refresh

    Upon completion of a retrival, the cache is updated.
    '''
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
    '''returns list of all movies.

    If a cached list is avalible, that is returned

    see: movies_force
    '''
    return self.extras.get('movies', []) or self.movies_force

  @property
  def movies_force(self):
    '''returns list of movies, focing a refresh

    Upon completion of a retrival, the cache is updated.
    '''
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
    '''returns list of all episodes.

    If a cached list is avalible, that is returned

    see: episodes_force
    '''
    return self.extras.get('episodes', []) or self.episodes_force

  @property
  def episodes_force(self):
    '''returns list of episodes, focing a refresh

    Upon completion of a retrival, the cache is updated.
    '''
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
