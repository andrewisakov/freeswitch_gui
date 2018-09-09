from aiopg.sa import create_engine
from models import *


DSN = 'postgresql://{user}:{password}@{host}:{port}/{database}'


async def init_pg(app):
    conf = app['config']['databases']['postgres']
    engine = await create_engine(
        database=conf['database'],
        user=conf['user'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()
