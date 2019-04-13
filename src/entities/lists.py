import os
import pickle
import uuid

from entities.item import CartItem, Product


class Cart:
    __instance = None
    cart_file = os.path.dirname(os.path.realpath(__file__)) + "/cart.pkl"

    def __init__(self, user):
        """
        Singleton class (for the same user) representing a cart.

        :param user: the user that is logged in
        """

        if Cart.__instance is not None and Cart.__instance.user is user:
            raise Exception("Cannot create two carts for the same user")
        else:
            self.user = user
            self.items = []
            __instance = self

    def add_item(self, item):
        """
        adds an items to the cart.

        :param item: the item to be added to the cart
        :return: Exception if the item is not an instance of class `CartItem`
        """

        if not isinstance(item, CartItem):
            raise Exception("Only cart items can be added to cart")

        self.items.append(item)

    def remove_item(self, item):
        """
        removes an item from the cart.

        :param item: the item to be removed
        :return: Exception if the item is not there in the cart.
        """

        if item not in self.items:
            raise Exception("Item not in cart")

        self.items.remove(item)

    def save(self):
        """
        pickles the object of this class and saves it.
        :return: None
        """
        with open(self.cart_file, 'wb') as f:
            pickle.dump(self, f)

    def load(self):
        """
        loads cart from pickled object. if pickled object is not present, does nothing.
        :return: None
        """
        try:
            with open(self.cart_file, 'rb') as f:
                data = pickle.load(f)
                self.items = data.items
        except FileNotFoundError:
            pass

    def delete(self):
        """
        deletes the pickled cart object.
        :return: None
        """
        os.remove(self.cart_file)

    @staticmethod
    def get_instance():
        """
        returns the created instance of the cart.

        :return: the instance of this class.
        """
        return Cart.__instance

    @property
    def total_price(self):
        """
        calculates the total cost of items in the cart.
        :return: total cost
        """
        total = 0
        for item in self.items:
            total += item.price * item.quantity
        return total


class Wishlist:
    def __init__(self, name, _id=uuid.uuid4()):
        """
        class that represents a wishlist. User can created multiple named wishlists.

        :param name: name of the wishlist
        :param _id: id of the wishlist
        """
        self.name = name
        self._id = _id
        self.items = []

    def add_item(self, item):
        """
        adds an items to the wishlist.

        :param item: the item to be added to the wishlist
        :return: Exception if the item is not an instance of class `Product`
        """

        if not isinstance(item, Product):
            raise Exception("Only products can be added to the wishlist")

        self.items.append(item)

    def remove_item(self, item):
        """
        removes an item from the wishlist.

        :param item: the item to be removed
        :return: Exception if the item is not there in the wishlist.
        """

        if item not in self.items:
            raise Exception("Item not in wishlist")

        self.items.remove(item)

