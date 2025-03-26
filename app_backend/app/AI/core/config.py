from langchain_openai import ChatOpenAI
from openai import OpenAI
class AIModel:
    def __init__(self):
        self.model = None
        self.init_model() 

    def init_model(self):
        self.model = ChatOpenAI(temperature=0 ,model="gpt-4-turbo")

client= AIModel()
