import random

def handle_response(message):
    p_message = message.lower()

    if p_message == "hello":
        return "Hey there"

    if p_message == "roll":
        return str(random.randint(1, 7))

    if p_message == "help":
        return "`This is a sample message`"

    return "Use help to see the commands"