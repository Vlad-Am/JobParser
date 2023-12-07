import json
import os
from abc import ABC, abstractmethod

import requests


class ApiService(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_connector(self):
        """Возвращает экз класса Connector"""
        pass


class HH(ApiService):
    """Класс для доступа к api hh.ru"""

    vacancies_all = []
    vacancies = []
    vacancies_dict = []

    def __init__(self, vacancies):
        self.vacancies = vacancies

    def get_request(self):
        """Метод для отправки запроса на hh, записывает json
        :return словарь для последующей работы с ним"""

        for num in range(100):
            url = "https://api.hh.ru/vacancies"
            params = {"text": {self.vacancies}, "area": 113, "per_page": 20, "page": num}
            response = requests.get(url, params=params)
            info = response.json()
            if info is None:
                return "Данны не найдены"
            elif "errors" in info:
                return info["errors"][0]["value"]
            elif "items" not in info:
                return "Нет вакансий"
            else:
                for vacancy in range(20):
                    self.vacancies_all.append(vacancy)
                    if info["items"][vacancy] is not None \
                            and info["items"][vacancy]["salary"]["currency"] == "RUR":
                        self.vacancies.append([info["items"][vacancy]["employer"]["name"],
                                              info["items"][vacancy]["name"],
                                              info["items"][vacancy]["apply_alternate_url"],
                                              info["items"][vacancy]["snippet"]["requirement"],
                                              info["items"][vacancy]["salary"]["from"],
                                              info["items"][vacancy]["salary"]["to"]])
        for vacancy in self.vacancies:
            vacancies_dict = {"employer": vacancy[0], "name": vacancy[1], "url": vacancy[2], "requirement": vacancy[3],
                              "salary_from": vacancy[4], "salary_to": vacancy[5]}
            if vacancies_dict["salary_from"] is None:
                vacancies_dict["salary_from"] = 0
            elif vacancies_dict["salary_to"] is None:
                vacancies_dict["salary_to"] = vacancies_dict["salary_from"]
            self.vacancies_dict.append(vacancies_dict)

        with open(f"{self.vacancies}_hh_ru.json" "w", encoding="UTF-8") as file:
            json.dump(self.vacancies_dict, file, indent=4, ensure_ascii=False)
        print(f"Отбор осуществлялся из {len(self.vacancies_all)} вакансий(проверка обращения к сервису)")
        return self.vacancies_dict
    #

                    

    def get_connector(self):
        pass

class SuperJob(ApiService):
    """Класс для доступа к api superjob.ru"""
    vacancies_all = []
    vacancies = []
    vacancies_dict = []
    def __init__(self, vacancies):
        self.vacancies = vacancies
        # load_dotenv()
        self.api_key = os.getenv('SJ_API_KEY', "key_error")

    def get_request(self):
        url = "https://api.superjob.ru/2.0/vacancies/"
        headers = {"X-Api-App-Id": os.getenv("SJ_API_KEY")}
        params = {"keyword": self.vacancies, "per_page": 100, "area": 113, "page": 0}
        while len(self.vacancies) <=50 #кол-во вакансий в поиске
            response = requests.get(url, headers=headers, params= params)

            response_decode = response.content.decode()
            response.close()
            data = json.loads(response_decode)
            vacancies = data['objects']
            for vacancy in vacancies:
                if vacancy['payment_from'] !=0 and vacancy['payment_to'] !=0 and vacancy["curency"] == "rub":
                    try:
                        self.vacancies.append([vacancy['client']["title"], vacancy['profession'], vacancy['link'],
                                               vacancy['candidate'], vacancy['payment_from'], vacancy['payment_to']])
                    except KeyError:
                        continue
            params["page"] += 1
        for vacancy in self.vacancies:
            vacancies_dict = {"employer": vacancy[0], "name": vacancy[1], "url": vacancy[2], "requirement": vacancy[3],
                              "salary_from": vacancy[4], "salary_to":vacancy[5]}
            if vacancies_dict["salary_to"] == 0:
                vacancies_dict["salary_to"] = vacancies_dict["salary_from"]
            self.vacancies_dict.append(vacancies_dict)
            with open(f"{self.vacancies}_sj.json" "w", encoding="UTF-8") as file:
                json.dump(self.vacancies_dict, file, indent=4, ensure_ascii=False)

            return self.vacancies_dict
