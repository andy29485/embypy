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
  def album(self):
    return self.object_dict.get('Album')

  @property
  def album_artist(self):
    return self.object_dict.get('AlbumArtist')

  @property
  def artists(self):
    return self.object_dict.get('Artists')

  @property
  def album_id(self):
    return self.object_dict.get('AlbumId')

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

