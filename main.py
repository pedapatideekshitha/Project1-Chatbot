import re
import random
from long_responses import R_ADVICE, R_EATING, unknown

class Chatbot:
    def __init__(self):
        self.memory = {}

    def remember(self, key, value):
        self.memory[key] = value

    def get_memory(self, key):
        return self.memory.get(key, None)

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message, chatbot):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    response('Hello! How can I assist you today?', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('Goodbye! Feel free to return if you have more questions.', ['bye', 'goodbye'], single_response=True)

    # Previous Context
    previous_question = chatbot.get_memory('previous_question')
    if previous_question:
        response(f"You previously asked me about {previous_question}. How can I help you now?", [previous_question.lower()])

    # Basic Questions
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return unknown() if highest_prob_list[best_match] < 1 else best_match

def ask_user_questions(chatbot):
    user_response = input('You: ')
    questions_asked = 0

    while questions_asked < 3 and user_response.lower() not in ['exit', 'quit', 'bye']:
        chatbot.remember(f'answer_{questions_asked + 1}', user_response)
        print('Bot:', get_response(user_response, chatbot))
        questions_asked += 1
        user_response = input('You: ')

    print('Bot: Goodbye! Feel free to return if you have more questions.')


def get_response(user_input, chatbot):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message, chatbot)
    return response

def main():
    chatbot = Chatbot()

    print('Bot:', get_response('hello', chatbot))  # Greeting
    ask_user_questions(chatbot)
    print('Bot:', get_response('goodbye', chatbot))  # Farewell

if __name__ == "__main__":
    main()
