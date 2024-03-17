from flask import Flask
from flask_cors import CORS

from controller.chatbot_controller import ChatbotController

app = Flask(__name__)
CORS(app)


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(ChatbotController.routes_bp)
    return app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(host='0.0.0.0', port=5000)
