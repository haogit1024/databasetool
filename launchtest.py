import mysql.connector
import launch
import unittest


class TestLaunch(unittest.TestCase):
    def test_fields(self):
        user = 'root'
        password = 'root'
        database = 'buspay'

        mysql_conn = mysql.connector.connect(user=user, password=password, database=database)
        cursor = mysql_conn.cursor()
        fields = launch.get_table_field(cursor, 'ims_pay_orders')
        print(fields)
