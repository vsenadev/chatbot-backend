from flask import jsonify
from repository.chatbot_repository import ChatbotRepository

class ChatbotService:
    def create_product(self, name, type_product):
        try:
            validate_product = ChatbotRepository().get_product_with_name(name)
            if validate_product:
                return jsonify({"message": "Product already exists in the database, please just inserted product specifications."}), 409
            else:
                ChatbotRepository().create_product(name, type_product)
                return jsonify({"message": "Product inserted successfully."}), 201
        except Exception as error:
            return jsonify({"message": "An error has occurred: {0}".format(error)}), 500

    def create_chatbot(self, product, specifications):
        try:
            validate_product = ChatbotRepository().get_product_with_name(product)
            if validate_product:
                ChatbotRepository().create_chatbot(product, specifications)
                return jsonify({"message": "Product specifications inserted successfully."}), 201
            else:
                return jsonify({"message": "Product does not exist please register."}), 404
        except Exception as error:
            return jsonify({"message": "An error has occurred: {0}".format(error)}), 500  

    def update_chatbot(self, product, specifications):
        try:
            validate_product = ChatbotRepository().get_product_with_name(product)
            if validate_product:
                ChatbotRepository().update_chatbot(product, specifications)
                return jsonify({"message": "Product specifications updated successfully."}), 201
            else:
                return jsonify({"message": "Product does not exist please register."}), 404
        except Exception as error:
            return jsonify({"message": "An error has occurred: {0}".format(error)}), 500    

    def get_products(self):
        try:
            response = ChatbotRepository().get_products()
            return jsonify({"products": response}), 201
        except Exception as error:
            return jsonify({"message": "An error has occurred: {0}".format(error)}), 500
