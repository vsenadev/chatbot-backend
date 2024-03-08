from flask import request, jsonify, Blueprint
from service.chatbot_service import ChatbotService


class ChatbotController:
    routes_bp = Blueprint('routes_chatbot', __name__)

    @routes_bp.route('/api/v1/product', methods=['POST'])
    def create_product():
        if request.is_json:
            new_product = request.get_json()
            response, status_code = ChatbotService().create_product(new_product['name'], new_product['type_product'])

            return response, status_code

    @routes_bp.route('/api/v1/chatbot', methods=['POST'])
    def create_chatbot():
        if request.is_json:
            new_chatbot = request.get_json()
            response, status_code = ChatbotService().create_chatbot(new_chatbot['product'], new_chatbot['specifications'])

            return response, status_code

    @routes_bp.route('/api/v1/chatbot', methods=['PUT'])
    def update_chatbot():
        if request.is_json:
            new_chatbot = request.get_json()
            response, status_code = ChatbotService().update_chatbot(new_chatbot['product'], new_chatbot['specifications'])

            return response, status_code

    @routes_bp.route('/api/v1/product', methods=['GET'])
    def get_products():
        response, status_code = ChatbotService().get_products()

        return response, status_code            
