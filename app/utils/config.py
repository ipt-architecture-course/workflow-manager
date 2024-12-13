from app.adapters.twiter_adapter import TwitterAdapter

# Credenciais do Twitter (substitua pelas suas)
CONSUMER_KEY = "your_consumer_key"
CONSUMER_SECRET = "your_consumer_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"

# Inicializa o adaptador
twitter_adapter = TwitterAdapter(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)

# Exemplo de processamento
workflow_id = "abc-123"
id_content = "456"

response = twitter_adapter.process(workflow_id, id_content)
print(response)
