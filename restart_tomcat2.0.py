#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 一个tomcat重启脚本, sb windows 爷不支持了 """


__author__ = 'chenzh'

import os
import time
import shutil
import sys
import string


def delete_tomcat_cache(tomcat_home: str):
    """
    delete tomcat cache: delete tomcat_home/work/Catalina and tomcat_home/conf/Catalina
    """
    # 用os的函数屏蔽系统差异
    # work_dir_cache_path = tomcat_home + r"\work\Catalina"
    # conf_dir_cache_path = tomcat_home + r"\conf\Catalina"
    work_dir_cache_path = os.path.join(tomcat_home, 'work', 'Catalina')
    conf_dir_cache_path = os.path.join(tomcat_home, 'conf', 'Catalina')
    if os.path.exists(work_dir_cache_path):
        shutil.rmtree(work_dir_cache_path)
    if os.path.exists(conf_dir_cache_path):
        shutil.rmtree(conf_dir_cache_path)

def delete_wabapp_cache(tomcat_home: str):
    webapp_path = os.path.join(tomcat_home, r'webapps')
    war_file_list = []
    file_list = os.listdir(webapp_path)
    print(file_list)
    war_file_list = []
    if len(file_list) > 0:
        for f in file_list:
            if r'.' in f:
                file_section = f.split(r'.')
                if file_section[1] == 'war':
                    war_file_list.append(file_section[0])
                    war_file_cache = os.path.join(webapp_path, file_section[0])
                    if os.path.exists(war_file_cache) and os.path.isdir(war_file_cache):
                        shutil.rmtree(war_file_cache)

    
def stop_tomcat(port: str):
    prot_cmd = 'lsof -i:{}'.format(port)
    print('prot_cmd: ' + prot_cmd)
    cmd_ret = os.popen(prot_cmd)
    lines = cmd_ret.readlines()
    print("cmd_ret:")
    print(lines)
    lines_len = len(lines)
    if lines_len == 2:
        pid = __get_pid(lines[1])
        kill_cmd = 'kill -s 9 ' + pid
        print('kill_cmd: ' + kill_cmd)
        os.popen(kill_cmd)


def __get_pid(line: str):
    array = line.split(" ")
    print(array)
    index = 0
    for item in array:
        if item != "":
            index = index + 1
        if index == 2:
            return item


def start_tomcat_server(tomcat_server):
    """
    run tomcat_home/bin/startup.sh
    """
    cmd = tomcat_home + "/bin/startup.sh"
    # os.popen(cmd)
    os.system(cmd)
    print('运行: ' + cmd + " 结束")


if __name__ == "__main__":
    args_length = len(sys.argv)
    if args_length < 2:
        print("请输入端口号")
        exit(0)
    curr_path = os.path.dirname(os.path.abspath(__file__))
    tomcat_home = os.path.dirname(curr_path)
    port = sys.argv[1]
    print("port: " + port)
    stop_tomcat(port)
    delete_tomcat_cache(tomcat_home)
    delete_wabapp_cache(tomcat_home)
    start_tomcat_server(tomcat_home)
