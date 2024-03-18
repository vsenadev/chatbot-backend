from flask import jsonify
from repository.chatbot_repository import ChatbotRepository
from utils.chatbot_utils import ChatbotUtils

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

    def get_product_specifications(self, product_name):
        try:
            response = ChatbotRepository().get_product_specifications(product_name)
            specification_index = ChatbotUtils().get_specification_index(response[0])

            return jsonify({'index': specification_index}), 201
        except Exception as error:
            return jsonify({"message": "An error has occurred: {0}".format(error)}), 500

    def get_question_specification(self, product_name, question_specification):
        try:
            get_product_specifications = ChatbotRepository().get_product_specifications(product_name)
            specification_object = ChatbotUtils().get_specification_value(get_product_specifications[0], question_specification)

            return jsonify({'answer': specification_object}), 201
        except Exception as error:
            return jsonify({"message": "An error has occurred: {0}".format(error)}), 500

    def get_specification_with_message(self, question_specification):
        try:
            get_products = ChatbotRepository().get_products()
            find_product = ChatbotUtils().find_product(get_products, question_specification)

            if find_product == None:
                return jsonify({'answer': 'Product not found, please ask a better question'}), 201

            get_product_specifications = ChatbotRepository().get_product_specifications(find_product)

            chatbot_answer = ChatbotUtils().make_question(get_product_specifications[0]['specifications'], question_specification)

            return jsonify({'answer': chatbot_answer.split(':')[1]}), 201
        except Exception as error:
            return jsonify({"message": "An error has occurred: {0}".format(error)}), 500
