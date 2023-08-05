from aio_avion.device import AviOnDevice
from aio_avion.location import AviOnLocation
from aio_avion.user_info import AviOnUserInfo
import aiohttp
import contextlib
from datetime import datetime, timezone

from .config import Configuration

class AviOnBridge(contextlib.AbstractAsyncContextManager):

    def __init__(self, email: str, password: str):
        self._config = Configuration()
        self._email = email
        self._password = password
        config = self._config.read()
        expiration = config.get('auth_token_expiration')
        self._auth_token = config.get('auth_token')
        self._auth_token_expiration = datetime.strptime(expiration, "%Y-%m-%dT%H:%M:%S%z") if expiration is not None else datetime.now(timezone.utc)
        self._refresh_token = config.get('refresh_token')
        self._session = aiohttp.ClientSession()


    def __del__(self):
        data = {
            'auth_token': self._auth_token,
            'auth_token_expiration': datetime.strftime(self._auth_token_expiration, "%Y-%m-%dT%H:%M:%S%z") if self._auth_token_expiration is not None else None,
            'refresh_token': self._refresh_token
        }
        
        self._config.write(data)


    async def __aenter__(self):
        return self


    async def __aexit__(self, exc_type, exc_value, traceback):
        if self._session is not None:
            await self._session.close()
            self._session = None


    async def get_token(self) -> str:
        if self._auth_token is not None and self._auth_token_expiration > datetime.now(timezone.utc):
            return self._auth_token

        body = {'email': self._email, 'password': self._password}

        async with self._session.post('https://api.avi-on.com/sessions', json=body) as resp:
            if resp.status != 201:
                print(await resp.text())
                raise Exception('Error retrieving authorization token.')

            json = await resp.json()

            self._auth_token = json['credentials']['auth_token']
            self._auth_token_expiration = datetime.strptime(json['credentials']['expiration_date'], "%Y-%m-%dT%H:%M:%S%z")
            self._refresh_token = json['credentials']['refresh_token']

            return self._auth_token


    async def get_devices(self):
        headers = await self.__request_headers()

        async with self._session.get('https://api.avi-on.com/user/devices', headers=headers) as resp:
            if resp.status != 200:
                print(f'Status Code: {resp.status}')
                print(f'Content: {await resp.text()}')
                raise Exception('Error retrieving devices.')

            json = await resp.json()
            devices = []

            for d in json['devices']:
                device = AviOnDevice()
                device.id = int(d['id'])
                device.name = d['name']

                devices.append(device)

            return devices

    
    async def get_user_info(self):
        headers = await self.__request_headers()

        async with self._session.get('https://api.avi-on.com/user', headers=headers) as resp:
            if resp.status != 200:
                print(f'Status Code: {resp.status}')
                print(f'Content: {await resp.text()}')
                raise Exception('Error retrieving user info.')

            json = await resp.json()

            userInfo = AviOnUserInfo()
            userInfo.id = int(json['user']['id'])
            userInfo.first_name = json['user']['first_name']
            userInfo.last_name = json['user']['last_name']
            userInfo.email = json['user']['email']

            return userInfo


    async def get_products(self):
        headers = await self.__request_headers()

        async with self._session.get('https://api.avi-on.com/products', headers=headers) as resp:
            if resp.status != 200:
                print(f'Status Code: {resp.status}')
                print(f'Content: {await resp.text()}')
                raise Exception('Error retrieving products.')

            json = await resp.json()

            return json


    async def get_locations(self):
        headers = await self.__request_headers()

        async with self._session.get('https://api.avi-on.com/locations', headers=headers) as resp:
            if resp.status != 200:
                print(f'Status Code: {resp.status}')
                print(f'Content: {await resp.text()}')
                raise Exception('Error retrieving locations.')

            json = await resp.json()
            locations = []

            for l in json['locations']:
                location = AviOnLocation()
                location.id = l['id']
                location.name = l['name']

                locations.append(location)

            return locations


    async def __request_headers(self) -> dict[str, str]:
        token = await self.get_token()

        headers = {
            'Accept': 'application/api.avi-on.v2+json',
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }

        return headers