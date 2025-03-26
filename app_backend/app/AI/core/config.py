from langchain_openai import ChatOpenAI
class AIModel:
    def __init__(self):
        self.model = self.init_model() 
    def init_model(self):
        return ChatOpenAI(
            temperature=0,
            model="gpt-4-turbo",
            max_tokens=600, 
            request_timeout=30,
            max_retries=3,
            client=None,
            http_client=None,
            verbose=False
        )

client= AIModel().model()
