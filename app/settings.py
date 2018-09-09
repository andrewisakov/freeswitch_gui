import pathlib
import yaml


BASE_DIR = pathlib.Path(__file__).parent.parent
TEMPLATES = BASE_DIR.absolute().__str__()
# db_config_path = BASE_DIR / 'config' / 'database.yaml'
config_path = BASE_DIR / 'config' / 'app.yaml'


def get_config(path):
    with open(path) as cfg:
        config = yaml.load(cfg)
    return config


# pg_config = get_config(db_config_path)
config = get_config(config_path)
