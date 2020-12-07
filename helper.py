import requests
import configparser


settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
settings.read('.env')


headers = {
    'Authorization': settings.get('Token', 'TOKEN')
}


def request_to_vacancies(params):
    return requests.get("https://api.hh.ru/vacancies", headers=headers, params=params)


def consist_in_vacancies(items, search_string, message):
    for i in range(len(items)):
        assert consist_in_vacancy(items[i], search_string), message + "\nошибка в вакансии: " + str(items[i]['id'])


def consist_in_vacancy(item, search_string):
    return consist_in_name(item, search_string) or \
        consist_in_company_name(item, search_string) or \
        consist_in_description(item, search_string)


def consist_in_name(item, search_string):
    return item['name'].lower().find(search_string.lower()) != -1


def consist_in_company_name(item, search_string):
    return item['employer']['name'].lower().find(search_string.lower()) != -1


def consist_in_description(item, search_string):
    data = requests.get("https://api.hh.ru/vacancies/" + str(item['id']), headers=headers).json()

    has_in_key_skills = False

    for i in range(len(data['key_skills'])):
        if data['key_skills'][i]['name'].lower().find(search_string.lower()) != -1:
            has_in_key_skills = True
            break

    return has_in_key_skills or data['description'].lower().find(search_string) != -1
