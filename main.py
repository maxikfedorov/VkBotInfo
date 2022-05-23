from weather import *
from coronavirus import *
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

MAIN_TOKEN = "d296387d6cc6a036685d913223aa3f2273553c37d2959e36d34eaffbaea81de9120d781e022c5734caa6f"

vk_session = vk_api.VkApi(token = MAIN_TOKEN)
longpoll = VkLongPoll(vk_session)

def send_message(usr_id, text): #сообщение, кому отправить, что отправить

	vk_session.method('messages.send', {'user_id' : usr_id, 'message' : text, 'random_id' : 0})

for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW and event.to_me: #Через if else осуществляем работу бота
        
        if event.text.lower() == "привет":
            
            send_message(event.user_id, "Привет! Я могу отправить тебе актуальную информацию о погоде или коронавирусе, напиши !корона или !погода")
            
        elif event.text.lower() == "!корона":
            
            send_message(event.user_id, "Напиши !корона регион, где регион - название интересующего тебя регона.\nПример: !корона Россия")
            
        elif event.text.lower()[0:7] == "!корона" and len(event.text.lower()) > 6:
    
            send_message(event.user_id, get_info_about_coronavirus(event.text[8::]))
            
        elif event.text.lower() == "!погода":
            
            send_message(event.user_id, "Напиши !погода дата, где дата - интересующая тебя дата.\nПример: !погода сегодня")
            
        elif event.text.lower()[0:7] == "!погода" and len(event.text.lower()) > 6:
                
            send_message(event.user_id, get_info_about_weather(event.text[8::]))
                      
        else:
            
            send_message(event.user_id, "Не смог тебя понять :(\nЯ не умею общаться, зато я умею отправлять актуальную информацию о погоде или коронавирусе.\nНапиши !корона или !погода")
