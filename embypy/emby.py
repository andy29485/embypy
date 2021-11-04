from simplejson.scanner import JSONDecodeError

import asyncio

from embypy import objects
from embypy.utils import Connector
from embypy.utils.asyncio import async_func


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

    username : str, optional
      username to login, this+password can be used instead of an apikey
    password : str, optional
      password for user to login as

    Attributes
    ----------
    connector : embypy.utils.connector.Connector
      Object used to make api requests, do not use
    '''
    def __init__(self, url, **kargs):
        connector = Connector(url, **kargs)
        super().__init__({'ItemId': '', 'Name': ''}, connector)
        self._partial_cache = {}
        self._cache_lock = asyncio.Condition()

    @async_func
    async def info(self, obj_id=None):
        '''Get info about object id

        |coro|

        Parameters
        ----------
        obj_id : str, list
          if not provided, server info is retured(as a dict).
          Otherwise, an object with that id is returned
          (or objects if `obj_id` is a list).
        '''
        if obj_id:
            try:
                return await self.process(obj_id)
            except JSONDecodeError:
                raise LookupError(
                    'Error object with that id does not exist',
                    obj_id
                )
        else:
            return await self.connector.info()

    @async_func
    async def search(
        self, query,
        sort_map={
            'BoxSet': 0,
            'Series': 1,
            'Movie': 2,
            'Audio': 3,
            'Person': 4
        },
        strict_sort=False
    ):
        '''Sends a search request to emby, returns results

        |coro|

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

        json = await self.connector.getJson('/Search/Hints/', **search_params)
        items = await self.process(json["SearchHints"])

        m_size = len(sort_map)
        return sorted(items, key=lambda x: sort_map.get(x.type, m_size))

    @async_func
    async def latest(self, userId=None, itemTypes='', groupItems=False):
        '''returns list of latest items

        |coro|

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
        json = await self.connector.getJson(
            '/Users/{UserId}/Items/Latest',
            remote=False,
            userId=userId,
            IncludeItemTypes=itemTypes,
            GroupItems=groupItems,
        )
        return await self.process(json)

    @async_func
    async def nextUp(self, userId=None):
        '''returns list of items marked as `next up`

        |coro|

        Parameters
        ----------
        userId : str
          if provided, then the list returned is
          the one that that use will see.

        Returns
        -------
        list
          the itmes that will appear as next up
          (for user if id was given)
        '''
        json = await self.connector.getJson(
            '/Shows/NextUp',
            pass_uid=True,
            remote=False,
            userId=userId
        )
        return await self.process(json)

    @async_func
    async def update(self):
        '''
        reload all cached information

        |coro|

        Notes
        -----
        This is a slow process, and will remove the cache before updating.
        Thus it is recomended to use the `*_force` properties, which will
        only update the cache after data is retrived.
        '''
        raise RuntimeError('why was this called?')
        keys = self.extras.keys()
        self.extras = {}
        for key in keys:
            try:
                func = getattr(self, key, None)
                if asyncio.iscoroutinefunction(func):
                    await func()
                elif asyncio.iscoroutine(func):
                    await func
                elif callable(func):
                    func()
            except asyncio.CancelledError:
                raise
            except Exception:
                pass

    @async_func
    async def create_playlist(self, name, *songs):
        '''create a new playlist

        |coro|

        Parameters
        ----------
        name : str
          name of new playlist
        songs : array_like
          list of song ids to add to playlist
        '''
        data = {'Name': name}
        ids = [i.id for i in (await self.process(songs))]

        if ids:
            data['Ids'] = ','.join(ids)

        # TODO - return playlist(s?)
        await self.connector.post(
            '/Playlists',
            data=data,
            pass_uid=True,
            remote=False
        )

    async def _get_list(
        self,
        types,
        path='/Users/{UserId}/Items',
        extra_fields='',
        limit=200,
        **params
    ):
        # Note: assumes no duplicates returned by jellyfin/emby
        # ---
        # more requests = slower
        # bigger requests = more chances of failure
        # 200 items/request seems to be a nice sweetspot where I'm
        # not getting failures
        total = -1
        last = -1
        fields = 'Path,ParentId,Overview,PremiereDate,DateCreated'
        if extra_fields:
            fields = f'{fields},{extra_fields}'
        hash = (types, path, extra_fields)
        async with self._cache_lock:
            count, event, items = self._partial_cache.get(hash, (0, None, []))

            if event is None:
                event = asyncio.Event()
            self._partial_cache[hash] = (count + 1, event, items)

        if count != 0:
            waiting = True
            while waiting:
                await event.wait()
                async with self._cache_lock:
                    if event.is_set():
                        event.clear()
                        waiting = False

        while len(items) != last and (len(items) < total or total == -1):
            try:
                resp = await self.connector.getJson(
                    path,
                    remote		= False,
                    format		= 'json',
                    recursive		= 'true',
                    includeItemTypes	= types,
                    fields		= fields,
                    sortBy		= 'SortName',
                    sortOrder		= 'Ascending',
                    startIndex		= len(items),
                    limit		= limit,
                    **params
                )
                total = int(resp.get('TotalRecordCount', -1))
                last = len(items)
                items.extend(resp['Items'])
                async with self._cache_lock:
                    count, event, _ = self._partial_cache[hash]
                    self._partial_cache[hash] = (count, event, items)
            except Exception:
                async with self._cache_lock:
                    self._partial_cache[hash] = (count - 1, event, items)
                event.set()
                raise
        # do all the item fetching after we get the full list of item ids
        try:
            return await self.process(items)
        finally:
            async with self._cache_lock:
                count, event, _ = self._partial_cache[hash]
                event.set()
                if count <= 1:
                    del self._partial_cache[hash]
                else:
                    self._partial_cache[hash] = (count - 1, event, items)

    @property
    @async_func
    async def albums(self):
        '''returns list of all albums.

        |force|

        |coro|

        Returns
        -------
        list
          of type :class:`embypy.objects.Album`
        '''
        return self.extras.get('albums') or await self.albums_force

    @property
    @async_func
    async def albums_force(self):
        items = await self._get_list(
            'MusicAlbum',
            extra_fields='Genres,Tags,Artists',
        )
        self.extras['albums'] = items
        return items

    @property
    @async_func
    async def songs(self):
        '''returns list of all songs.

        |force|

        |coro|

        Returns
        -------
        list
          of type :class:`embypy.objects.Audio`
        '''
        return self.extras.get('songs') or await self.songs_force

    @property
    @async_func
    async def songs_force(self):
        items = await self._get_list(
            'Audio',
            extra_fields='Genres,Tags,Artists',
            limit=300,
        )
        self.extras['songs'] = items
        return items

    @property
    @async_func
    async def playlists(self):
        '''returns list of all playlists.

        |force|

        |coro|

        Returns
        -------
        list
          of type :class:`embypy.objects.Playlist`
        '''
        return self.extras.get('playlists') or await self.playlists_force

    @property
    @async_func
    async def playlists_force(self):
        items = await self._get_list('Playlist')
        self.extras['playlists'] = items
        return items

    @property
    @async_func
    async def artists(self):
        '''returns list of all song artists.

        |force|

        |coro|

        Returns
        -------
        list
          of type :class:`embypy.objects.Artist`
        '''
        return self.extras.get('artists', []) or await self.artists_force

    @property
    @async_func
    async def artists_force(self):
        items = await self._get_list(
            'MusicArtist',
            extra_fields='Genres,Tags',
        )
        self.extras['artists'] = items
        return items

    @property
    @async_func
    async def movies(self):
        '''returns list of all movies.

        |force|

        |coro|

        Returns
        -------
        list
          of type :class:`embypy.objects.Movie`
        '''
        return self.extras.get('movies', []) or await self.movies_force

    @property
    @async_func
    async def movies_force(self):
        items = await self._get_list(
            'Movie',
            extra_fields='Genres,Tags,ProviderIds',
            limit=100,
        )
        self.extras['movies'] = items
        return items

    @property
    @async_func
    async def series(self):
        '''returns a list of all series in emby.

        |force|

        |coro|

        Returns
        -------
        list
          of type :class:`embypy.objects.Series`
        '''
        return self.extras.get('series', []) or await self.series_force

    @property
    @async_func
    async def series_force(self):
        items = await self._get_list('Series', extra_fields='Genres,Tags')
        self.extras['series'] = items
        return items

    @property
    @async_func
    async def episodes(self):
        '''returns a list of all episodes in emby.

        |force|

        |coro|

        Returns
        -------
        list
          of type :class:`embypy.objects.Episode`
        '''
        return self.extras.get('episodes', []) or await self.episodes_force

    @property
    @async_func
    async def episodes_force(self):
        items = await self._get_list(
            'Episode',
            extra_fields='Genres,Tags',
            limit=500,
        )
        self.extras['episodes'] = items
        return items

    @property
    @async_func
    async def devices(self):
        '''returns a list of all devices connected to emby.

        |force|

        |coro|

        Returns
        -------
        list
          of type :class:`embypy.objects.Devices`
        '''
        return self.extras.get('devices', []) or await self.devices_force

    @property
    @async_func
    async def devices_force(self):
        items = await self.connector.getJson('/Devices', remote=False)
        items = await self.process(items)
        self.extras['devices'] = items
        return items

    @property
    @async_func
    async def users(self):
        '''returns a list of all users.

        |force|

        |coro|

        Returns
        -------
        list
          of type :class:`embypy.objects.Users`
        '''
        return self.extras.get('users', []) or await self.users_force

    @property
    @async_func
    async def users_force(self):
        items = await self.connector.getJson('/Users', remote=False)
        items = await self.process(items)
        self.extras['users'] = items
        return items
