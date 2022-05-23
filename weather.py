import requests
from bs4 import BeautifulSoup #импорт библиотек

def get_info_about_weather(date): #принимает аргумент как дату, возвращает сообщение
    
    url = "https://yandex.ru/pogoda/moscow/details?via=ms" #парсим с Яндекса
    
    req = requests.get(url) #запрос
    soup = BeautifulSoup(req.text, "lxml") #парсим через lxml
    
    all_days = soup.find_all("article", class_="card") #Массив по тегу артикль с атрибутом кард, массив блоков div`ов на две недели про каждый из дней
    predict_days = [] #Массив, куда записываются дни, которые мы будем предиктить
    
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
            
            continue
        
    if date.lower() == "сегодня": #Далее идёт обычная выборка, сколько дней отправлять
        return predict_days[0]
    
    elif date.lower() == "завтра":
        return predict_days[1]
    
    elif date.lower() == "неделя":
        
        info = ""
        
        for i in range(0, 7):
            info += predict_days[i] + "\n" + "—-------------------------------------------------------------------------------------------—" + "\n"
            
        return info
    
    elif date.lower() == "10 дней":
        
        info = ""
        
        for i in predict_days:
            info += i + "\n" + "—--------------------------------------------------------------------------—" + "\n"
            
        print(len(info))
            
        return info
    
    else:
        
        return "Не понимаю твой формат, доступные: сегодня, завтра, неделя, 10 дней" #Если бот не понял сообщение

