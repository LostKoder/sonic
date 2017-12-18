import MySQLdb


class Database:
    connection = None

    @staticmethod
    def cursor():
        if Database.connection is None:
            Database.connection = MySQLdb.connect("localhost", "root", "root", "npm")

        return Database.connection.cursor()
