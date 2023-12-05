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

    def get_connector(self):
        pass
