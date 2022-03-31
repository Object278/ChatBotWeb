#向机器人发送消息和获取回复的方法，机器人目前在huggingface网站部署
from ast import Str
from tokenize import String
import requests
import json


class Bot:
    def __init__(self, id) -> None:
        #之后应该是通过id或者name来在数据库中查询这个bot的所有信息
        self.model_id = "LeonLi279/DialoGPT-small-harrypotter"
        #之后放入环境变量中
        self.api_token = "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" # get yours at hf.co/settings/tokens

    def __query(self, payload: dict):
        data = json.dumps(payload)
        headers = {"Authorization": f"Bearer {self.api_token}"}
        API_URL = f"https://api-inference.huggingface.co/models/{self.model_id}"
        response = requests.post(API_URL, headers=headers, data=data)
        return response.json()
    
    def wakeup(self) -> None:
        self.__query({'inputs': {'text': 'Wake up'}})

    def send_message(self, message: String) -> Str:
        # form query payload with the content of the message
        payload = {'inputs': {'text': message}}

        response = self.__query(payload)
        bot_response = response.get('generated_text', None)
        
        # we may get ill-formed response if the model hasn't fully loaded
        # or has timed out
        if not bot_response:
            if 'error' in response:
                bot_response = 'BotError'
            else:
                bot_response = 'OtherError'
        return bot_response
