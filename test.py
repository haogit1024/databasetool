import json
from config import Config

if __name__ == "__main__":
    c = Config('./config.json')
    print(c.get_config())
    s = r"%'%s'%"
    print(s % 'fuck')
