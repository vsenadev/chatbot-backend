from flask import Flask
from flask_cors import CORS
from controller.chatbot_controller import ChatbotController

app = Flask(__name__)
CORS(app)

app.register_blueprint(ChatbotController.routes_bp)

