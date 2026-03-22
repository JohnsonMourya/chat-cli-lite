from google import genai
from google.api_core import exceptions
from dotenv import load_dotenv
from datetime import datetime
import os, json, pathlib

load_dotenv()

with open('setting.json', 'r') as file:
    setting = json.load(fp=file)

client = genai.Client(api_key=os.getenv(f"GEMINI_API_KEY"))

# usage = {}
# for i in range(setting["no_api"]):
#     model ={}
#     for key in list(setting['models'].keys()):
#         model.update({key: {'request': 0}})
#     usage.update({f'api{i}': model})

# for model in client.models.list():
#     print(model.name, model.description)
# exit()

class User_Chat:
    
    def __init__(self) -> None:

        self.current_model = setting['default_model']
        self.chat = client.chats.create(model=self.current_model)
        self.current_file = ""

    def change_model(self, new_model):
        global client
        self.current_model = new_model
        convesation_history = self.chat.get_history()
        self.chat = client.chats.create(model=new_model, history=convesation_history)

    def load_chat(self, file):
        global client
        self.current_file = file
        with open("chats/"+self.current_file, 'r') as f:
            data = json.load(f)
        self.chat = client.chats.create(model=self.current_model, history=data)
        return data

    def new_chat(self):
        self.current_file = ""
        self.chat = client.chats.create(model=self.current_model)

    def save_chat(self, name=""):
        history = []
        chat_history = self.chat.get_history()
        if chat_history == []:
            return None
        now = datetime.now()
        time = now.strftime("%Y_%m_%d_%H_%M_%S")
        if self.current_file == "":
            if str(name) == "":
                self.current_file = time + ".json"
            else: 
                self.current_file = f"{time}_{name}.json"
        for message in chat_history:
            message_dict = {
                    "role": message.role,
                    "parts": [{"text": part.text} for part in message.parts]
                    }
            history.append(message_dict)
        pathlib.Path('chats').mkdir(parents=True, exist_ok=True)
        with open("chats/"+self.current_file, 'w', encoding='utf-8') as f:
            json.dump(history, f)
        return self.current_file

    def call_chat(self, user_input):
        try:
            reponse = self.chat.send_message(user_input)
            return reponse.text
        except Exception as e:
            error_message = str(e).lower()
            if "exceeded" in error_message and "quota" in error_message:
                raise Exception("Daily Quota is exhausted for this model. Please try other model")
            elif "too" in error_message and "many" in error_message:
                raise Exception("You hit temprary rate limit try some time later")
            raise Exception("Some Unknow Error")
    
    def close(self):
        pass


if __name__ == "__main__":
    user_chat = User_Chat()
    while True:
        user = input(">>")
        if user == "exit":
            break
        print(user_chat.call_chat(user))
