#!/usr/bin/env python3

from embypy.objects.object import *

# Generic class
class Video(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
  @property
  def aspect_ratio(self):
    return self.object_dict.get('AspectRatio')

  @property
  def chapters(self):
    return self.object_dict.get('Chapters')

  @property
  def overview(self):
    return self.object_dict.get('Overview')

  @property
  def genres(self):
    return self.object_dict.get('Genres')

  @property
  def stream_url(self):
    path = '/Videos/{}/stream.mp4'.format(self.id)
    return self.connector.get_url(path)

# Videos
class Movie(Video):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
  @property
  def premiere_date(self):
    return self.object_dict.get('PremiereDate')


class Episode(Video):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
  @property
  def index_number(self):
    return self.object_dict.get('IndexNumber')

  @property
  def premiere_date(self):
    return self.object_dict.get('PremiereDate')

  @property
  def index_number(self):
    return self.object_dict.get('IndexNumber')

  @property
  def episode_number(self):
    return self.index_number

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
  def season_id(self):
    return self.object_dict.get('SeasonId')

  @property
  def season(self):
    return self.process(self.season_id)

  @property
  def series_name(self):
    return self.object_dict.get('SeriesName')

  @property
  def genres(self):
    return self.object_dict.get('SeriesGenres')

class Trailer(Video):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

class AdultVideo(Video):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

class MusicVideo(Video):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
