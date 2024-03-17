from pymongo import MongoClient
import os
from dotenv import load_dotenv

dotenv_path = '.env'
load_dotenv(dotenv_path)


def create_mongo_client():
    try:
        username = os.getenv('DATAUSER')
        password = os.getenv('PASSWORD')
        database_url = os.getenv('DATABASE_URL')

        if not (username and password and database_url):
            raise ValueError("Variáveis de ambiente não configuradas corretamente.")

        connection_string = f'mongodb+srv://{username}:{password}@{database_url}/?retryWrites=true&w=majority'
        client = MongoClient(connection_string)
        database_name = "Huawei"
        db = client[database_name]
        return db
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


if __name__ == "__main__":
    db = create_mongo_client()
    if db:
        print("ConexÃ£o ao banco de dados estabelecida com sucesso.")
    else:
        print("Falha ao estabelecer conexÃ£o com o banco de dados.")
