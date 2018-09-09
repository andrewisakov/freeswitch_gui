import views


def setup_routes(app):
    app.router.add_get('/', views.index)
    app.router.add_get('/device/{device_id:\d+}', views.Device)
    app.router.add_get('/channel/{channel_id:\d+}', views.Channel)
    app.router.add_get('/channels/{device_id:\d+}', views.Channels)
    app.router.add_get('/sim_cards', views.SIMs)
    app.router.add_get('/sim_card/{sim_id:\d+}', views.SIM)
