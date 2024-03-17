from run import create_mongo_client
from model.product_model import ProductModel
from model.chatbot_model import ChatbotModel


class ChatbotRepository:
    def __init__(self):
        self.db = create_mongo_client()
        self.chatbot_collection = self.db['chatbot']
        self.product_collection = self.db['product']

    def _execute_query(self, collection, query, projection=None):
        try:
            if projection is None:
                return collection.find(query)
            else:
                return collection.find(query, projection)
        except Exception as e:
            raise e

    def _execute_insert(self, collection, data):
        try:
            return collection.insert_one(data)
        except Exception as e:
            raise e

    def _execute_update(self, collection, query, update):
        try:
            return collection.update_one(query, {'$set': update})
        except Exception as e:
            raise e

    def get_product_with_name(self, name):
        query = {"name": name}
        return self._execute_query(self.product_collection, query)

    def create_product(self, name, type_product):
        new_product = ProductModel(name, type_product)
        return self._execute_insert(self.product_collection, new_product.__dict__)

    def create_chatbot(self, product, specifications):
        new_chatbot = ChatbotModel(product, specifications)
        return self._execute_insert(self.chatbot_collection, new_chatbot.__dict__)

    def update_chatbot(self, product, specifications):
        query = {'product': product}
        update = {'specifications': specifications}
        return self._execute_update(self.chatbot_collection, query, update)

    def get_products(self):
        return list(self._execute_query(self.product_collection, {}, {'_id': 0}))

    def get_product_specifications(self, product_name):
        query = {'product': product_name}
        projection = {'_id': 0, 'product': 0}
        return self._execute_query(self.chatbot_collection, query, projection)
