import sqlite3
from src import const
# from src.utils import file_path as from_variables
# import urllib
# import pymysql
from sqlalchemy import create_engine


# import pandas as pd
# import xasys

# from urllib.request import urlopen
# from bs4 import BeautifulSoup

class MySql:
    db_path = ''
    conn = None
    cursor = None

    def __init__(self, *args):
        # set database file path with first argument
        # if len(args) != 0:
        #     self.db_path = from_variables.get_file_path(from_variables.get_database_path(), args[0] + '.db')

        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def execute_query(self, query):
        return self.cursor.execute(query)

    def fetch_all(self):
        return self.cursor.fetchall()

    def get_columns(self):
        return [column[0] for column in self.cursor.description]


STAND_BY = 0
LOGGED_ON = 1


class DBConnect:
    connect_state = STAND_BY

    # print('DBLoginState: ' + str(connect_state))

    def __init__(self):
    # self.pid = xasys.return_pid()

    def chkLogin(self):
        if DBConnect.connect_state == LOGGED_ON:
            return False
        else:
            return True

    def login(self, dbName, log):
        """
        :param dbName:
        :return:
        """
        if self.chkLogin() is False:
            log.info('DataBase Connected Already!')
            # print('---[p' + str(self.pid) + ' Info] DataBase Connected Already!')
            return
        else:
            engine = create_engine('mysql+pymysql://root:2413@127.0.0.1:3306/' + dbName, echo=False)
            log.info('DataBase Connected Successfully Initially')
            # print('---[p' + str(self.pid) + ' Info] DataBase Connected Successfully Initially')

            conn = engine.connect()
            DBConnect.connect_state = LOGGED_ON

            # return conn
            return engine

# class dbconnYN:
#     def __init__(self):
#         self.conn_state = 0
#
#     def connYN(self, dbNm):
#         if dbConnect(dbNm) is not None:
#             self.conn_state = 1
#
#         return self.conn_state


# engine = dbConnect()
# test = pd.read_sql('select * from test', con=engine)
# print(test)
#
# engine.close()
