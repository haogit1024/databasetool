import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="lonely"
)

cusor = conn.cursor()


class DataBaseUtil(object):
    def __init__(self):
        pass

    def execute_sql(self, sql):
        cusor.execute(sql)
        col = cusor.description
        # TODO 测试col是什么类型和值
        print(col)
        res = cusor.fetchall()
        return res


if __name__ == "__main__":
    pass
