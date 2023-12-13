from src.container import Container
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

    if user_input == '0':
        print("Программа закончила работу")
        exit()
    user_prof = input("Введите профессию для поиска вакансий по ней\n ").lower()
    vacancies = None
    con = Container(user_prof)
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

    print(f"всего найдено {len(vacancies)} вакансий")

    user_sort = input("Сортировать по зарплате?\n1. Да\n2. Нет\n")
    while user_sort not in ['1', '2']:
        user_sort = input("Сортировать по зарплате?\n1. Да\n2. Нет\n")
    if user_sort == '2':
        for vacancy in vacancies:
            vacancy_class = Vacancy(vacancy["employer"], vacancy["name"], vacancy["url"], vacancy["requirement"],
                                    vacancy["salary_from"], vacancy["salary_to"])

            print(vacancy_class)
    else:
        # сортировка вакансий по зп от большей к меньшей
        vacancy_sort = sorted(vacancies, key=lambda d: int(d['salary_from']), reverse=True)
        for vacancy in vacancy_sort:
            vacancy_class = Vacancy(vacancy["employer"], vacancy["name"], vacancy["url"], vacancy["requirement"],
                                    vacancy["salary_from"], vacancy["salary_to"])

            print(vacancy_class)


if __name__ == "__main__":
    main()
