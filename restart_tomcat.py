#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'一个删除缓存重启tomcat的脚本，支持从/bin目录的脚本和从系统服务中关闭和启动tomcat。'


__author__ = 'chenzh'

import os, sys, platform, shutil

def delete_cache(tomcat_home):
    """
    delete tomcat cache: delete tomcat_home/work/Catalina and tomcat_home/conf/Catalina
    """
    work_dir_cache_path = tomcat_home + r"\work\Catalina"
    conf_dir_cache_path = tomcat_home + r"\conf\Catalina"
    if os.path.exists(work_dir_cache_path):
        shutil.rmtree(work_dir_cache_path)
    if os.path.exists(os.path.exists(conf_dir_cache_path)):
        shutil.rmtree(conf_dir_cache_path)

def stop_tomcat_script(tomcat_home, os_type):
    """
    run tomcat_home/bin/shutdown.bat / tomcat_home/bin/shutdown.sh 
    """
    cmd = ''
    if os_type == 'Windows':
        cmd = tomcat_home + "\\bin\\shutdown.bat"
    elif os_type == 'Linux':
        cmd = tomcat_home + "/bin/shutdown.sh"
    # os.popen(cmd)
    os.system(cmd)
    print(cmd)

def start_tomcat_script(tomcat_home, os_type):
    """
    run tomcat_home/bin/startup.bat / tomcat_home/bin/startup.sh 
    """
    cmd = ''
    if os_type == 'Windows':
        cmd = tomcat_home + '\\bin\\startup.bat'
    elif os_type == 'Linux':
        cmd = tomcat_home + "/bin/startup.sh"
    # os.popen(cmd)
    os.system(cmd)
    print(cmd)

def start_tomcat_server(tomcat_server, os_type):
    """
    run net start server_name / service server_name start
    """
    cmd = ''
    if os_type == 'Windows':
        cmd = 'net start {}'.format(tomcat_server)
    elif os_type == 'Linux':
        cmd = 'service {} start'.format(tomcat_server)
    print(cmd)
    os.system(cmd)

def stop_tomcat_server(tomcat_server, os_type):
    """
    run net stop server_name / service server_name stop
    """
    cmd = ''
    if os_type == 'Windows':
        cmd = 'net stop {}'.format(tomcat_server)
    elif os_type == 'Linux':
        cmd = 'service {} stop'.format(tomcat_server)
    print(cmd)
    os.system(cmd)

if __name__ == "__main__":
    """
    如果用系统服务启动和关闭tomcat，需要系统管理员权限。这可能需要会在触发重启脚本的时候暴露管理员密码。
    所以强烈推荐用tomcat/bin目录下的脚本启动和关闭tomcat
    """
    args_length = len(sys.argv)
    # 参数默认值
    # 脚本默认放在webapps目录下, os.path.dirname(os.getcwd())获取上一级目录
    tomcat_home = os.path.dirname(os.getcwd())
    # 类型 1.脚本启动 2.服务启动, 默认是脚本启动
    tocmat_type = 1
    # tomcat服务名，默认为tomcat
    tomcat_server_name = 'tomcat'
    # tomcat_home默认路径 默认脚本放在webapps目录下
    # 第一个参数为操作类型
    if args_length > 1:
        tocmat_type = sys.argv[1]
    # 第二个参数为tomcat_home目录路径或者服务名
    if args_length > 2:
        tomcat_home = sys.argv[2]
    # 第三个参数为tocmat服务名
    if args_length > 3:
        tomcat_server_name = sys.argv[3]
    # 获取操作系统类型 Windows / Liunx 
    os_type = platform.system()
    print('os_type=', os_type)
    if os_type != 'Windows' and os_type != 'Linux':
        print('运行失败，目前只支持Windows和Linux操作系统')
        exit(0)
    if tocmat_type == 2:
        # ! 服务启动需要获取管理员权限 Linux用base和Windows用bat获取
        # 服务启动 完善服务启动
        stop_tomcat_server(tomcat_server_name, os_type)
        delete_cache(tomcat_home)
        start_tomcat_server(tomcat_server_name, os_type)
    else:
        # 脚本启动 
        stop_tomcat_script(tomcat_home, os_type)
        delete_cache(tomcat_home)
        start_tomcat_script(tomcat_home, os_type)
    print("重新启动完成")
    