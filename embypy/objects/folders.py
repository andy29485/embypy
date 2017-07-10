#!/usr/bin/env python3

from embypy.objects.object import *

# Generic class
class Folder(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
  @property
  def child_count(self):
    return self.object_dict.get('ChildCount')

  @property
  def cumulative_run_time(self):
    return self.object_dict.get('CumulativeRunTimeTicks')

  @property
  def genres(self):
    return self.object_dict.get('Genres')

# Folders
class Playlist(Folder):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

  @property
  def items(self):
    items = self.extras.get('items', [])
    if not items:
      items = self.connector.getJson('/Playlists/{Id}/Items'.format(Id=self.id))
      items = self.process(items)
      self.extras['items'] = items
    return items

  @property
  def songs(self):
    items = []
    for i in self.items:
      if i.type == 'Audio':
        items.append(i)
      elif hasattr(i, 'songs'):
        items.extend(i.songs)
    return items

class BoxSet(Folder):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

  @property
  def overview(self):
    return self.object_dict.get('Overview')

class MusicAlbum(Folder):
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
    return self.object_dict.get('Artists')

  @property
  def artists(self):
    artists = []
    for aid in self.artists_ids:
      artists.append(self.process(aid))
    return artists

  @property
  def album_id(self):
    return self.object_dict.get('AlbumId')

  @property
  def album(self):
    return self.object_dict.get('Album')

  @property
  def songs(self):
    items = self.extras.get('songs', [])
    if not items:
      items = self.connector.getJson('/Users/{UserId}/Items',
                                     format            = 'json',
                                     SortOrder         = 'Ascending',
                                     AlbumIds          = self.id,
                                     Recursive         = 'true',
                                     IncludeItemTypes  = 'Audio'
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
                                     format            = 'json',
                                     SortOrder         = 'Ascending',
                                     ArtistIds         = self.id,
                                     Recursive         = 'true',
                                     IncludeItemTypes  = 'MusicAlbum'
      )
      items = self.process(items)
      self.extras['albums'] = items
    return items

  @property
  def songs(self):
    items = self.extras.get('songs', [])
    if not items:
      item = self.connector.getJson('/Users/{UserId}/Items',
                                     format            = 'json',
                                     SortOrder         = 'Ascending',
                                     ArtistIds         = self.id,
                                     Recursive         = 'true',
                                     IncludeItemTypes  = 'Audio'
      )
      items = self.process(items)
      self.extras['songs'] = items
    return items

class Season(Folder):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
  @property
  def index_number(self):
    return self.object_dict.get('IndexNumber')

  @property
  def played_percentage(self):
    return self.object_dict.get('PlayedPercentage')

  @property
  def overview(self):
    return self.object_dict.get('Overview')

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
    return self.object_dict.get('SeriesName')

class Series(Folder):
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
  def overview(self):
    return self.object_dict.get('Overview')

  @property
  def season_count(self):
    return self.object_dict.get('SeasonCount')

# Game
class GameSystem(Folder):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
