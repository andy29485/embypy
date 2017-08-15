#!/usr/bin/env python3

import embypy.utils.connector

class EmbyObject:
  def __init__(self, object_dict, connector):
    self.connector   = connector
    self.object_dict = object_dict
    self.extras      = {}

  @property
  def id(self):
    return self.object_dict.get('Id') or self.object_dict.get('ItemId')

  @property
  def name(self):
    return self.object_dict.get('Name', '')

  @property
  def path(self):
    return self.object_dict.get('Path', '')

  @property
  def type(self):
    return self.object_dict.get('Type')

  @property
  def media_type(self):
    return self.object_dict.get('MediaType')

  @property
  def community_rating(self):
    return self.object_dict.get('CommunityRating')

  @property
  def primary_image_url(self):
    path = '/Items/{}/Images/Primary'.format(self.id)
    return self.connector.get_url(path, attach_api_key=False)

  @property
  def parent_id(self):
    return self.object_dict.get('ParentId')

  @property
  def parent(self):
    if self.parent_id:
      return self.process(self.parent_id)
    else:
      return None

  @property
  def url(self):
    path = '/web/itemdetails.html?id={}'.format(self.id)
    return self.connector.get_url(path, attach_api_key=False)

  def update(self):
    path = 'Users/{{UserId}}/Items/{}'.format(self.id)
    info = self.connector.getJson(path, remote=False)
    self.object_dict.update(info)
    self.extras = {}
    return self

  def process(self, object_dict):
    if not object_dict:
      return object_dict

    if type(object_dict)       == dict and \
       set(object_dict.keys()) == {'Items', 'TotalRecordCount'}:
      object_dict = object_dict['Items']

    if type(object_dict) == list:
      items = []
      for item in object_dict:
        items.append(self.process(item))
      return items

    import embypy.objects.folders
    import embypy.objects.videos
    import embypy.objects.misc

    if type(object_dict) == str:
      obj = embypy.objects.EmbyObject({"Id":object_dict}, self.connector)
      object_dict = obj.update().object_dict

    if object_dict['Type'] == 'Audio':
      return embypy.objects.misc.Audio(object_dict, self.connector)
    if object_dict['Type'] == 'Person':
      return embypy.objects.misc.Person(object_dict, self.connector)
    if object_dict['Type'] == 'Video':
      return embypy.objects.videos.Video(object_dict, self.connector)
    if object_dict['Type'] == 'Movie':
      return embypy.objects.videos.Movie(object_dict, self.connector)
    if object_dict['Type'] == 'Trailer':
      return embypy.objects.videos.Trailer(object_dict, self.connector)
    if object_dict['Type'] == 'AdultVideo':
      return embypy.objects.videos.AdultVideo(object_dict, self.connector)
    if object_dict['Type'] == 'MusicVideo':
      return embypy.objects.videos.MusicVideo(object_dict, self.connector)
    if object_dict['Type'] == 'Episode':
      return embypy.objects.videos.Episode(object_dict, self.connector)
    if object_dict['Type'] == 'Folder':
      return embypy.objects.folders.Folder(object_dict, self.connector)
    if object_dict['Type'] == 'Playlist':
      return embypy.objects.folders.Playlist(object_dict, self.connector)
    if object_dict['Type'] == 'BoxSet':
      return embypy.objects.folders.BoxSet(object_dict, self.connector)
    if object_dict['Type'] == 'MusicAlbum':
      return embypy.objects.folders.MusicAlbum(object_dict, self.connector)
    if object_dict['Type'] == 'MusicArtist':
      return embypy.objects.folders.MusicArtist(object_dict, self.connector)
    if object_dict['Type'] == 'Season':
      return embypy.objects.folders.Season(object_dict, self.connector)
    if object_dict['Type'] == 'Series':
      return embypy.objects.folders.Series(object_dict, self.connector)
    if object_dict['Type'] == 'Game':
      return embypy.objects.misc.Game(object_dict, self.connector)
    if object_dict['Type'] == 'GameSystem':
      return embypy.objects.folders.GameSystem(object_dict, self.connector)
    if object_dict['Type'] == 'Photo':
      return embypy.objects.misc.Photo(object_dict, self.connector)
    if object_dict['Type'] == 'Book':
      return embypy.objects.misc.Book(object_dict, self.connector)
    if object_dict['Type'] == 'Image':
      return embypy.objects.misc.Image(object_dict, self.connector)
    return EmbyObject(object_dict, self.connector)

  def getPrimaryImageUrl(self):
    path = '/Items/' + self.id + '/Images/Primary'
    return urlunparse((self.connector.scheme,
                       self.connector.netloc, path,
                       '', '', ''
    ))

  def __str__(self):
    return self.name

  def __repr__(self):
    return '<{} {}>'.format(self.type, self.id)
