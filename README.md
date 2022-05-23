VK BOT INFO
Бот для социальной сети ВКОНТАКТЕ, умеющий отправлять актуальную статистику о коронавирусе в разных регионах, а так же прогноз погоды в Москве.
Файлы проекта
---
Проект содержит три файла - _main_ запускает самого бота, _weather_ содержит алгоритм о передачи информации с сайта о погоде, а _coronavirus_ - с сайта о коронавирусе.
```
main.py
coronavirus.py
weather.py
```
coronavirus.py
---
__Сбор информации будет вестись с сайта horosho-tam.ru.__
После импорта библиотек, позволяющих нам отправлять запросы и парсить информацию с сайтов, идёт функция _get_info_about_coronavirus(region)_, которая на вход принимает название региона. 


```
import requests
from bs4 import BeautifulSoup

def get_info_about_coronavirus(region): #Функция принимает регион
    
    url = "https://horosho-tam.ru/rossiya/coronavirus" #

    req = requests.get(url) #запрос
    soup = BeautifulSoup(req.text, "lxml") #парсинг   
    
    all_regions = soup.find_all("tbody")[1].find_all("tr") #инфа по всем регионам
    stats_of_all_regions = dict() #словарь из регионов и статуса по ним
```


После получения информации о регионах, начинается процесс сортировки и форматировании данных, в котором и происходит получение необходимой нам статистики о числе заражённых, выздоровевших и т. д.

```
for reg in all_regions:#сортировака и форматирование данных
        
        all_stats_about_current_region = reg.find_all("td") #на каждый регион своя статистика в td
        
        reg_name = all_stats_about_current_region[1].find("a").text #говорящие названия переменных записывают соответвествующую информацию
        
        reg_infection_today = all_stats_about_current_region[2].text
        reg_infection_all = all_stats_about_current_region[6].text
        
        reg_dies_today = all_stats_about_current_region[3].text
        reg_dies_all = all_stats_about_current_region[7].text
        
        reg_recovereds_today = all_stats_about_current_region[5].text
        reg_recovereds_all = all_stats_about_current_region[8].text
        
        stats_of_all_regions.update({reg_name : f"Заражений сегодня: {reg_infection_today}\nЗаражений за всё время: {reg_infection_all}\nСмертей сегодня: {reg_dies_today}\nСмертей за всё время: {reg_dies_all}\nВыздоровело сегодня: {reg_recovereds_today}\nВыздоровело за всё время: {reg_recovereds_all}"})
        #форматирование
```

Так же есть функция подсказки, если пользователь ввёл неверный регион или ввёл его с ошибкой.
```
try:
        return stats_of_all_regions[region] #по ключу возвращаем из словаря всю информацию
    except:
        
        data = "Не найдено региона" #если не найдено ничего, то возвращаем сообщение
        
        for i in stats_of_all_regions: #если подстрока присутствует в словаре, то делаем подсказку
            if region in i:
                data += f", возможно вы имели ввиду {i}"
                break
            
        return data
```

weather.py
---
После импорта библиотек, вызывается функция _get_info_about_weather(date)_, которая принимает дату как аргумент, а возвращает уже готовое сообщение. Парсинг в этот раз происходит с Яндекс.Погода (_yandex.ru/pogoda_).

Так же посылаем на сайт запрос и парсим информацию в удобном для нас формате lxml. В результате запроса мы получаем информацию на две недели, которую мы записываем в массив _all_days_, а необходимые нам дни будут записаны в _predict_days_.
Далее проходимся циклом по каждому элементу и достаём нужную нам информацию о погоде в каждый из промежутков времени.
```
for i in all_days: #дальше проходимся  циклом по каждому элементу внутри all_days
        try: #внутри all_days может попасться реклама с таким же классом `card`, поэтому делаем try.
                   
            day = i.find("span", class_="a11y-hidden").text #текущий день
            info_on_day = i.find("tbody", class_="weather-table__body").find_all("tr") #инфо на каждое время суток
            
            info_on_morning = info_on_day[0].find_all("td")  #на утро
            weather_on_morning = info_on_morning[0].find("span", class_="a11y-hidden").text
            type_on_morning = info_on_morning[2].text
            wind_on_morning = info_on_morning[5].find("span", class_="a11y-hidden").text
            
            info_on_noon = info_on_day[1].find_all("td") #на день
            weather_on_noon = info_on_noon[0].find("span", class_="a11y-hidden").text
            type_on_noon = info_on_noon[2].text
            wind_on_noon = info_on_noon[5].find("span", class_="a11y-hidden").text
            
            info_on_evening = info_on_day[2].find_all("td") #вечер
            weather_on_evening = info_on_evening[0].find("span", class_="a11y-hidden").text
            type_on_evening = info_on_evening[2].text
            wind_on_evening = info_on_evening [5].find("span", class_="a11y-hidden").text
            
            info_on_night = info_on_day[3].find_all("td") #на ночь
            weather_on_night = info_on_night[0].find("span", class_="a11y-hidden").text
            type_on_night = info_on_night[2].text
            wind_on_night = info_on_night[5].find("span", class_="a11y-hidden").text
    
            predict_days.append(f"{day}\n**********\n{weather_on_morning} {type_on_morning}, ветер (м/c): {wind_on_morning}\n//////////\n{weather_on_noon} {type_on_noon}, ветер (м/c): {wind_on_noon}\n//////////\n{weather_on_evening} {type_on_evening}, ветер (м/c): {wind_on_evening}\n//////////\n{weather_on_night} {type_on_night}, ветер (м/c): {wind_on_night}")
            #форматируем данные для вывода     
        except:
```
Далее сам пользователь определяет, на сколько дней он хочет получить прогноз.

main.py
---
Именно функция main запускает данного бота. Здесь идёт импорт наших двух файлов, а так же необходимых библиотек для работы с ВК - _from vk_api.longpoll import VkLongPoll, VkEventType_.
Далее, через функцию send_message, идёт отправление нужного нам сообщения о погоде или коронавирусе.
```
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
```
