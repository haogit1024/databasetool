import json


class Config(object):
    def __init__(self):
        print()

    def __init__(self, config_file, host, port, database, user, password, charset):
        self.config_file = config_file
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.charset = charset

    def save_config(self):
        config = {
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'user': self.user,
            'password': self.password,
            'charset': self.charset
        }
        json_config = json.dumps(config)
        self.write_file(json_config)

    def write_file(self, json_config):
        config_file = self.config_file
        try:
            f = open(config_file, 'r')
        except FileNotFoundError as e:
            f = open(config_file, 'w')
            f.write(json_config)
        finally:
            if f:
                f.close()

    def get_config(self):
        with open(self.config_file, 'r') as f:
            json_config = f.read()
            return json.loads(json_config)
