from run import create_mongo_client


class ChatbotRepository:
    def __init__(self):
        self.db = create_mongo_client()
        self.collection = self.db['chatbot']
