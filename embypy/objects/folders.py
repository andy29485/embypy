#!/usr/bin/env python3

from embypy.objects.object import *

# Generic class
class Folder(EmbyObject):
  '''Class representing generic emby folder objects

  Parameters
  ----------
    object_dict : dict
      same as for `EmbyObject`
    connector : embypy.utils.connector.Connector
      same as for `EmbyObject`
  '''
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

  @property
  def child_count(self):
    '''number of items in this folder'''
    return self.object_dict.get('ChildCount', 0)

  @property
  def cumulative_run_time(self):
    '''total run time of items'''
    return self.object_dict.get('CumulativeRunTimeTicks', 0)

  @property
  def items(self):
    '''list of emby objects contained in the folder'''
    return self.extras.get('items', []) or self.items_force

  @property
  def items_force(self):
    items = self.connector.getJson(
          'Playlists/{Id}/Items'.format(Id=self.id), remote=False
    )
    items = self.process(items)
    self.extras['items'] = items
    return items

# Folders
class Playlist(Folder):
  '''Class representing emby playlist objects

  Parameters
  ----------
    object_dict : dict
      same as for `EmbyObject`
    connector : embypy.utils.connector.Connector
      same as for `EmbyObject`
  '''
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

  @property
  def songs(self):
    '''list of songs in the playlist'''
    items = []
    for i in self.items:
      if i.type == 'Audio':
        items.append(i)
      elif hasattr(i, 'songs'):
        items.extend(i.songs)
    return items

  @property
  def songs_force(self):
    items = []
    for i in self.items_force:
      if i.type == 'Audio':
        items.append(i)
      elif hasattr(i, 'songs'):
        items.extend(i.songs)
    return items

  def add_items(self, *items):
    '''append items to the playlist

    Parameters
    ----------
    items : array_like
      list of items to add(or their ids)

    See Also
    --------
      remove_items :
    '''
    items = [item.id for item in self.process(items)]
    if not items:
      return

    self.connector.post('Playlists/{Id}/Items'.format(Id=self.id),
      data={'Ids': ','.join(items)},
      remote=False
    )

  def remove_items(self, *items):
    '''remove items from the playlist

    Parameters
    ----------
    items : array_like
      list of items to remove(or their ids)

    See Also
    --------
      add_items :
    '''
    items = [item.id for item in self.process(items) if item in self.items]
    if not items:
      return

    self.connector.delete('Playlists/{Id}/Items'.format(Id=self.id),
      EntryIds=','.join(items),
      remote=False
    )

class BoxSet(Folder):
  '''Class representing emby boxsets/collection objects

  Parameters
  ----------
    object_dict : dict
      same as for `EmbyObject`
    connector : embypy.utils.connector.Connector
      same as for `EmbyObject`
  '''
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

class MusicAlbum(Folder):
  '''Class representing emby music album objects

  Parameters
  ----------
    object_dict : dict
      same as for `EmbyObject`
    connector : embypy.utils.connector.Connector
      same as for `EmbyObject`
  '''
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

  @property
  def album_artist_id(self):
    return self.object_dict.get('AlbumArtist')

  @property
  def album_artist(self):
    return self.process(self.album_artist_id)

  @property
  def artist_ids(self):
    return self.object_dict.get('Artists', [])

  @property
  def artists(self):
    return self.process(self.artist_ids)

  @property
  def album_id(self):
    return self.object_dict.get('AlbumId')

  @property
  def album(self):
    return self.object_dict.get('Album', '')

  @album.setter
  def album(self, value):
    self.object_dict['Album'] = value

  @property
  def songs(self):
    items = self.extras.get('songs', [])
    if not items:
      items = self.connector.getJson('/Users/{UserId}/Items',
                                     remote            = False,
                                     format            = 'json',
                                     SortOrder         = 'Ascending',
                                     SortBy            = 'SortName',
                                     AlbumIds          = self.id,
                                     Recursive         = 'true',
                                     IncludeItemTypes  = 'Audio',
                                     Fields            = 'Path,ParentId'
      )
      items = self.process(items)
      self.extras['songs'] = items
    return items

  @property
  def album_primary_image_tag(self):
    return self.object_dict.get('AlbumPrimaryImageTag')

  @property
  def premiere_date(self):
    return self.object_dict.get('PremiereDate')

class MusicArtist(Folder):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

  @property
  def premiere_date(self):
    return self.object_dict.get('PremiereDate')

  @property
  def albums(self):
    items = self.extras.get('albums', [])
    if not items:
      items = self.connector.getJson('/Users/{UserId}/Items',
                                     remote            = False,
                                     format            = 'json',
                                     SortOrder         = 'Ascending',
                                     SortBy            = 'SortName',
                                     ArtistIds         = self.id,
                                     Recursive         = 'true',
                                     IncludeItemTypes  = 'MusicAlbum',
                                     Fields            = 'Path,ParentId'
      )
      items = self.process(items)
      self.extras['albums'] = items
    return items

  @property
  def songs(self):
    items = self.extras.get('songs', [])
    if not items:
      item = self.connector.getJson('/Users/{UserId}/Items',
                                     remote            = False,
                                     format            = 'json',
                                     SortOrder         = 'Ascending',
                                     SortBy            = 'SortName',
                                     ArtistIds         = self.id,
                                     Recursive         = 'true',
                                     IncludeItemTypes  = 'Audio',
                                     Fields            = 'Path,ParentId'
      )
      items = self.process(items)
      self.extras['songs'] = items
    return items

class Season(Folder):
  '''Class representing emby season objects for TV shows

  Parameters
  ----------
    object_dict : dict
      same as for `EmbyObject`
    connector : embypy.utils.connector.Connector
      same as for `EmbyObject`
  '''
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

  @property
  def index_number(self):
    return self.object_dict.get('IndexNumber', 1)

  @index_number.setter
  def index_number(self, value):
    self.object_dict['IndexNumber'] = value

  @property
  def played_percentage(self):
    return self.object_dict.get('PlayedPercentage', 0)

  @property
  def series_id(self):
    return self.object_dict.get('SeriesId')

  @property
  def series(self):
    return self.process(self.series_id)

  @property
  def show(self):
    return self.series

  @property
  def series_name(self):
    return self.object_dict.get('SeriesName', '')

class Series(Folder):
  '''Class representing emby TV show/series objects

  Parameters
  ----------
    object_dict : dict
      same as for `EmbyObject`
    connector : embypy.utils.connector.Connector
      same as for `EmbyObject`
  '''
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

  @property
  def air_days(self):
    return self.object_dict.get('AirDays')

  @property
  def air_time(self):
    return self.object_dict.get('AirTime')

  @property
  def status(self):
    return self.object_dict.get('Status')

  @property
  def premiere_date(self):
    return self.object_dict.get('PremiereDate')

  @property
  def season_count(self):
    return self.object_dict.get('SeasonCount', 0)

# Game
class GameSystem(Folder):
  '''Class representing emby game systems objects

  Parameters
  ----------
    object_dict : dict
      same as for `EmbyObject`
    connector : embypy.utils.connector.Connector
      same as for `EmbyObject`
  '''
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
