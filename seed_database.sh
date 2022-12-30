!/bin/bash

rm db.sqlite3
rm -rf ./kwizzedapi/migrations
python3 manage.py makemigrations kwizzedapi
python3 manage.py migrate
python3 manage.py loaddata users
python3 manage.py loaddata players
python3 manage.py loaddata tokens
python3 manage.py loaddata categories
python3 manage.py loaddata questions
python3 manage.py loaddata answers
python3 manage.py loaddata player_responses
python3 manage.py loaddata reviews
python3 manage.py loaddata achievements
