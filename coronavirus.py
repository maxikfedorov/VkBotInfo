import requests
from bs4 import BeautifulSoup

def get_info_about_coronavirus(region): #Функция принимает регион
    
    url = "https://horosho-tam.ru/rossiya/coronavirus" #

    req = requests.get(url) #запрос
    soup = BeautifulSoup(req.text, "lxml") #парсинг   
    
    all_regions = soup.find_all("tbody")[1].find_all("tr") #инфа по всем регионам
    stats_of_all_regions = dict() #словарь из регионов и статуса по ним
    
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
    try:
        return stats_of_all_regions[region] #по ключу возвращаем из словаря всю информацию
    except:
        
        data = "Не найдено региона" #если не найдено ничего, то возвращаем сообщение
        
        for i in stats_of_all_regions: #если подстрока присутствует в словаре, то делаем подсказку
            if region in i:
                data += f", возможно вы имели ввиду {i}"
                break
            
        return data