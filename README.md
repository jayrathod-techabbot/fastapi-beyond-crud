Play list = https://www.youtube.com/watch?v=7DQEQPlBNVM&list=PLEt8Tae2spYnHy378vMlPH--87cfeh33P&index=2

=============================================================================

RUN COMMAND

uv run fastapi dev              -> default in the current directory ( main.py)
uv run fastapi dev index.py     -> 


IF SEPERATE FOLDER THEN 


uv run fastapi dev src/                 ->           find inside src/__init__.py
docker start pg-db redis
=============================================================================

for docker -> Db : postgres
                   Redis



docker start pg-db
docker stop pg-db


docker exec -it pg-db psql -U appuser -d bookly_db


docker start redis


==============================================================================
uv add alembic                                                :  Add db migration ( new table is added so needed)
alembic init -t async migration                               : initialize 
alembic revision --autogenerate -m "init"                     : create migration file
alembic upgrade head                                          : apply migration
