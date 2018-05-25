#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a mysql tool '


__author__ = 'chenzh'


import sys
import mysql.connector
from mysql.connector import ProgrammingError
from mysql.connector.abstracts import MySQLCursorAbstract


def check_cursor(cursor):
    if isinstance(cursor, MySQLCursorAbstract):
        return cursor
    else:
        return None


def get_tables_name(cursor):

    if isinstance(cursor, MySQLCursorAbstract):
        sql = "show tables"
        cursor.execute(sql)
        tables_name_list = cursor.fetchall()
        tables_name = []
        for list in tables_name_list:
            name = list[0]
            tables_name.append(name)
        return tables_name
    else:
        print("cursor类型错误")
        return []


def get_table_field(cursor, table_name):
    sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '" + table_name + "'"
    cursor = check_cursor(cursor)
    cursor.execute(sql)
    files_name = cursor.fetchall()
    name_list = []
    for name in files_name:
        name_list.append(name[0])
    # print(name_list)
    return name_list


def search_content(cursor, table_name, content):
    # print(table_name)
    fields_name = get_table_field(cursor, table_name)
    first_file_name = fields_name[0]
    cursor = check_cursor(cursor)
    for name in fields_name:
        try:
            count_sql = "select count(*) from " + table_name + " where `" + name + "` like '%" + content + "%'"
            cursor.execute(count_sql)
            count = cursor.fetchone()[0]
            if count > 100:
                print(table_name + "表超过一百条匹配")
            else:
                sql = "select * from " + table_name + " where `" + name + "` like '%" + content + "%'"
                cursor.execute(sql)
                result = cursor.fetchall()
                # print(result)
                field_index = fields_name.index(name)
                for r_item in result:
                    print("table_name = " + table_name + "\t" + first_file_name + " = " + r_item[0] + "\t" + name + " = " + r_item[field_index])
                    print("sql = " + sql)
        except ProgrammingError as e:
            print('error')
            # print("************error************")
            # print("table_name = " + table_name)
            # print("field_name = ")
            # print(fields_name)
            # print("content = " +content)
            # print("count_sql = " + count_sql)
            # print("*****************************")


args = sys.argv
args_len = len(args)
if args_len < 2:
    print("请输入查找内容")
    sys.exit(0)


content = args[1]
user = 'root'
password = 'root'
database = 'buspay'


mysql_conn = mysql.connector.connect(user=user, password=password, database=database)
cursor = mysql_conn.cursor()

tables_name = get_tables_name(cursor)
for name in tables_name:
    # print(name)
    search_content(cursor, name, content)

cursor.close()
mysql_conn.close()

