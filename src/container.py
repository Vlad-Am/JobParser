import json

from src.engine import HeadHunterAPI, SuperJobAPI


class Container:

    def __init__(self, vacancy):
        self.vacancy_sj = None
        self.vacancy_hh = None
        self.vacancy = vacancy

    def connect_hh(self):
        try:
            with open(f"{self.vacancy}_hh_ru.json", encoding="utf-8") as file:
                self.vacancy_hh = json.load(file)
        except FileNotFoundError:
            print("Создаю новый файл")
            self.vacancy_hh = HeadHunterAPI().get_request(self.vacancy)

    def connect_sj(self):
        try:
            with open(f"{self.vacancy}_sj_ru.json", encoding="utf-8") as file:
                self.vacancy_sj = json.load(file)
        except FileNotFoundError:
            print("Создаю новый файл")
            self.vacancy_sj = SuperJobAPI().get_request(self.vacancy)

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
