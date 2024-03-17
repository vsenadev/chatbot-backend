import nltk
from difflib import SequenceMatcher
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ChatbotUtils:
    @staticmethod
    def ensure_nltk_downloads():
        if not nltk.download('punkt', quiet=True):
            nltk.data.find('tokenizers/punkt')
        if not nltk.download('wordnet', quiet=True):
            nltk.data.find('corpora/wordnet')

    @staticmethod
    def preprocess_input(user_input):
        ChatbotUtils.ensure_nltk_downloads()

        lemmatizer = WordNetLemmatizer()
        tokens = nltk.word_tokenize(user_input.lower())
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
        return ' '.join(lemmatized_tokens)

    @staticmethod
    def generate_response(user_input, corpus):
        user_input = ChatbotUtils.preprocess_input(user_input)

        if not hasattr(ChatbotUtils, 'tfidf_vectorizer'):
            ChatbotUtils.tfidf_vectorizer = TfidfVectorizer()
            ChatbotUtils.tfidf_matrix = ChatbotUtils.tfidf_vectorizer.fit_transform(corpus)

        user_input_vector = ChatbotUtils.tfidf_vectorizer.transform([user_input])

        similarities = cosine_similarity(user_input_vector, ChatbotUtils.tfidf_matrix)

        max_similarity_index = similarities.argmax()

        response = corpus[max_similarity_index]
        return response

    @staticmethod
    def get_specification_index(product_specifications):
        index_list = []

        for element in product_specifications['specifications']:
            index_list.append(element.split(':')[0])

        return index_list

    @staticmethod
    def get_specification_value(product_specifications, question):
        specification_object = {}

        for element in product_specifications['specifications']:
            specification_object[element.split(':')[0]] = element.split(':')[1]

        return specification_object.get(question)

    @staticmethod
    def find_product(products, question):
        names_list = []
        similar_product = None
        for element in products:
            names_list.append(element['name'])

        for product in names_list:
            similarity = SequenceMatcher(None, question.lower(), product.lower()).ratio()

            if similarity > 0.4:
                similar_product = product
                break
        return similar_product

    @staticmethod
    def make_question(specifications, question):
        ChatbotUtils.ensure_nltk_downloads()

        return ChatbotUtils.generate_response(question, specifications)
