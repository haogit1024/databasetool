import pymysql


class DataBaseUtil(object):
    def __init__(self, **kw):
        """
        初始化工具类
        :param kw:
        :param host        端口号
        :param user        用户名
        :param password    密码
        :param database    数据库
        """
        self.host = kw['host']
        self.user = kw['user']
        self.password = kw['password']
        self.database = kw['database']
        conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cusor = conn.cursor()
        self.__tables = []

    def __execute_sql(self, sql: str):
        self.cusor.execute(sql)
        res = self.cusor.fetchall()
        return res

    def __reduce(self, two_d_arr) -> []:
        """
        二维数组扁平化为一维数组
        """
        res = []
        for one_d_arr in two_d_arr:
            res.append(one_d_arr[0])
        return res

    def list_tables(self) -> [str]:
        if len(self.__tables) == 0:
            sql = r'show tables'
            res = self.__execute_sql(sql)
            self.__tables = self.__reduce(res)
        return self.__tables

    def list_fields(self, table: str) -> [str]:
        sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' and table_schema = '%s'"
        sql = sql % (table, self.database)
        # print(sql)
        res = self.__execute_sql(sql)
        return self.__reduce(res)

    def search_field_content(self, content: str) -> [str]:
        # TODO 改为内部方法并添加sql查询方法
        res = []
        tables = self.list_tables()
        for table in tables:
            fields = self.list_fields(table)
            for field in fields:
                if field.find(content):
                    res.append("table: %s, field: %s" % (table, field))
        return res

    def search_value_content(self, content: str, type='s') -> [str]:
        if type == 'm':
            res = self.__multi_pro_search_value(content)
        else:
            res = self.__simple_search_value(content)
        return res

    def __simple_search_value(self, content: str) -> [str]:
        # TODO 完善
        pass

    def __multi_pro_search_value(self, content: str) -> [str]:
        # TODO 完善
        pass

if __name__ == "__main__":
    data_info = {"host": "localhost",
    "user": "root",
    "password": "root",
    "database": "lonely"}
    db_util = DataBaseUtil(host="localhost",
    user="root",
    password="root",
    database="lonely")
    tables = db_util.list_tables()
    db_util.list_fields(tables[0])
    # print(db_util.search_field_content("id"))
