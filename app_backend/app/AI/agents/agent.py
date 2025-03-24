from openai import OpenAI

client = OpenAI()
chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages= [{"role":"user", "content":"Hello"}]
)
chat_completion.choices[0].message.content

class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = client.chat.completions.create(
                        model="gpt-3.5-turbo", 
                        temperature=0,
                        messages=self.messages)
        return completion.choices[0].message.content
    
        