class Vacancy:
    """Класс для работы с данными из json"""

    def __init__(self, employer=None, name=None, url=None, requirement=None, salary_from=None, salary_to=None):
        self.employer = employer
        self.name = name
        self.url = url
        self.requirement = requirement
        try:
            if "<highlighttext>" and "</highlighttext>" in self.requirement:
                self.requirement = self.requirement.replace("<highlighttext>", "")
                self.requirement = self.requirement.replace("</highlighttext>", "")
        except TypeError:
            self.requirement = requirement
        self.salary_from = salary_from
        self.salary_to = salary_to

    def __str__(self):
        return f"""
        Наниматель:{self.employer}
        Вакансия: {self.name}
        Ссылка {self.url}
        Описание/требования {self.requirement}
        Зарплата от {self.salary_from}
        Зарплата до {self.salary_to}"""
