import json


class Connector:

    def __init__(self, vacancy):
        self.vacancy = vacancy

    def connect_hh(self):
        try:
            with open(f"{self.vacancy}__hh_ru.json", encoding="utf-8") as file:
                self.vacancy_hh = json.load(file)
        except FileNotFoundError:
            print("Создаю новый файл")
            self.vacancy_hh = HH(self.vacancy).get_request()

    def connect_sj(self):
        try:
            with open(f"{self.vacancy}__sj_ru.json", encoding="utf-8") as file:
                self.vacancy_sj = json.load(file)
        except FileNotFoundError:
            print("Создаю новый файл")
            self.vacancy_sj = SuperJob(self.vacancy).get_request()

    def select_hh(self):
        hh_vacancy = []

        for vacancy in self.vacancy_hh:
            hh_vacancy.append(vacancy)
        return hh_vacancy

    def select_sj(self):
        sj_vacancy = []

        for vacancy in self.vacancy_sj:
            sj_vacancy.append(vacancy)
        return sj_vacancy
