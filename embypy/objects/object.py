#!/usr/bin/env python3

import embypy.utils.connector

class EmbyObject:
  '''Deafult EMby Object Template

  Parameters
  ----------
  object_dict : dict
    dictionary with json info returned from emby
  connector: embypy.utils.connector.Connector
    connector object to make upstream api calls
  '''
  def __init__(self, object_dict, connector):
    self.connector   = connector
    self.object_dict = object_dict
    self.extras      = {}

  def __eq__(self, other):
    return isinstance(other, EmbyObject) and self.id == other.id

  @property
  def id(self):
    '''string with hexidecimal hash representing the id of this
    object in emby
    '''
    return self.object_dict.get('Id') or self.object_dict.get('ItemId')

  @property
  def name(self):
    '''name of the item

    See Also
    --------
      post :
    '''
    return self.object_dict.get('Name', '')

  @name.setter
  def name(self, value):
    self.object_dict['Name'] = value

  @property
  def title(self):
    '''same as name

    See Also
    --------
      post :
    '''
    return self.name

  @title.setter
  def title(self, value):
    self.name = value

  @property
  def path(self):
    '''get the filepath of the media file (not url)

    See Also
    --------
      url :
    '''
    return self.object_dict.get('Path', '')

  @property
  def type(self):
    '''get the object type (general)

    See Also
    --------
      media_type :
    '''
    return self.object_dict.get('Type', 'Object')

  @property
  def media_type(self):
    '''get the object type (specific)

    See Also
    --------
      type :
    '''
    return self.object_dict.get('MediaType', 'Object')

  @property
  def genres(self):
    '''list of genres

    See Also
    --------
      post :
    '''
    return self.object_dict.get('Genres', [])

  @genres.setter
  def genres(self, genres : list):
    self.object_dict['Genres'] = genres

  @property
  def tags(self):
    '''list of tags

    See Also
    --------
      post :
    '''
    return self.object_dict.get('Tags', [])

  @tags.setter
  def tags(self, tags : list):
    self.object_dict['Tags'] = tags

  @property
  def overview(self):
    '''the description of the item

    See Also
    --------
      post :
    '''
    return self.object_dict.get('Overview', '')

  @overview.setter
  def overview(self, value):
    self.object_dict['Overview'] = value

  @property
  def community_rating(self):
    '''int [0-10] with the rating of the item

    See Also
    --------
      post :
    '''
    return self.object_dict.get('CommunityRating', 0)

  @community_rating.setter
  def community_rating(self, value):
    self.object_dict['CommunityRating'] = value

  @property
  def primary_image_url(self):
    '''url of the main poster image'''
    path = '/Items/{}/Images/Primary'.format(self.id)
    return self.connector.get_url(path, attach_api_key=False)

  @property
  def parent_id(self):
    '''id of the parent object

    See Also
    --------
      parent :
    '''
    return self.object_dict.get('ParentId')

  @property
  def parent(self):
    '''parent object as a subclass of EmbyObject

    See Also
    --------
      parent :
    '''
    if self.parent_id:
      return self.process(self.parent_id)
    else:
      return None

  @property
  def url(self):
    '''url of the item

    Notes
    -----
      if remote-adderes was given, then that is used as the base
    '''
    path = '/web/itemdetails.html?id={}'.format(self.id)
    return self.connector.get_url(path, attach_api_key=False)

  def update(self):
    '''reload object info from emby

    See Also
    --------
      refresh : same thing
      send :
      post :
    '''
    path = 'Users/{{UserId}}/Items/{}'.format(self.id)
    info = self.connector.getJson(path, remote=False, Fields='Path,Overview')
    self.object_dict.update(info)
    self.extras = {}
    return self

  def refresh(self):
    '''Same as update

    See Also
    --------
      update :
    '''
    return self.update()

  def send(self):
    '''send data that was changed to emby

    This should be used after using any of the setter. Not necessarily
    immediately, but soon after.

    See Also
    --------
      post: same thing
      update :
      refresh :
    '''
    path = 'Items/{}'.format(self.id)
    resp = self.connector.post(path, data=self.object_dict, remote=False)
    if resp.status_code == 400:
      EmbyObject(self.object_dict, self.connector).update()
      resp = self.connector.post(path, data=self.object_dict, remote=False)
    return resp

  def post(self):
    '''Same as send

    See Also
    --------
      send :
    '''
    return self.send()

  def process(self, object_dict):
    '''[for internal use] convert json into python object

    Parameters
    ----------
    object_dict : dict
      json representation of object from emby

    Notes
    -----
    if a string is given, it is assumed to be an id, obj is returned.
    if a list is given, this method is called for each item in list.

    Returns
    -------
    EmbyObject
      the object that is represented by the json dict
    list
      if input is a list, list is returned
    '''
    try:
      if type(object_dict) == str:
        obj = EmbyObject({"Id":object_dict}, self.connector)
        object_dict = obj.update().object_dict
    except:
      return None

    if not object_dict or isinstance(object_dict, EmbyObject):
      return object_dict

    if type(object_dict)       == dict and \
       set(object_dict.keys()) == {'Items', 'TotalRecordCount'}:
      object_dict = object_dict['Items']

    if type(object_dict) == list:
      items = []
      for item in object_dict:
        item = self.process(item)
        if item:
          items.append(item)
      return items

    import embypy.objects.folders
    import embypy.objects.videos
    import embypy.objects.misc

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

  def __str__(self):
    return self.name

  def __repr__(self):
    return '<{} {}>'.format(self.type, self.id)
