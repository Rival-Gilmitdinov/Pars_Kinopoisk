import requests
from bs4 import BeautifulSoup as bs
from cookies_kinopoisk import params, cookies, headers

def end_url() -> list :
    """Функция отправляет запрос на страницу кинопоиска и создает список ссылок на другие страницы
    Return:
        end_url: Список тэгов на страницы кинопоиска"""
    response = requests.get('https://www.kinopoisk.ru/lists/movies/100_greatest_movies_XXI/',
                            params=params, cookies=cookies, headers=headers)
    root = bs(response.text, 'html.parser')
    end_url = []
    link = root.find_all('a', class_='styles_page__zbGy7')
    for page in link:
        end_url.append(page['href'])
    return end_url

def all_url():
    url = []
    for link in end_url():
        url.append('https://www.kinopoisk.ru' + link )
    return url

def find_movies() -> list:
    """Функция проходит по страницам 100 лучших фильмов XXI века и получает список ссылок всех фильмов
    Return:
        links_film: список тэгов на ссылки всех фильмов из класса 100 лучших фильмов XXI """
    links_film = []
    for link_page in all_url():
        response = requests.get(link_page, params=params, cookies=cookies, headers=headers)
        soup = bs(response.text, 'html.parser')
        films = soup.find_all('a', {'class': 'styles_root__wgbNq'})
        for film in films:
            links_film.append(film['href'])
    return links_film

def movie_links():
    movie_links = []
    for link in find_movies():
        movie_links.append('https://www.kinopoisk.ru' + link)
    return movie_links
