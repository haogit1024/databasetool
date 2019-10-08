import json
import os
import shutil
from config import Config

if __name__ == "__main__":
    webapp_path = r'D:\tomcat9\webapps'
    file_list = os.listdir(webapp_path)
    print(file_list)
    war_file_list = []
    if len(file_list) > 0:
        for f in file_list:
            if r'.' in f:
                file_section = f.split(r'.')
                if file_section[1] == 'war':
                    war_file_list.append(file_section[0])
    print(war_file_list)
    for war_file_cache in war_file_list:
        war_file_cache = os.path.join(webapp_path, war_file_cache)
        if os.path.exists(war_file_cache) and os.path.isdir(war_file_cache):
            print(war_file_cache)
            shutil.rmtree(war_file_cache)
