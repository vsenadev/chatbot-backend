from flask import request, jsonify, Blueprint
from service.chatbot_service import ChatbotService


class ChatbotController:
    routes_bp = Blueprint('routes_chatbot', __name__)

    @routes_bp.route('/api/v1/chatbot', methods=['POST'])
    def create_answer():
        return jsonify({'message': 'sucesso'}), 401
