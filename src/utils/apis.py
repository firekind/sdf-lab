import json
import os
import uuid

from entities.actors import User
from utils.database import Sqlite


class DatabaseAPI:
    def __init__(self):
        """
        class that acts as an API for the database.
        """
        self.db = Sqlite.get_instance()

    def authenticate(self, username, password):
        """
        checks if the user exists and if the password provided is right.
        :param username: username of the user
        :param password: password provided by the user
        :return: True, if successful authentication, False otherwise
        """
        res = self.db.execute('select password from users where name=?', [username])
        try:
            if res[0][0] == password:
                return True
            return False
        except IndexError:
            raise AuthenticationException()

    def create_user(self, username, password):
        """
        creates a user entry in the database.
        :param username: the username of the user
        :param password: the password of the user
        :return: None
        """
        self.db.execute('insert into users (id, name, password) values (?, ?, ?)',
                        [str(uuid.uuid4()), username, password]
                        )
        self.db.commit()

    def search_product(self, prod_name, regex=True):
        """
        executes a search query in the database using pattern matching. searches for item
        based on name.
        :param prod_name: the name of the item
        :return: a list containing tuples of the results.
        """
        if regex:
            return self.db.execute(f"select * from items where name like '{str(prod_name)}%'")
        return self.db.execute(f"select * from items where name = '{str(prod_name)}'")

    def dispose(self):
        """
        closes the database.
        :return: None
        """
        self.db.close()


class AuthAPI:
    auth_file = os.path.dirname(os.path.realpath(__file__)) + "/user.json"

    def __init__(self):
        """
        class that handles authenticating the user for signing in.
        """
        self.db_api = DatabaseAPI()

    def login(self, username, password):
        """
        signs the user in.
        :param username: username of the user
        :param password: password of the user
        :return: True if sign in is successful.
        """
        res = self.db_api.authenticate(username, password)
        if res:
            with open(self.auth_file, 'w') as f:
                json.dump({'username': username}, f)
            return User(username)
        raise AuthenticationException()

    def logout(self):
        """
        logs out the user. removes the user.json file and resets the instance
        of the user class, which makes creating another instance of user class
        possible
        :return: None
        """
        User.reset()
        os.remove(self.auth_file)

    def signup(self, username, password):
        """
        creates a user in the database, and logs the user in. user registration.
        :param username: username of the user
        :param password: password of the user
        :return: None
        """
        self.db_api.create_user(username, password)
        self.login(username, password)

    def signin_from_file(self):
        """
        signs in an already signed in user.
        :return: None
        """
        data = json.load(open(self.auth_file, "r"))
        User(username=data['username'])

    @staticmethod
    def is_logged_in():
        return os.path.exists(AuthAPI.auth_file)

    def dispose(self):
        """
        performs cleanup.
        :return: None
        """
        self.db_api.dispose()


class SearchAPI:
    def __init__(self):
        """
        api for searching stuff.
        """
        self.db_api = DatabaseAPI()

    def search_items(self, prod_name):
        """
        searches for products based on product name.
        :param prod_name: the name of the product
        :return: list containing the results.
        """
        return self.db_api.search_product(prod_name)

    def search_item(self, prod_name):
        """
        searches for a single product based on product name.
        :param prod_name: the name of the product
        :return: list containing the result.
        """
        return self.db_api.search_product(prod_name, regex=False)

    def dispose(self):
        """
        performs cleanup.
        :return: None
        """
        self.db_api.dispose()


class AuthenticationException(Exception):
    def __init__(self):
        """
        class that represents an exception that occurs due to error logging in.
        """
        super(AuthenticationException, self).__init__("Invalid username or password")
