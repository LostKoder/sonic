import MySQLdb


class Database:
    def __init__(self):
        pass

    connection = None

    @staticmethod
    def cursor():
        if Database.connection is None:
            Database.connection = MySQLdb.connect("localhost", "root", "root", "malltina_crawler")
        return Database.connection.cursor()

    @staticmethod
    def get_connection():
        if Database.connection is None:
            Database.connection = MySQLdb.connect("localhost", "root", "root", "malltina_crawler")
        return Database.connection
