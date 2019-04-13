import pickle
import os

from entities.lists import Cart, Wishlist


class User:
    __instance = None
    wishlist_info_file = os.path.dirname(os.path.realpath(__file__)) + "/wishlist-info.pkl"

    def __init__(self, username, email=None):
        """
        represents a user.
        :param username: the username
        :param email: email of the user
        """
        if User.__instance is not None:
            raise MultipleUserException()

        self.username = username
        self.email = email
        self.cart = Cart(self)
        self.orders = []
        self.wishlist_default = Wishlist(name="default")
        self.wishlists = {"default": self.wishlist_default}
        User.__instance = self

    @staticmethod
    def place_order(payment_method, offer):
        """
        places an order.
        :param payment_method: the payment method to be used.
        :param offer: the offer chosen by the user.
        :return: True if order is placed successfully, False otherwise
        """
        return True

    @staticmethod
    def get_current_user():
        """
        gets the currently logged in user.
        :return: The instance of this class
        """
        return User.__instance

    @staticmethod
    def reset():
        """
        resets the currently logged in user. deletes any user related files.
        :return: None
        """
        User.__instance.cart.delete()
        os.remove(User.wishlist_info_file)
        User.__instance = None

    def get_wishlist(self, name):
        """
        returns the wishlist of a given name.
        :param name: the name of the wishlist needed
        :return: object of class `Wishlist` if found, None otherwise.
        """
        return self.wishlists.get(name, None)

    def add_wishlist(self, wishlist):
        """
        adds a wishlist for the user.
        :param wishlist: the wishlist to be added.
        :return: None
        """
        self.wishlists[wishlist.name] = wishlist

    def save_wishlists(self):
        """
        saves wishlists to pickle file. does nothing if file is not found.
        :return: None
        """
        try:
            pickle.dump(self.wishlists, open(self.wishlist_info_file, 'wb'))

        except FileNotFoundError:
            pass

    def create_wishlist(self, name):
        """
        creates a wishlist with the given name.
        :param name: the name of the wishlist
        :return: None
        """
        self.wishlists[name] = Wishlist(name)

    def init(self):
        """
        initializes existing user.
        :return: None
        """
        self.cart.load()
        try:
            wishlists = pickle.load(open(self.wishlist_info_file, 'rb'))
            for wishlist in wishlists:
                self.add_wishlist(wishlists[wishlist])
        except FileNotFoundError:
            pass


class MultipleUserException(Exception):
    def __init__(self):
        super(MultipleUserException, self).__init__("cannot login as another user. logout first")
