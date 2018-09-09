from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date, DateTime, Boolean,
    SmallInteger
)
meta = MetaData()


distributors = Table(
    'distributors', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(64)),
    Column('is_active', Boolean, default=False),
    Column('all_home', Boolean, default=False),
    Column('sms', Boolean, default=False)
)

operators = Table(
    'operators', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(256)),
    Column('distributor_id', Integer, default=-1)
)

sim_cards = Table(
    'sim_cards', meta,
    Column('id', Integer, primary_key=True),
    Column('distributor_id', Integer, ForeignKey(
        'distributors.id'), nullable=True),
    Column('phone', String(10)),
    Column('operator_id', Integer, ForeignKey('operators.id'), nullable=True),
    Column('direction', Integer, nullable=True),
    Column('tag', String(64)),
    Column('is_active', Boolean, default=False),
    Column('service_id', Integer, nullable=True)
)

devices = Table(
    'devices', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(256)),
    Column('address', String(15)),
    Column('max_channels', SmallInteger, default=8),
    Column('realm', String(64), nullable=True)
)

channels = Table(
    'channels', meta,
    Column('id', Integer, primary_key=True),
    Column('device_id', Integer, ForeignKey('devices.id')),
    Column('port', SmallInteger, default=5060),
    Column('sip_login', String(64)),
    Column('sip_password', String(64)),
    # Column('sip_realm', String(1024)),
    Column('sip_register', Boolean, default=False),
    Column('is_active', Boolean, default=True),
    Column('sim_id', Integer, nullable=True),
)


def create_tables(engine):
    # meta = Metadata()
    meta.create_all(bind=engine, tables=[])
