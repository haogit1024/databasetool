#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 一个给用户授权的文件的脚本 """

import os


# 需要授权的目录
dirs = [r'/logs', r'/opt/tomcat8081_dev/logs', r'/opt/tomcat8080_test/logs']


def main():
    users = os.listdir(r'/home')
    base_cmd = r'chown -R {user} {dir}'
    for user in users:
        for dir in dirs:
            cmd = base_cmd.format(user=user, dir=dir)
            ret = os.system(cmd)
            print(ret)


if __name__ == "__main__":
    main()
