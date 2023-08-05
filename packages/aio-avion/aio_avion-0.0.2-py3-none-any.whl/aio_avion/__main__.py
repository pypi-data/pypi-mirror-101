import asyncio
import os

from . import AviOnBridge

async def main():
    async with AviOnBridge(os.environ.get('EMAIL'), os.environ.get('PASSWORD')) as bridge:
        userInfo = await bridge.get_user_info()
        devices = await bridge.get_devices()
        locations = await bridge.get_locations()
        # products = await bridge.get_products()

        print(f'User Info: {userInfo}')
        print(f'Devices: {devices}')
        print(f'Locations: {locations}')
        # print(f'Products: {products}')


if __name__ == "__main__":
    # execute only if run as a script
    asyncio.run(main())

