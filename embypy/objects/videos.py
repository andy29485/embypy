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
  def series_id(self):
    return self.object_dict.get('SeriesId')

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

