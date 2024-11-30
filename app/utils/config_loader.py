import importlib
import json

def load_adapters_from_config(config_path, factory):
    with open(config_path) as f:
        config = json.load(f)
    for process_type, adapter_path in config.items():
        module_path, class_name = adapter_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        adapter_class = getattr(module, class_name)
        factory.register_processor(process_type, adapter_class())