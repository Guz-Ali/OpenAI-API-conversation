import os
from openai import OpenAI

filename = 'apikey'
DEFAULT_ROLE = """You are an amateur T-Rap star that sings very
            trashy lines about the topic, even when asked to answer seriously."""
def get_file_contents(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)
API_KEY = get_file_contents(filename)
os.environ["OPENAI_API_KEY"] = API_KEY

client = OpenAI()
system_role = DEFAULT_ROLE

def chat_gpt(prompt, system_role):
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content.strip()


if __name__ == "__main__":
    print("You can 'quit', or 'change role' of the chatbot.")
    while True:
        user_input = input("You:\n")
        if user_input.lower() in ["quit", "exit", "close"]:
            print("closing.")
            break
        if user_input.lower() in ["change role"]:
            new_role = input("Input the new role for Chatbot:\n")
            system_role = new_role
            print("role changed.")
            continue

        response = chat_gpt(user_input, system_role)
        print("Chatbot:\n", response)

