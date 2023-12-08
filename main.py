# Создание экземпляра класса для работы с API сайтов с вакансиями
from src.Connector import Connector
from src.vacancy import Vacancy


def main():
    user_input = input("""Выберете ресурс для поиска\n
                        1. HeadHunter\n
                        2. SuperJob\n
                        0. Exit\n""")
    while user_input not in ['1', '2', '0']:
        user_input = input("""Выберете ресурс для поиска\n
                            1. HeadHunter\n
                            2. SuperJob\n
                            0. Exit\n""")
    user_proff = input("Введите профессию для поиска вакансий по ней")
    vacancies = None
    con = Connector(user_proff)
    if user_input == '1':
        try:
            con.connect_hh()
        except IndexError:
            print("Вакансий не найдено")
            exit()
        vacancies = con.select_hh()
    elif user_input == '2':
        try:
            con.connect_sj()
        except IndexError:
            print("Вакансий не найдено")
            exit()
        vacancies = con.select_sj()
    else:
        print("Программа закончила работу")
        exit()
    print(f"всего найдено {len(vacancies)} вакансий")
    for vacancy in vacancies:
        vacancy_class = Vacancy(vacancy["employer"], vacancy["name"], vacancy["url"], vacancy["requirement"],
                                vacancy["salary_from"], vacancy["salary_to"])
        print(vacancy_class)
        user_sort = input("Сортировать по зарплате?\n1. Да\n2. Нет\n")
        if user_sort == '1':
            for sort in sorting(vacancies)
            print(vacancies)
if __name__ == "__main__":
    main()