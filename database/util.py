import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="lonely"
)

cusor = conn.cursor()
# cusor.execute('SELECT VERSION()')
# res = cusor.fetchone()
# print('res: %s' % res)

def execute_sql(sql):
    cusor.execute(sql)
    col = cusor.description
    res = cusor.fetchall()
    print(col)
    print('--------')
    print(res)

# collation_database
# innodb_default_row_format
if __name__ == "__main__":
    sql = input('请输入sql: ')
    execute_sql(sql)
