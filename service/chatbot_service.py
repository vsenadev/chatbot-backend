from flask import jsonify
from repository.chatbot_repository import ChatbotRepository
from utils.chatbot_utils import ChatbotUtils


class ChatbotService:
    HTTP_STATUS_OK = 200
    HTTP_STATUS_CREATED = 201
    HTTP_STATUS_NOT_FOUND = 404
    HTTP_STATUS_CONFLICT = 409
    HTTP_STATUS_INTERNAL_SERVER_ERROR = 500

    def __init__(self):
        self.repository = ChatbotRepository()
        self.utils = ChatbotUtils()

    def _handle_exception(self, error_message, status_code):
        return jsonify({"message": f"An error has occurred: {error_message}"}), status_code

    def _check_product_exists(self, product_name):
        return self.repository.get_product_with_name(product_name)

    def create_product(self, name, type_product):
        try:
            if len(list(self._check_product_exists(name))) > 0:
                return jsonify({"message": "Product already exists in the database, please just insert product "
                                           "specifications."}), self.HTTP_STATUS_CONFLICT
            else:
                self.repository.create_product(name, type_product)
                return jsonify({"message": "Product inserted successfully."}), self.HTTP_STATUS_CREATED
        except Exception as error:
            return self._handle_exception(error, self.HTTP_STATUS_INTERNAL_SERVER_ERROR)

    def create_chatbot(self, product, specifications):
        try:
            if self._check_product_exists(product):
                self.repository.create_chatbot(product, specifications)
                return jsonify({"message": "Product specifications inserted successfully."}), self.HTTP_STATUS_CREATED
            else:
                return jsonify({"message": "Product does not exist, please register."}), self.HTTP_STATUS_NOT_FOUND
        except Exception as error:
            return self._handle_exception(error, self.HTTP_STATUS_INTERNAL_SERVER_ERROR)

    def update_chatbot(self, product, specifications):
        try:
            if self._check_product_exists(product):
                self.repository.update_chatbot(product, specifications)
                return jsonify({"message": "Product specifications updated successfully."}), self.HTTP_STATUS_OK
            else:
                return jsonify({"message": "Product does not exist, please register."}), self.HTTP_STATUS_NOT_FOUND
        except Exception as error:
            return self._handle_exception(error, self.HTTP_STATUS_INTERNAL_SERVER_ERROR)

    def get_products(self):
        try:
            response = self.repository.get_products()
            return jsonify({"products": response}), self.HTTP_STATUS_OK
        except Exception as error:
            return self._handle_exception(error, self.HTTP_STATUS_INTERNAL_SERVER_ERROR)

    def get_product_specifications(self, product_name):
        try:
            response = self.repository.get_product_specifications(product_name)
            specification_index = self.utils.get_specification_index(response[0])
            return jsonify({'index': specification_index}), self.HTTP_STATUS_OK
        except Exception as error:
            return self._handle_exception(error, self.HTTP_STATUS_INTERNAL_SERVER_ERROR)

    def get_question_specification(self, product_name, question):
        try:
            get_product_specifications = self.repository.get_product_specifications(product_name)
            specification_object = self.utils.get_specification_value(get_product_specifications[0], question)
            return jsonify({'answer': specification_object}), self.HTTP_STATUS_OK
        except Exception as error:
            return self._handle_exception(error, self.HTTP_STATUS_INTERNAL_SERVER_ERROR)

    def get_specification_with_message(self, question):
        try:
            get_products = self.repository.get_products()
            find_product = self.utils.find_product(get_products, question)

            if find_product is None:
                return jsonify({'answer': 'Product not found, please ask a better question'}), self.HTTP_STATUS_OK

            get_product_specifications = self.repository.get_product_specifications(find_product)

            chatbot_answer = self.utils.make_question(get_product_specifications[0]['specifications'], question)

            return jsonify({'answer': chatbot_answer.split(':')[1]}), self.HTTP_STATUS_OK
        except Exception as error:
            return self._handle_exception(error, self.HTTP_STATUS_INTERNAL_SERVER_ERROR)
