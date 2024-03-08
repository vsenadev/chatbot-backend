from pymongo import MongoClient
import os
from dotenv import load_dotenv

dotenv_path = '.env'

load_dotenv(dotenv_path)

username = os.getenv('DATAUSER')
password = os.getenv('PASSWORD')
database_url = os.getenv('DATABASE_URL')

connection_string = 'mongodb+srv://{0}:{1}@{2}/?retryWrites=true&w=majority'.format(username, password, database_url)


def create_mongo_client():
    client = MongoClient(connection_string)
    database_name = "Huawei"
    db = client[database_name]
    return db
