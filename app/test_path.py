import os

config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app/utils/config_loader.py'))
print(f"Config loader path: {config_path}")

config_path_json = os.path.abspath(os.path.join(os.path.dirname(__file__), 'adapters_config.json'))
print(f"Adapters config path: {config_path_json}")
