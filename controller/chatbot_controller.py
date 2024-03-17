from flask import request, jsonify, Blueprint
from service.chatbot_service import ChatbotService


class ChatbotController:
    routes_bp = Blueprint('routes_chatbot', __name__)

    @staticmethod
    def _process_request(request_json, service_method, *args):
        if request.is_json:
            data = request.get_json()
            if all(key in data for key in request_json):
                return service_method(*args, **data)
        return jsonify({'message': 'Dados inválidos'}), 400

    @staticmethod
    @routes_bp.route('/api/v1/product', methods=['POST'])
    def create_product():
        return ChatbotController._process_request(['name', 'type_product'], ChatbotService().create_product)

    @staticmethod
    @routes_bp.route('/api/v1/chatbot', methods=['POST'])
    def create_chatbot():
        return ChatbotController._process_request(['product', 'specifications'], ChatbotService().create_chatbot)

    @staticmethod
    @routes_bp.route('/api/v1/chatbot', methods=['PUT'])
    def update_chatbot():
        return ChatbotController._process_request(['product', 'specifications'], ChatbotService().update_chatbot)

    @staticmethod
    @routes_bp.route('/api/v1/product', methods=['GET'])
    def get_products():
        return ChatbotService().get_products()

    @staticmethod
    @routes_bp.route('/api/v1/chatbot/<string:product_name>', methods=['GET'])
    def get_product_specifications(product_name):
        return ChatbotService().get_product_specifications(product_name)

    @staticmethod
    @routes_bp.route('/api/v1/chatbot/question', methods=['PATCH'])
    def get_product_specifications_with_select():
        return ChatbotController._process_request(['product_name', 'question'],
                                                  ChatbotService().get_question_specification)

    @staticmethod
    @routes_bp.route('/api/v1/chatbot/message', methods=['PATCH'])
    def get_product_specifications_with_message():
        return ChatbotController._process_request(['question'], ChatbotService().get_specification_with_message)
