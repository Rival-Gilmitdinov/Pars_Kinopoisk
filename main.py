from get_movie_desc import get_movie_desc
from sql_handler import create_table, insert_value, insert_values, select_values_wparams
from excel_handler import make_excel_file, write_excel_data
from find_greatest100movies import movie_links

movies_desc = []

for lnk in movie_links():
    movies_desc.append(get_movie_desc(lnk))

create_table('movies', id='INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY', name='VARCHAR', year='INT', premiere='DATE',
              country='VARCHAR', description='TEXT', rating='FLOAT', mpaa='VARCHAR', adult='BOOL')
create_table('mpaa_rating', id='INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY', movie_id='INT REFERENCES movies (id)',
             mpaa='VARCHAR')
create_table('countries', id='INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY', country_id='INT REFERENCES movies (id)',
              country='VARCHAR')


for desc in movies_desc:
    insert_values('movies', desc)
for i in range(len(movies_desc)):
    insert_value('mpaa_rating', 'mpaa', movies_desc[i]['mpaa'])
for i in range(len(movies_desc)):
    insert_value('countries', 'country', movies_desc[i]['country'])


make_excel_file('films', movies_desc)

countries_data = select_values_wparams('movies', 'country, count(country)', 'GROUP BY country')
write_excel_data('films.xlsx', countries_data, 'По странам', ["Страна", "Количество фильмов"])
rating_data = select_values_wparams('movies', 'name, rating', 'WHERE rating <= 8 ORDER BY rating DESC')
write_excel_data('films.xlsx', rating_data, 'По рейтингу', ["Фильм", "Рейтинг"])
