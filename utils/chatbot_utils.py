from difflib import SequenceMatcher
import re
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ChatbotUtils:

    def preprocess_input(self, user_input):
        lemmatizer = WordNetLemmatizer()
        tokens = nltk.word_tokenize(user_input.lower())
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

        return ' '.join(lemmatized_tokens)

    def generate_response(self, user_input, corpus):
        user_input = self.preprocess_input(user_input)

        # Vectorize o corpus
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

        # Vectorize a entrada do usuário
        user_input_vector = tfidf_vectorizer.transform([user_input])

        # Calcule a similaridade de cosseno entre a entrada do usuário e as respostas no corpus
        similarities = cosine_similarity(user_input_vector, tfidf_matrix)

        # Encontre o índice da resposta com a maior similaridade
        max_similarity_index = similarities.argmax()

        # Retorne a resposta correspondente ao índice com a maior similaridade
        response = corpus[max_similarity_index]
        return response

    def get_specification_index(self, list):
        index_list = []

        for element in list['specifications']:
            index_list.append(element.split(':')[0])

        return index_list

    def get_specification_value(self, product_specifications, question):
        specification_object = {}

        for element in product_specifications['specifications']:
            specification_object[element.split(':')[0]] = element.split(':')[1]

        return specification_object[question]

    def find_product(self, products, question):
        names_list = []
        max_similarity = 0
        similar_product = None

        for element in products:
            names_list.append(element['name'])

        for product in names_list:
            similarity = SequenceMatcher(None, question.lower(), product.lower()).ratio()

            if similarity > 0.4:
                similar_product = product

        return similar_product

    def make_question(self, specifications, question):
        nltk.download('punkt')
        nltk.download('wordnet')

        return self.generate_response(question, specifications)
