from nltk.chat.eliza import eliza_chatbot

def get_eliza_response(user_input: str) -> str:
    return eliza_chatbot.respond(user_input)

if __name__ == "__main__":
    print("ELIZA Chatbot")
    print("Type 'quit' to stop.\n")
    eliza_chatbot.converse()