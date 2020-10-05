db = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'miniter'
}

DB_URL = f"mysql + mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"

# db = {
#     'user': 'root',
#     'password': 'root',
#     'host': 'localhost',
#     'port': 3306,
#     'database': 'minitter'
# }
