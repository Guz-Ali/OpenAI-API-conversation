import os
from openai import OpenAI
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI

API_KEY_FILENAME = 'apikey'
DEFAULT_SYSTEM_ROLE = 'default'

class GPTMemory:
    def __init__(self):
        self.index = ''
        self.system_role = DEFAULT_SYSTEM_ROLE
        os.environ['OPENAI_API_KEY'] = self.get_file_contents(API_KEY_FILENAME)
        self.client = OpenAI()
    
    def change_system_role(self, role):
        if not role:
            raise Exception
        self.system_role = role
        print('role changed.')

    def rag_from_directory(self, directory, glob='*.txt'):
        try:
            loader = DirectoryLoader(directory, glob=glob)
            index = VectorstoreIndexCreator().from_loaders([loader])
            self.add_index(index)
            print('files integrated.')
        except Exception as e:
            print('Exception at RAG from dir: ', e)

    def add_index(self, index):
        if not index:
            raise Exception
        self.index = index

    def get_file_contents(self, filename):
        try:
            with open(filename, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print('"%s" file not found' % filename)

    def chat_gpt(self, prompt):
        completion = self.client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': prompt}, 
                {'role': 'system', 'content': self.system_role} 
            ]
        )
        return completion.choices[0].message.content.strip()



if __name__ == '__main__':
    gpt_session = GPTMemory()
    print('GPT session initialized.')
    print('You can "quit", "change role" of the chatbot, "use local data", \
          or chat with it.')
    while True:
        try:
            user_input = input('You:\n')
            if user_input.lower() in ['quit', 'exit', 'close']:
                print('closing.')
                break
            if user_input.lower() in ['change role', 'role', 'system role']:
                new_role = input('Input the new role for Chatbot:\n')
                gpt_session.change_system_role(new_role)
                continue
            if user_input.lower() in ['use local data', 'local data', 'local']:
                directory = input('Directory of the files:\n')
                # file_types = input('Type of files (ex. .txt, .xlsx, ...)')
                gpt_session.index = gpt_session.rag_from_directory(directory)
                continue
            # response = chat_gpt(user_input, system_role)
            # response = rag_file('./data.txt').query(user_input)
            
            response = gpt_session.index.query(user_input, llm=ChatOpenAI())
            print('Chatbot:\n', response)
        except Exception as e:
            print('error, try again.', e)