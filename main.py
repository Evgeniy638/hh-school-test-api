import requests
from helper import request_to_vacancies, consist_in_description, consist_in_vacancies, \
    consist_in_vacancy, consist_in_name, consist_in_company_name


def test_base_search():
    params = {
        'text': 'продажи'
    }
    response = request_to_vacancies(params)
    data = response.json()
    consist_in_vacancies(data['items'], 'продаж',
                         "ошибка в базовой проверке с учётом словоформ")

    print("\nПроверка с учётом словоформ прошла успешно")


def test_search_without_word_forms():
    check_search_without_word_forms('продажи')
    check_search_without_word_forms('"продажи автомобилей"')

    print("\nПроверка без учёта словоформ прошла успешно")


# метод помогает при проверке поиска слова или фразы без учёта словоформ
def check_search_without_word_forms(search_string):
    params = {
        'text': '!' + search_string
    }
    response = request_to_vacancies(params)
    data = response.json()
    found_without_word_forms = data['found']
    items = data['items']
    consist_in_vacancies(items, search_string.replace('"', ''), "ошибка в базовой проверке без учёта словоформ у слов")

    found_word = request_to_vacancies({'text': 'продажи'}).json()['found']
    assert found_word >= found_without_word_forms, "количество найденных вакансий без учёта словоформ " \
                                                   "не может быть больше " \
                                                   "чем количество найденных вакансий с учётом " \
                                                   "\nОшибка возникла при поиске строки: " + search_string


def test_unlimited_character_set():
    params = {
        'text': 'био*'
    }
    data = request_to_vacancies(params).json()
    consist_in_vacancies(data['items'], "био", "ошибка в неограниченном наборе символов")

    print("\nПроверка поиска с неограниченным набором символов прошла успешно")


def test_search_for_one_of_the_words():
    params = {
        'text': '!продажи OR !автомобили OR !"ценные бумаги"'
    }

    data = request_to_vacancies(params).json()

    for i in range(len(data['items'])):
        item = data['items'][i]

        assert consist_in_vacancy(item, "продажи") or \
               consist_in_vacancy(item, "автомобили") or \
               consist_in_vacancy(item, "ценные бумаги"), "Ошибка в поиске одного из слов"

    print("\nПроверка поиска одного из слов прошла успешно")


def test_search_all_words():
    params = {
        'text': '!продажи AND !"ценные бумаги"'
    }

    data = request_to_vacancies(params).json()

    for i in range(len(data['items'])):
        item = data['items'][i]

        assert consist_in_vacancy(item, "продажи") and \
               consist_in_vacancy(item, "ценные бумаги"), "Ошибка в поиске всех слов"

    print("\nПроверка поиска всех слов прошла успешно")


def test_exclude_word():
    params = {
        'text': 'NOT !продажи'
    }

    data = request_to_vacancies(params).json()

    for i in range(len(data['items'])):
        item = data['items'][i]

        assert not consist_in_vacancy(item, "продажи"), "Ошибка поиска с исключением слов"

    print("\nПроверка поиска с исключением слова прошла успешно")


def test_combining_multiple_conditions():
    params = {
        'text': '(!продажи OR NOT !продавец) AND (!"ценные бумаги" OR !специалист)'
    }

    data = request_to_vacancies(params).json()

    for i in range(len(data['items'])):
        item = data['items'][i]

        assert (consist_in_vacancy(item, "продажи") or not consist_in_vacancy(item, "продавец")) and \
               (consist_in_vacancy(item, "ценные бумаги") or consist_in_vacancy(item, "специалист")), \
            "Ошибка поиска с объединением нескольких условий"

    print("\nПроверка поиска с объединением нескольких условий прошла успешно")


def test_search_by_field():
    params = {
        'text': 'NAME:(!python) AND COMPANY_NAME:(!Headhunter OR !Яндекс) OR DESCRIPTION:(!javascript)'
    }

    data = request_to_vacancies(params).json()

    for i in range(len(data['items'])):
        item = data['items'][i]

        assert consist_in_name(item, "python") and \
               (consist_in_company_name(item, 'Headhunter') or consist_in_company_name(item, 'Яндекс')) or \
               consist_in_description(item, "javascript"), \
            "Ошибка поиска по полям\nid: " + str(item['id'])

    print("\nПроверка поиска по полям прошла успешно")
