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
    engine = None
    status = None

    def __init__(self, *args):
        # set database file path with first argument
        # if len(args) != 0:
        #     self.db_path = from_variables.get_file_path(from_variables.get_database_path(), args[0] + '.db')

        # self.conn = sqlite3.connect(self.db_path)
        # self.cursor = self.conn.cursor()
        self.status = STAND_BY

    def check_login(self):
        if self.status == LOGGED_ON:
            return False
        else:
            return True

    def login(self, database_name):
        """

        :param database_name:
        :return:
        """
        if self.check_login() is False:
            return
        else:
            self.engine = create_engine('mysql+pymysql://root:2413@127.0.0.1:3306/' + database_name, echo=False)
            # log.info('DataBase Connected Successfully Initially')

            self.conn = self.engine.connect()
            self.status = LOGGED_ON

            # return conn
            # return engine

    def execute_query(self, query):
        return self.cursor.execute(query)

    def fetch_all(self):
        return self.cursor.fetchall()

    def get_columns(self):
        return [column[0] for column in self.cursor.description]

