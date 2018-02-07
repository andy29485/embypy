#!/usr/bin/env python3

from embypy.utils import Connector
from embypy import objects
from simplejson.scanner import JSONDecodeError

class Emby(objects.EmbyObject):
  '''Emby connection class, an object of this type should be created
  to communicate with emby

  Parameters
  ----------
  url : str
    url to the server (e.g. http://127.0.0.1:8096/)
  api_key : str, optional
    key obtained from server dashboard
  device_id : str, optional
    device id to pass to emby

  Attributes
  ----------
  connector : embypy.utils.connector.Connector
    Object used to make api requests, do not use
  '''
  def __init__(self, url, **kargs):
    connector = Connector(url, **kargs)
    super().__init__({'ItemId':'', 'Name':''}, connector)

  def info(self, obj_id=None):
    '''Get info about object id

    Parameters
    ----------
    obj_id : str, list
      if not provided, server info is retured(as a dict).
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

    Parameters
    ----------
    query : str
      the search string to send to emby
    sort_map : dict
      is a dict of strings to ints. Strings should be item types, and
      the ints are the priority of those types(for sorting).
      lower valued(0) will appear first.
    strict_sort : bool
      if True, then only item types in the keys of sortmap will be
      included in the results

    Returns
    -------
    list
      list of emby objects
    '''
    search_params = {
      'remote'     : False,
      'searchTerm' : query
    }
    if strict_sort:
      search_params['IncludeItemTypes'] = ','.join(sort_map.keys())

    json = self.connector.getJson('/Search/Hints/', **search_params)
    items  = []
    for item in json["SearchHints"]:
      item = self.process(item)
      items.append(item)

    m_size = len(sort_map)
    items  = sorted(items, key = lambda x : sort_map.get(x.type, m_size))

    return items

  def latest(self, userId=None, itemTypes='', groupItems=False):
    '''returns list of latest items

    Parameters
    ----------
    userId : str
      if provided, then the list returned is
      the one that that use will see.
    itemTypes: str
      if provided, then the list will only include items
      if that type - gets passed to the emby api
      see https://github.com/MediaBrowser/Emby/wiki/Item-Types

    Returns
    -------
    list
      the itmes that will appear as latest (for user if id was given)
    '''
    json = self.connector.getJson('/Users/{UserId}/Items/Latest',
                                  remote=False,
                                  userId=userId,
                                  IncludeItemTypes=itemTypes,
                                  GroupItems=groupItems
    )
    return self.process(json)

  def nextUp(self, userId=None):
    '''returns list of items marked as `next up`

    Parameters
    ----------
    userId : str
      if provided, then the list returned is
      the one that that use will see.

    Returns
    -------
    list
      the itmes that will appear as next up (for user if id was given)
    '''
    json = self.connector.getJson('/Shows/NextUp', pass_uid=True,
                                   remote=False,   userId=userId
    )
    return self.process(json)

  def update(self):
    '''
    reload all cached information

    Notes
    -----
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

    Parameters
    ----------
    name : str
      name of new playlist
    song_ids : array_like
      list of song ids to add to playlist
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

    |force|

    Returns
    -------
    list
      of type :class:`embypy.objects.Album`
    '''
    return self.extras.get('albums', []) or self.albums_force

  @property
  def albums_force(self):
    items = self.connector.getJson('/Users/{UserId}/Items',
                                   remote            = False,
                                   format            = 'json',
                                   Recursive         = 'true',
                                   IncludeItemTypes  = 'MusicAlbum',
                                   Fields            = 'Path,ParentId,Overview',
                                   SortBy            = 'SortName',
                                   SortOrder         = 'Ascending'
    )
    items = self.process(items)
    self.extras['albums'] = items
    return items

  @property
  def songs(self):
    '''returns list of all songs.

    |force|

    Returns
    -------
    list
      of type :class:`embypy.objects.Audio`
    '''
    return self.extras.get('songs', []) or self.songs_force

  @property
  def songs_force(self):
    items = self.connector.getJson('/Users/{UserId}/Items',
                                   remote            = False,
                                   format            = 'json',
                                   SortOrder         = 'Ascending',
                                   Recursive         = 'true',
                                   IncludeItemTypes  = 'Audio',
                                   Fields            = 'Path,ParentId,Overview',
                                   SortBy            = 'SortName',
                                   SortOrder         = 'Ascending'
    )
    items = self.process(items)
    self.extras['songs'] = items
    return items

  @property
  def playlists(self):
    '''returns list of all playlists.

    |force|

    Returns
    -------
    list
      of type :class:`embypy.objects.Playlist`
    '''
    return self.extras.get('playlists', []) or self.playlists_force

  @property
  def playlists_force(self):
    items = self.connector.getJson('/Users/{UserId}/Items',
                                   remote            = False,
                                   format            = 'json',
                                   SortOrder         = 'Ascending',
                                   Recursive         = 'true',
                                   IncludeItemTypes  = 'Playlist',
                                   Fields            = 'Path,ParentId,Overview',
                                   SortBy            = 'SortName',
                                   SortOrder         = 'Ascending'
    )
    items = self.process(items)
    self.extras['playlists'] = items
    return items

  @property
  def artists(self):
    '''returns list of all song artists.

    |force|

    Returns
    -------
    list
      of type :class:`embypy.objects.Artist`
    '''
    return self.extras.get('artists', []) or self.artists_force

  @property
  def artists_force(self):
    items = self.connector.getJson('/Users/{UserId}/Items',
                                   remote            = False,
                                   format            = 'json',
                                   SortOrder         = 'Ascending',
                                   Recursive         = 'true',
                                   IncludeItemTypes  = 'MusicArtist',
                                   Fields            = 'Path,ParentId,Overview',
                                   SortBy            = 'SortName',
                                   SortOrder         = 'Ascending'
    )
    items = self.process(items)
    self.extras['artists'] = items
    return items

  @property
  def movies(self):
    '''returns list of all movies.

    |force|

    Returns
    -------
    list
      of type :class:`embypy.objects.Movie`
    '''
    return self.extras.get('movies', []) or self.movies_force

  @property
  def movies_force(self):
    items = self.connector.getJson('/Users/{UserId}/Items',
                                   remote            = False,
                                   format            = 'json',
                                   SortOrder         = 'Ascending',
                                   Recursive         = 'true',
                                   IncludeItemTypes  = 'Movie',
                                   Fields            = 'Path,ParentId,Overview',
                                   SortBy            = 'SortName',
                                   SortOrder         = 'Ascending'
    )
    items = self.process(items)
    self.extras['movies'] = items
    return items

  @property
  def episodes(self):
    '''returns a list of all episodes in emby.

    |force|

    Returns
    -------
    list
      of type :class:`embypy.objects.Episode`
    '''
    return self.extras.get('episodes', []) or self.episodes_force

  @property
  def episodes_force(self):
    items = self.connector.getJson('/Users/{UserId}/Items',
                                   remote            = False,
                                   format            = 'json',
                                   SortOrder         = 'Ascending',
                                   Recursive         = 'true',
                                   IncludeItemTypes  = 'Episode',
                                   Fields            = 'Path,ParentId,Overview',
                                   SortBy            = 'SortName',
                                   SortOrder         = 'Ascending'
    )
    items = self.process(items)
    self.extras['episodes'] = items
    return items
