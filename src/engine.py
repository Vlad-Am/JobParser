import json
import os
from abc import ABC, abstractmethod

import requests


class ApiService(ABC):
    @abstractmethod
    def get_request(self, vacancies):
        pass


class HeadHunterAPI(ApiService):
    """Класс для доступа к api hh.ru"""

    def __init__(self):
        self.vacancies_all = []
        self.vac = []
        self.vacancies_dict = []

        print("Подключаюсь к HH.ru")

    def get_request(self, vacancies):
        """Метод для отправки запроса на hh, записывает json"""

        for num in range(49):
            url = "https://api.hh.ru/vacancies"
            params = {"text": vacancies, "area": 113, "per_page": 20, "page": num}
            response = requests.get(url, params=params)
            info = response.json()
            if info is None:
                return "Данны не найдены"
            elif "errors" in info:
                return info["errors"][0]["value"]
            elif "items" not in info:
                return "Нет вакансий"
            else:
                for vacancy in range(len(info["items"])):
                    if (info["items"][vacancy]["salary"] is not None
                            and info["items"][vacancy]["salary"]["currency"] == 'RUR'):
                        self.vac.append([info["items"][vacancy]["employer"]["name"],
                                         info["items"][vacancy]["name"],
                                         info["items"][vacancy]["apply_alternate_url"],
                                         info["items"][vacancy]["snippet"]["requirement"],
                                         info["items"][vacancy]["salary"]["from"],
                                         info["items"][vacancy]["salary"]["to"]])
        for vacancy in self.vac:
            vacancies_dict = {"employer": vacancy[0], "name": vacancy[1], "url": vacancy[2], "requirement": vacancy[3],
                              "salary_from": vacancy[4], "salary_to": vacancy[5]}
            if vacancies_dict["salary_from"] is None:
                vacancies_dict["salary_from"] = 0
            elif vacancies_dict["salary_to"] is None:
                vacancies_dict["salary_to"] = vacancies_dict["salary_from"]
            self.vacancies_dict.append(vacancies_dict)

        with open(f"{vacancies}_hh_ru.json", "w", encoding="UTF-8") as file:
            json.dump(self.vacancies_dict, file, indent=4, ensure_ascii=False)
        print(f"Отбор осуществлялся из {len(self.vac)} вакансий(проверка обращения к сервису)")
        return self.vacancies_dict


class SuperJobAPI(ApiService):
    """Класс для доступа к api superjob.ru"""

    def __init__(self):
        self.vacancies_all = []
        self.vacancies_dict = []
        self.vac = []
        print("Подключаюсь по API  super job")
        self.api_key = os.getenv('SJ_API_KEY', "key_error")

    def get_request(self, vacancies):
        """Метод для отправки запроса на superjob, записывает json"""
        url = "https://api.superjob.ru/2.0/vacancies/"
        headers = {"X-Api-App-Id": os.getenv("SJ_API_KEY")}
        for num in range(20):  # кол-во просматриваемых страниц
            params = {"keyword": vacancies, "per_page": 100, "area": 113, "page": num}
            response = requests.get(url, headers=headers, params=params)
            response_decode = response.content.decode()
            response.close()
            data = json.loads(response_decode)
            # Присвоили значение списка словарей вакансий словарю_all
            self.vacancies_all = data['objects']
            for vacancy in self.vacancies_all:
                if vacancy["currency"] == "rub":
                    try:
                        # Добавили вакансии в список vac
                        self.vac.append([vacancy["id"], vacancy['client']["title"], vacancy['profession'],
                                         vacancy["client"]['link'], vacancy['candidat'], vacancy['payment_from'],
                                         vacancy['payment_to']])
                    except KeyError:
                        continue
                params["page"] += 1
        # Перебираем вакансии полученные с сайта и присваиваем списку словарей значения нужные нам
        for vacancy in self.vac:
            vacancies_dict = {"id": vacancy[0], "employer": vacancy[1], "name": vacancy[2], "url": vacancy[3],
                              "requirement": vacancy[4], "salary_from": vacancy[5], "salary_to": vacancy[6]}
            if vacancies_dict["salary_to"] == 0:
                vacancies_dict["salary_to"] = vacancies_dict["salary_from"]
            self.vacancies_dict.append(vacancies_dict)
            # сохраняем в json формате полученный список словарей
        with open(f"{vacancies}_sj.json", "w", encoding="UTF-8") as file:
            json.dump(self.vacancies_dict, file, indent=4, ensure_ascii=False)
        return self.vacancies_dict
