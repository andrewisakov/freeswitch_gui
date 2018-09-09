from psycopg2.extras import Json
from aiohttp import web, ClientSession
# from aiohttp_route import route
import aiohttp_jinja2
import json
from database import devices, channels, sim_cards


# @route('GET', '/')
async def index(request):
    return web.Response(text='Hello Freeswitch')


class Device(web.View):
    def get_device_id(self):
        return int(self.request.match_info['device_id']) \
            if self.request.match_info.get('device_id') else None

    @aiohttp_jinja2.template('devices.html')
    async def get(self):
        # print(dir(devices))
        device_data = []
        async with self.request.app['db'].acquire() as conn:
            device_id = self.get_device_id()
            try:
                # device_data = await conn.execute(devices.select().where(id==device_id))
                # device_data = await conn.query(devices).filter_by(id=device_id)
                query = devices.select().where(devices.c.id==device_id)
                # print()
                async for dd in conn.execute(query):
                    _device_data = {k: v for k, v in dd.items()}
                    _device_data['channels'] = []
                    async with ClientSession() as session:
                        resp = await session.get(f'{self.request.scheme}://{self.request.host}/channels/{device_id}')
                        _device_data['channels'] = json.loads(await resp.text())
                    device_data.append(_device_data)
            except Exception as e:
                print(f'get.execption: {e}')
                raise web.HTTPNotFound(text=str(e))
            return web.json_response(device_data)
            # return device_data

    # @route('POST', '/devices/{device_id:\d+}')
    async def post(self):
        pass


class Channels(web.View):
    async def get(self):
        device_id = int(self.request.match_info['device_id']) \
            if self.request.match_info.get('device_id') else None
        # print(f'Channels.get: {device_id}')
        channels_data = []
        async with self.request.app['db'].acquire() as conn:
            query = channels.select().where(channels.c.device_id==device_id).order_by(channels.c.port)
            # print(query.__str__())
            async for ch in conn.execute(query):
                _channel_data = {k: v for k, v in ch.items()}
                del _channel_data['device_id']
                channels_data.append(_channel_data)
        return web.json_response(channels_data)


class Channel(web.View):
    async def get(self):
        pass


class SIMs(web.View):
    async def get(self):
        sims = []
        async with self.request.app['db'].acquire() as conn:
            query = sim_cards.select().order_by(sim_cards.c.phone)
            async for sc in conn.execute(query):
                _sc_data = {k: v for k, v in sc.items()}
                sims.append(_sc_data)
        return web.json_response(sims)


class SIM(web.View):
    async def get(self):
        sim_id = int(self.request.match_info['sim_id']) \
            if self.request.match_info.get('sim_id') else None
        sim_data = []
        async with self.request.app['db'].acquire() as conn:
            query = sim_cards.select().where(sim_cards.c.id==sim_id)
            async for sc in conn.execute(query):
                _sc_data = {k: v for k, v in sc.items()}
                sim_data.append(_sc_data)
        return web.json_response(sim_data)
