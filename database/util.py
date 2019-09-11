import pymysql
import time
from multiprocessing import Pool, cpu_count


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
        self.port = kw['port']

        self.cusor = self.__connect()
        self.__tables = []
        self._power_mode = False
        # self.__testc()

    def __connect(self):
        conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )
        return conn.cursor()

    def __get_connect(self):
        pass

    @property
    def power_mode(self):
        return self._power_mode

    @power_mode.setter
    def power_mode(self, is_power_mode):
        if is_power_mode:
            # 开启性能模式，初始化线程池
            pass
        else:
            # 关闭性能模式，关闭线程池
            pass

    def __execute_sql(self, sql: str):
        self.cusor.execute(sql)
        res = self.cusor.fetchall()
        return res

    def __power_excute_sql(self, sql):
        pass

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
        return self.__search_field_by_string(content)

    def __search_field_by_string(self, content: str) -> [str]:
        """
        程序遍历查找字段和用sql查找效率差不多(数据库性能不错的情况下)
        :param content:
        :return:
        """
        res = []
        tables = self.list_tables()
        for table in tables:
            fields = self.list_fields(table)
            for field in fields:
                if field.find(content):
                    res.append("table: %s, field: %s" % (table, field))
        return res

    def __search_field_by_sql(self, content: str) -> [str]:
        """
        sql查找字段(数据库性能不错的情况下)和程序遍历效率差不多
        :param content:
        :return:
        """
        tables = self.list_tables()
        res = []
        for table in tables:
            sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' and table_schema = '%s'"
            sql = sql % (table, self.database)
            sql = sql + " and COLUMN_NAME like '%" + content + "%'"
            sql_res = self.__execute_sql(sql)
            sql_res = self.__reduce(sql_res)
            for res_item in sql_res:
                res.append("table: %s, field: %s" % (table, res_item))
        return res

    def search_value_content(self, content: str, t='s') -> [str]:
        if t == 'm':
            res = self.__multi_processes_search_value(content)
        else:
            res = self.__simple_search_value(content)
        return res

    def __simple_search_value(self, content: str) -> [str]:
        res = []
        tables = self.list_tables()
        for table in tables:
            fields = self.list_fields(table)
            first_field = fields[0]
            for field in fields:
                sql_res = self.__search_field_value_content_task(table, first_field, field, content, res)
                # for col_vale in sql_res:
                #     res.append("table: %s, firstField: %s, firstValue: %s. field: %s, value: %s"
                #            % (table, first_field, col_vale[0], field, col_vale[1]))
        return res

    def __multi_processes_search_value(self, content: str) -> [str]:
        res =[]
        search_pool = Pool(processes=cpu_count() * 2)
        tables = self.list_tables()
        for table in tables:
            fields = self.list_fields(table)
            first_field = fields[0]
            for field in fields:
                search_pool.apply_async(self.__search_field_value_content_task(table, first_field, field, content, res), args=())
        search_pool.close()
        search_pool.join()
        return res

    def __search_field_value_content_task(self, table: str, first_field: str, field: str, content: str, r=[]) -> ([str, str]):
        sql = r"select `%s`, `%s` from `%s` where `%s` like "
        sql = sql % (first_field, field, table, field)
        sql = sql + " '%" + content + "%'"
        # print(sql)
        try:
            sql_res = self.__execute_sql(sql)
            for col_vale in sql_res:
                r.append("table: %s, firstField: %s, firstValue: %s. field: %s, value: %s"
                           % (table, first_field, col_vale[0], field, col_vale[1]))
            return sql_res
        except Exception as e:
            print("__search_field_value_content_task exception" , e)
            print("error sql: " + sql)
            return ()

    def close(self):
        # 关闭所有线程池
        pass

    def __testc(self):
        print(self.database)
        print("test")


if __name__ == "__main__":
    data_info = {"host": "localhost",
    "user": "root",
    "password": "root",
    "database": "yct_server"}
    db_util = DataBaseUtil(host="localhost",
    user="root",
    password="root",
    database="yct_server", port=3306)

    # TODO 找一个更好的计算运行时间的方法
    print("runing......")
    start = time.time()
    s = db_util.search_value_content("18813365177", 'm')
    print(time.time() - start)
    # db_util._DataBaseUtil__search_field_value_content_task('order', 'id', 'user_phone', '189')
    # elapsed = (time.process_time() - start)
    # print("Time used:", elapsed)
    # print(s)
    # print(cpu_count())
