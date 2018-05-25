import json

config = {
        'host': '127.0.0.1',
        'port': 3306,
        'database': 'test',
        'user': 'test',
        'password': 'test',
        'charset': 'utf8'
    }
json_str = json.dumps(config)
print(json_str)
print(str('a'))
