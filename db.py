import web
from decouple import config

print('Database is initializing...')

DB_USER = config('DBUSER')
DB_PASS = config('DBPASS')
db = web.database(dbn='mysql', db='db', user=DB_USER, pw=DB_PASS)