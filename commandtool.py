import click
import mysql
from mysql.connector import ProgrammingError
from mysql.connector.abstracts import MySQLCursorAbstract
import json


@click.command()
@click.option('--oper', default='field', help='field: 查找字段, data: 查找内容')
@click.option('--content', default='', help='搜索内容')
def test_func(oper, content):
    """Simple program that greets NAME for a total of COUNT times."""
    print(oper)
    if oper == 'config':
        host = ''
    elif oper == "field":
        print()
    elif oper == "data":
        print("this is print")
        config = get_config()
        print(config)
        print(content)
        mysql_conn = mysql.connector.connect(**config)
        cursor = mysql_conn.cursor()
        tables_name = get_tables_name(cursor)
        for name in tables_name:
            # print(name)
            search_content(cursor, name, content)
        cursor.close()
        mysql_conn.close()
    else:
        print("无效--oper")


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
    # cursor = check_cursor(cursor)
    for name in fields_name:
        field_index = fields_name.index(name)
        # TODO 添加进程
        run_search_data(cursor, table_name, name, content, first_file_name, field_index)


def run_search_data(cursor, table_name, field_name, content, first_field_name, field_index):
    cursor = check_cursor(cursor)
    try:
        count_sql = "select count(*) from " + table_name + " where `" + field_name + "` like '%" + content + "%'"
        cursor.execute(count_sql)
        count = cursor.fetchone()[0]
        if count > 100:
            print(table_name + "表超过一百条匹配")
        else:
            sql = "select * from " + table_name + " where `" + field_name + "` like '%" + content + "%'"
            cursor.execute(sql)
            result = cursor.fetchall()
            for r_item in result:
                print("table_name = " + table_name + "\t" + first_field_name + " = " + str(
                    r_item[0]) + "\t" + field_name + " = " + r_item[field_index])
    except ProgrammingError as e:
        a = 1
        # print('error')
        # print("************error************")
        # print("table_name = " + table_name)
        # print("field_name = ")
        # print(fields_name)
        # print("content = " +content)
        # print("count_sql = " + count_sql)
        # print("*****************************")


def get_config():
    with open('./config.json', 'r') as f:
        json_config = f.read()
        return json.loads(json_config)


if __name__ == '__main__':
    test_func()
