#!/usr/bin/env python3

from embypy.objects.object import *
import asyncio

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
  def items_sync(self):
    return self.connector.sync_run(self.items)

  @property
  async def items(self):
    '''list of emby objects contained in the folder

    |force|

    |coro|

    Returns
    -------
    list
      with subclass of type :class:`embypy.objects.EmbyObject`
    '''
    return self.extras.get('items', []) or await self.items_force

  @property
  def items_force_sync(self):
    return self.connector.sync_run(self.items_force)

  @property
  async def items_force(self):
    items = await self.connector.getJson(
          '/Users/{UserId}/Items', parentId=self.id, remote=False,
          SortOrder='Ascending', SortBy='SortName',
    )
    items = await self.process(items)
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
  def songs_sync(self):
    return self.connector.sync_run(self.songs)

  @property
  async def songs(self):
    '''list of songs in the playlist

    |force|

    |coro|

    Returns
    -------
    list
      of type :class:`embypy.objects.Audio`
    '''
    items = []
    for i in await self.items:
      if i.type == 'Audio':
        items.append(i)
      elif hasattr(i, 'songs'):
        items.extend(await i.songs)
    return items

  @property
  def songs_force_sync(self):
    return self.connector.sync_run(self.songs_force)

  @property
  async def songs_force(self):
    items = []
    for i in await self.items_force:
      if i.type == 'Audio':
        items.append(i)
      elif hasattr(i, 'songs'):
        items.extend(await i.songs)
    return items

  @property
  async def items_force(self):
    items = await self.connector.getJson(
          'Playlists/{Id}/Items'.format(Id=self.id),
          remote=False, SortOrder='Ascending', SortBy='SortName',
    )
    items = await self.process(items)
    self.extras['items'] = items
    return items

  def add_items_sync(self, *items):
    return self.connector.sync_run(self.add_items_sync(*items))

  async def add_items(self, *items):
    '''append items to the playlist

    |coro|

    Parameters
    ----------
    items : array_like
      list of items to add(or their ids)

    See Also
    --------
      remove_items :
    '''
    items = [item.id for item in await self.process(items)]
    if not items:
      return

    await self.connector.post('Playlists/{Id}/Items'.format(Id=self.id),
      data={'Ids': ','.join(items)}, remote=False
    )

  def remove_items_sync(self, *items):
    return self.connector.sync_run(self.remove_items_sync(*items))

  async def remove_items(self, *items):
    '''remove items from the playlist

    |coro|

    Parameters
    ----------
    items : array_like
      list of items to remove(or their ids)

    See Also
    --------
      add_items :
    '''
    items = [i.id for i in (await self.process(items)) if i in self.items]
    if not items:
      return

    await self.connector.delete(
      'Playlists/{Id}/Items'.format(Id=self.id),
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

  @property
  def movies_sync(self):
    return self.connector.sync_run(self.movies)

  @property
  async def movies(self):
    '''list of movies in the collection

    |force|

    |coro|

    Returns
    -------
    list
      of type :class:`embypy.objects.Movie`
    '''
    items = []
    for i in await self.items:
      if i.type == 'Movie':
        items.append(i)
      elif hasattr(i, 'movies'):
        items.extend(await i.movies)
    return items

  @property
  def movies_force_sync(self):
    return self.connector.sync_run(self.movies_force)

  @property
  async def movies_force(self):
    items = []
    for i in await self.items_force:
      if i.type == 'Movie':
        items.append(i)
      elif hasattr(i, 'movies'):
        items.extend(await i.movies)
    return items

  @property
  def shows_sync(self):
    return self.series_sync

  @property
  def series_sync(self):
    return self.connector.sync_run(self.series)

  @property
  async def shows(self):
    return await self.series

  @property
  async def series(self):
    '''list of series in the collection

    |force|

    |coro|

    Returns
    -------
    list
      of type :class:`embypy.objects.Series`
    '''
    items = []
    for i in await self.items:
      if i.type == 'Series':
        items.append(i)
      elif hasattr(i, 'series'):
        items.extend(await i.series)
    return items

  @property
  def shows_force_sync(self):
    return self.series_force_sync

  @property
  def series_force_sync(self):
    return self.connector.sync_run(self.series_force)

  @property
  async def shows(self):
    return await self.series_force

  @property
  async def series_force(self):
    items = []
    for i in await self.items_force:
      if i.type == 'Series':
        items.append(i)
      elif hasattr(i, 'series'):
        items.extend(await i.series)
    return items

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
  def album_artist_ids(self):
    '''emby id of album artist'''
    return [a['Id'] for a in self.object_dict.get('AlbumArtists', [])]

  @property
  def album_artists_sync(self):
    return self.connector.sync_run(self.album_artists)

  @property
  async def album_artists(self):
    '''
    list of album artist objects

    |coro|

    Returns
    -------
    list
      of type :class:`embypy.objects.MusicArtist`
    '''
    return await self.process(self.album_artist_ids)

  @property
  def artist_ids(self):
    '''list of emby artist ids for the song'''
    return [a['Id'] for a in self.object_dict.get('ArtistItems', [])]

  @property
  def artists_sync(self):
    return self.connector.sync_run(self.artists)

  @property
  async def artists(self):
    '''list of song artist objects

    |coro|

    Returns
    -------
    list
      of type :class:`embypy.objects.MusicArtist`
    '''
    return await self.process(self.artist_ids)

  @property
  def songs_sync(self):
    return self.connector.sync_run(self.songs)

  @property
  async def songs(self):
    '''returns a list of songs in the album

    |force|

    |coro|

    Returns
    -------
    list
      of type :class:`embypy.objects.Audio`
    '''
    return self.extras.get('songs') or await self.songs_force

  @property
  def songs_force_sync(self):
    return self.connector.sync_run(self.songs_force)

  @property
  async def songs_force(self):
    items = await self.connector.getJson('/Users/{UserId}/Items',
                                   remote            = False,
                                   format            = 'json',
                                   SortOrder         = 'Ascending',
                                   SortBy            = 'SortName',
                                   AlbumIds          = self.id,
                                   Recursive         = 'true',
                                   IncludeItemTypes  = 'Audio',
                                   Fields            = 'Path,ParentId,Overview'
    )
    items = await self.process(items)
    self.extras['songs'] = items
    return items

class MusicArtist(Folder):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

  @property
  def premiere_date(self):
    return self.object_dict.get('PremiereDate')

  @property
  def albums_sync(self):
    return self.connector.sync_run(self.albums)

  @property
  async def albums(self):
    '''list of album objects that include the artist

    |force|

    |coro|

    Returns
    -------
    list
      of type :class:`embypy.objects.Album`
    '''
    return self.extras.get('albums') or await self.albums_force

  @property
  def albums_force_sync(self):
    return self.connector.sync_run(self.albums_force)

  @property
  async def albums_force(self):
    items = await self.connector.getJson('/Users/{UserId}/Items',
                                   remote            = False,
                                   format            = 'json',
                                   SortOrder         = 'Ascending',
                                   SortBy            = 'SortName',
                                   ArtistIds         = self.id,
                                   Recursive         = 'true',
                                   IncludeItemTypes  = 'MusicAlbum',
                                   Fields            = 'Path,ParentId,Overview'
    )
    items = await self.process(items)
    self.extras['albums'] = items
    return items

  @property
  def songs_sync(self):
    return self.connector.sync_run(self.songs)

  @property
  async def songs(self):
    '''list of song objects that include the artist

    |force|

    |coro|

    Returns
    -------
    list
      of type :class:`embypy.objects.Audio`
    '''
    return self.extras.get('songs') or await self.songs_force

  @property
  def songs_force_sync(self):
    return self.connector.sync_run(self.songs_force)

  @property
  async def songs_force(self):
    items = await self.connector.getJson('/Users/{UserId}/Items',
                                   remote            = False,
                                   format            = 'json',
                                   SortOrder         = 'Ascending',
                                   SortBy            = 'SortName',
                                   AlbumIds          = self.id,
                                   Recursive         = 'true',
                                   IncludeItemTypes  = 'Audio',
                                   Fields            = 'Path,ParentId,Overview'
    )
    items = await self.process(items)
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
    '''season number'''
    return self.object_dict.get('IndexNumber', 1)

  @index_number.setter
  def index_number(self, value):
    self.object_dict['IndexNumber'] = value

  @property
  def played_percentage(self):
    '''percentage of episodes watched'''
    return self.object_dict.get('PlayedPercentage', 0)

  @property
  def series_id(self):
    '''emby id of the show'''
    return self.object_dict.get('SeriesId')

  @property
  def series_sync(self):
    return self.connector.sync_run(self.series)

  @property
  async def series(self):
    '''
    emby object representing the show

    |coro|

    Returns
    -------
    :class:`embypy.objects.Series`
    '''
    return await self.process(self.series_id)

  @property
  def show_sync(self):
    return self.connector.sync_run(self.series)

  @property
  async def show(self):
    '''same as `series`'''
    return await self.series

  @property
  def series_name(self):
    '''Name of the show'''
    return self.object_dict.get('SeriesName', '')

  @property
  def episodes_sync(self):
    return self.connector.sync_run(self.episodes)

  @property
  async def episodes(self):
    '''returns a list of all episodes in this season.

    |force|

    |coro|

    Returns
    -------
    list
      of type :class:`embypy.objects.Episode`
    '''
    return self.extras.get('episodes', []) or await self.episodes_force

  @property
  def episodes_force_sync(self):
    return self.connector.sync_run(self.episodes_force)

  @property
  async def episodes_force(self):
    items = await self.connector.getJson(
                            '/Shows/{}/Episodes'.format(self.series_id),
                            remote            = False,
                            format            = 'json',
                            Season            = self.index_number,
                            pass_uid          = True,
                            SortOrder         = 'Ascending',
                            Recursive         = 'true',
                            IncludeItemTypes  = 'Episode',
                            Fields            = 'Path,ParentId,Overview'
    )
    items = await self.process(items)
    #sortkey = lambda x: (x.season_number, x.index_number)
    #items   = sorted(items, key=sortkey)
    self.extras['episodes'] = items
    return items

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
    '''Days of the week the show airs'''
    return self.object_dict.get('AirDays')

  @property
  def air_time(self):
    '''Time of day at which show airs'''
    return self.object_dict.get('AirTime')

  @property
  def status(self):
    '''whether show is Airing or Complete'''
    return self.object_dict.get('Status')

  @property
  def premiere_date(self):
    '''date the show started airing'''
    return self.object_dict.get('PremiereDate')

  @property
  def seasons_sync(self):
    return self.connector.sync_run(self.seasons)

  @property
  async def seasons(self):
    '''list of seasons that are part of the show

    |force|

    |coro|

    Returns
    -------
    list
      of type :class:`embypy.objects.Season`
    '''
    return self.extras.get('seasons') or await self.seasons_force

  @property
  def seasons_force_sync(self):
    return self.connector.sync_run(self.seasons_force)

  @property
  async def seasons_force(self):
    items = await self.connector.getJson(
                                  '/Shows/{}/Seasons'.format(self.id),
                                  remote            = False,
                                  format            = 'json',
                                  SortOrder         = 'Ascending',
                                  SortBy            = 'SortName',
                                  Recursive         = 'true',
                                  pass_uid          = True,
                                  Fields            = 'Path,ParentId,Overview'
    )
    items = await self.process(items)
    self.extras['seasons'] = items
    return items

  @property
  def episodes_sync(self):
    return self.connector.sync_run(self.episodes)

  @property
  async def episodes(self):
    '''list of episodes that are part of the show

    |force|

    |coro|

    Returns
    -------
    list
      of type :class:`embypy.objects.Episode`
    '''
    return self.extras.get('episodes') or await self.episodes_force

  @property
  def episodes_force_sync(self):
    return self.connector.sync_run(self.episodes_force)

  @property
  async def episodes_force(self):
    items = await self.connector.getJson(
                            '/Shows/{}/Episodes'.format(self.id),
                            remote            = False,
                            format            = 'json',
                            SortOrder         = 'Ascending',
                            SortBy            = 'SortName',
                            Recursive         = 'true',
                            pass_uid          = True,
                            Fields            = 'Path,ParentId,Overview'
    )
    items = await self.process(items)
    self.extras['episodes'] = items
    return items

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
