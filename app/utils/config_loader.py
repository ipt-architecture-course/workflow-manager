import importlib
import json
import os
<<<<<<< HEAD
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config() -> dict:
    """
    Carrega a configuração a partir do arquivo 'adapters_config.json'.

    :return: Dicionário contendo a configuração.
    :raises FileNotFoundError: Se o arquivo não for encontrado.
    :raises ValueError: Se o arquivo JSON estiver malformado.
    """
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../adapters_config.json'))
    logger.info(f"Tentando carregar configuração de {config_path}")

    if not os.path.exists(config_path):
        logger.error(f"Arquivo de configuração não encontrado: {config_path}")
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            logger.info(f"Configuração carregada com sucesso de {config_path}")
            return config
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao carregar o arquivo JSON: {e}")
        raise ValueError(f"Invalid JSON format in configuration file: {config_path}")

def load_adapters_from_config(config_path: str, factory):
    """
    Carrega os adaptadores da configuração e os registra na fábrica.

    :param config_path: Caminho para o arquivo de configuração.
    :param factory: Instância da fábrica para registrar os adaptadores.
    :raises ImportError: Se o módulo ou classe não for encontrado.
    """
    logger.info(f"Carregando adaptadores de configuração em {config_path}")

    try:
        with open(config_path) as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao carregar o arquivo JSON: {e}")
        raise ValueError(f"Invalid JSON format in configuration file: {config_path}")

    for process_type, adapter_path in config.items():
        try:
            module_path, class_name = adapter_path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            adapter_class = getattr(module, class_name)
            factory.register_processor(process_type, adapter_class())
            logger.info(f"Registrado adaptador '{class_name}' para o tipo '{process_type}'")
        except (ImportError, AttributeError) as e:
            logger.error(f"Erro ao registrar adaptador '{adapter_path}': {e}")
            raise ImportError(f"Could not load adapter '{adapter_path}': {e}")

    import importlib

def validate_config(config: dict):
    for process_type, adapter_path in config.items():
        try:
            module_path, class_name = adapter_path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            getattr(module, class_name)
        except (ImportError, AttributeError):
            raise ValueError(f"Invalid adapter configuration: {adapter_path}")

=======

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
>>>>>>> 4a1bbd2fa7007d6f5600e8226b0c8c326a83d452
