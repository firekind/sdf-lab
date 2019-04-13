import sqlite3


class Sqlite:
    __instance = None

    def __init__(self):
        if Sqlite.__instance is not None:
            raise Exception("Database already connected.")

        self.connection = sqlite3.connect("database.sqlite3")
        self.cursor = self.connection.cursor()
        Sqlite.__instance = self

    def execute(self, query, args=[]):
        """
        executes a query and returns the result.

        :param query: the query to be executed.
        :param args:  the arguments to be inserted into the query
        :return: the result of the query
        """
        res = self.cursor.execute(query, args).fetchall()
        return res

    def commit(self):
        """
        commits changes made to the database.
        :return: None
        """
        self.connection.commit()

    def close(self):
        """
        closes the connection to the database.
        :return: None
        """
        self.connection.close()

    @staticmethod
    def get_instance():
        """
        returns the created instance of this class.

        :return: the instance of this class.
        """
        if Sqlite.__instance is None:
            Sqlite.__instance = Sqlite()
        return Sqlite.__instance
