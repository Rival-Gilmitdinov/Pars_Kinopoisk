from bs4 import BeautifulSoup as bs
import requests
from cookies_kinopoisk import params, cookies, headers
# from main import movie_links

def get_movie_desc(lnk) -> dict:
    """функция парсит данные из кинопоиска и собирает их в словарь
    Args:
        lnk: объект цикла, который проходит по списку ссылок фильмов кинопоиска
    Return:
        dict: данные из фильма кинопоиска в одном словаре """
    movie = requests.get(lnk, params=params, cookies=cookies, headers=headers)
    movie_desc = {'name': '', 'year': '', 'premiere': '', 'country': '', 'description': '', 'rating': '', 'mpaa': '', 'adult': ''}

    root = bs(movie.text, 'html.parser')
    name = root.find(name='span', attrs={'data-tid': '75209b22'})
    description = root.find(name='p', attrs={'data-tid': 'bbb11238'})
    mpaa = root.find(name='span', attrs={'data-tid': '5c1ffa33'})

    rating = root.find(name='span', attrs={'data-tid': '939058a8'})

    desc_list = []

    desc_html = root.find(name='div', attrs={'data-test-id': 'encyclopedic-table'})
    for i in desc_html.find_all(name='div', attrs={'data-tid': '7cda04a5'}):
        desc_list.append(i.get_text())


    desc_list = '*'.join(desc_list)
    a = desc_list.find('Год производства')
    b = desc_list.find('Страна')
    c = desc_list.find('Жанр')
    d = desc_list.find('Премьера в России')
    e = desc_list.find(',', d)
    f = desc_list.find('Возраст')
    g = desc_list.find('Рейтинг')

    adult = desc_list[f:g][7:-2]
    if len(adult) > 2:
        adult = adult[:2]
    try:
        if int(adult) < 18:
            adult = False
        else:
            adult = True
    except:
        adult = 'пусто'

    date = desc_list[d:e][17:]
    mounths_rus = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    mounths_eng = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for i in mounths_rus:
        if i in date:
            k = mounths_rus.index(i)
            date = date.replace(i, mounths_eng[k])
    date = date.split()
    if len(date) == 0:
        date = ['0000', '00', '00']
    elif len(date[0]) == 1:
        date[0] = '0' + date[0]
    date = '-'.join(date)


    movie_desc['name'] = name.get_text()[:-7]
    movie_desc['year'] = desc_list[a:b][-5:-1]
    movie_desc['premiere'] = date
    movie_desc['country'] = desc_list[b:c][6:-1]
    movie_desc['description'] = description.get_text()
    movie_desc['rating'] = rating.get_text()
    if adult == 'пусто':
        movie_desc['mpaa'] = 'пусто'
    else:
        movie_desc['mpaa'] = mpaa.get_text()
    movie_desc['adult'] = adult

    return movie_desc




