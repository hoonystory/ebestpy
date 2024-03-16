import sqlite3
from src import const
# from src.utils import file_path as from_variables
# import urllib
# import pymysql
from sqlalchemy import create_engine


class Sqlite3:
    db_path = './t9945.db'
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
