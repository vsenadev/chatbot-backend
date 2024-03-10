from run import create_mongo_client
from model.product_model import ProductModel
from model.chatbot_model import ChatbotModel


class ChatbotRepository:
    def __init__(self):
        self.db = create_mongo_client()
        self.chatbot_collection = self.db['chatbot']
        self.product_collection = self.db['product']

    def get_product_with_name(self, name):
        try:
            response = self.product_collection.find_one({"name": name})
            return response
        except Exception as e:
            return e


    def create_product(self, name, type_product):
        try:
            new_product = ProductModel(name, type_product)
            response = self.product_collection.insert_one(new_product.__dict__)
            return response
        except Exception as e:
            return e

    def create_chatbot(self, product, specifications):
        try:
            new_chatbot = ChatbotModel(product, specifications)
            response = self.chatbot_collection.insert_one(new_chatbot.__dict__)
            return response
        except Exception as e:
            return e

    def update_chatbot(self, product, specifications):
        try:
            response = self.chatbot_collection.update_one(
                {'product': product},  
                {'$set': {'specifications': specifications}}
            )
            return response
        except Exception as e:
            return e

    def get_products(self):
        try:
            response = list(self.product_collection.find({}, {'_id': 0}))

            return response
        except Exception as e:
            return e

    def get_product_specifications(self, product_name):
        try:
            response = list(self.chatbot_collection.find({'product': product_name}, {'_id': 0, 'product': 0}))
            return response
        except Exception as e:
            return e       