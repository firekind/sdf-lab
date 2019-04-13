class CartItem:
    def __init__(self, product, quantity):
        """
        class representing an item in the cart.

        :param product: the product that is added to the cart
        :param quantity: the amount of this product that needs to be
        added to the cart
        """

        self.product = product
        self.quantity = quantity

    @property
    def name(self):
        return self.product.name

    @property
    def ID(self):
        return self.product.id

    @property
    def price(self):
        return self.product.price

    @property
    def manu_name(self):
        return self.product.manu_name

    def __str__(self):
        return f"---------------------------------------\n" \
               f"| Product Name:\t\t{self.name}\n" \
               f"| Product Price:\t{self.price}\n" \
               f"| Total Price:\t\t{self.price*self.quantity}\n" \
               f"| Product Manufacturer:\t{self.manu_name}\n" \
               f"| Quantity:\t\t{self.quantity}\n" \
               f"---------------------------------------"


class Product:
    def __init__(self, id_, name, price, manu_name, category):
        self.id = id_
        self.name = name
        self.price = price
        self.manu_name = manu_name
        self.category = category
        self.rating = None

    def rate(self, rating):
        """
        sets the rating for the product.
        :param rating: new rating of the product
        :return: None
        """
        self.rating = rating

    def __str__(self):
        return f"---------------------------------------\n" \
               f"| Product Name:\t\t{self.name}\n" \
               f"| Product Price:\t{self.price}\n" \
               f"| Product Manufacturer:\t{self.manu_name}\n" \
               f"| Product Category:\t{self.category}\n" \
               f"---------------------------------------"

