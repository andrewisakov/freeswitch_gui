import base64
from cryptography import fernet
from aiohttp import web
from aiohttp_route import router
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import aiohttp_jinja2
import jinja2
from settings import config, TEMPLATES
from routes import setup_routes
from database import init_pg, close_pg


def setup_session(app):
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))
    # app.add_routes([web.get('/', handler)])

app = web.Application()

setup_routes(app)
print(config)
app['config'] = config
setup_session(app)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(TEMPLATES, 'templates'))

app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
routes = router(app, ['views'])
print(app.router.routes)
web.run_app(app, port=config['app']['port'])
