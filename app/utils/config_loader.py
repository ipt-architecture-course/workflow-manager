import importlib
import json
import os

def load_config():
    """
    Loads configuration from the 'adapters_config.json' file.
    """
    # Ajuste para calcular o caminho correto desde a raiz do projeto
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    config_path = os.path.join(project_root, 'adapters_config.json')

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, 'r') as file:
        return json.load(file)

def load_adapters_from_config(config_path, factory):
    with open(config_path) as f:
        config = json.load(f)
    for process_type, adapter_path in config.items():
        module_path, class_name = adapter_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        adapter_class = getattr(module, class_name)
        factory.register_processor(process_type, adapter_class())
