#!/usr/bin/env python3

from embypy.objects.object import *

# Generic class
class Audio(EmbyObject):
  '''Class representing generic emby Audio objects

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
  def album_id(self):
    '''the id of the album this song is in'''
    return self.object_dict.get('AlbumId')

  @property
  def album(self):
    return self.process(self.album_id)

  @property
  def index_number(self):
    '''track number on disc'''
    return self.object_dict.get('IndexNumber', 1)

  @index_number.setter
  def index_number(self, value):
    self.object_dict['IndexNumber'] = value

  @property
  def track_number(self):
    return self.index_number

  @track_number.setter
  def track_number(self, value):
    self.index_number = value

  @property
  def album_artist_ids(self):
    '''list of album artist ids'''
    return [a['Id'] for a in self.object_dict.get('AlbumArtists', [])]

  @property
  def album_artist_names(self):
    '''names of album artists'''
    return self.object_dict.get('AlbumArtist', '').split(';')

  @property
  def album_artists(self):
    return self.process(self.album_artist_ids)

  @property
  def artist_ids(self):
    '''list of song artist ids'''
    return [a['Id'] for a in self.object_dict.get('ArtistItems', [])]

  @property
  def artist_names(self):
    '''names of song artists'''
    return self.object_dict.get('Artists', [])

  @property
  def artists(self):
    '''list of song artist objects'''
    return self.process(self.artist_ids)

  @property
  def album_primary_image_tag(self):
    return self.object_dict.get('AlbumPrimaryImageTag')

  @property
  def media_type(self):
    return self.object_dict.get('MediaType', 'Audio')

  @property
  def type(self):
    return self.object_dict.get('Type', 'Audio')

  def stream(self):
    '''steam object for this song'''
    return self.connector.get_stream(self.stream_url)

  @property
  def stream_url(self):
    '''stream for this song - not re-encoded'''
    path = '/Audio/{}/universal'.format(self.id)
    return self.connector.get_url(path,
                                  userId=self.connector.userid,
                                  MaxStreamingBitrate=140000000,
                                  Container='opus',
                                  TranscodingContainer='opus',
                                  AudioCodec='opus',
                                  MaxSampleRate=48000,
                                  PlaySessionId=1496213367201 #TODO no hard code
    )


class Person(EmbyObject):
  '''Class representing emby people objects

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
  def role(self):
    '''Role the person played as'''
    return self.object_dict.get('Role', '')

  @role.setter
  def role(self, value):
    self.object_dict['Role'] = value

  @property
  def type(self):
    return self.object_dict.get('Type', 'Person')

  @property
  def primary_image_tag(self):
    return self.object_dict.get('PrimaryImageTag')

  @property
  def premiere_date(self):
    return self.object_dict.get('PremiereDate')


class Image(EmbyObject):
  '''Class representing emby image objects

  Parameters
  ----------
    object_dict : dict
      same as for `EmbyObject`
    connector : embypy.utils.connector.Connector
      same as for `EmbyObject`
  '''
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)


# Game
class Game(EmbyObject):
  '''Class representing emby game objects

  Parameters
  ----------
    object_dict : dict
      same as for `EmbyObject`
    connector : embypy.utils.connector.Connector
      same as for `EmbyObject`
  '''
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

# Book
class Book(EmbyObject):
  '''Class representing emby book objects

  Parameters
  ----------
    object_dict : dict
      same as for `EmbyObject`
    connector : embypy.utils.connector.Connector
      same as for `EmbyObject`
  '''
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
