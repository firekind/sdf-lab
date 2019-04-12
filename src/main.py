import click

from creation.factory import ProductFactory
from entities.actors import User
from entities.item import CartItem
from utils.apis import AuthAPI, AuthenticationException, SearchAPI

auth = None
search = None


@click.group()
def cli():
    pass


@cli.command()
@click.option("--username", required=True)
@click.option("--password", required=True)
def signin(username, password):
    """
    signs the user in.
    :param username: the username of the user
    :param password: the password of the user
    :return: None
    """
    try:
        auth.login(username, password)
    except AuthenticationException as e:
        print(e)
        return

    print("You have successfully logged in")
    dispose()


@cli.command()
def signout():
    """
    signs the user out.
    :return: None
    """
    init_user()
    try:
        auth.logout()
    except FileNotFoundError:
        print("You have already signed out.")
        return
    print("You have successfully logged out.")
    dispose()


@cli.command()
@click.option("--username", required=True)
@click.option("--password", required=True)
def signup(username, password):
    """
    registers a new user.
    :param username: username of the new user.
    :param password: password of the new user.
    :return: None
    """
    try:
        auth.signup(username, password)
    except AuthenticationException as e:
        print(e)
        return

    print("You have successfully signed up and logged in")
    dispose()


@cli.command()
@click.argument("prodname")
def search(prodname):
    """
    searches for a product given a search string.
    :param prodname: the name (or partial name) of the product to be searched
    :return: None
    """
    products_meta = search.search_items(prodname)
    search_res = ProductFactory.create_products(products_meta)

    if search_res is not None:
        print("Products that were found:")
        for product in search_res:
            print(product)
            print()
    else:
        print("No products were found.")

    dispose()


@cli.command()
@click.argument("prodname")
@click.option("--quantity", default=1)
def addtocart(prodname, quantity):
    """
    adds an item to the cart.
    :param prodname: the full name of the product to be added
    :param quantity: the quantity of the product.
    :return: None
    """
    if not AuthAPI.is_logged_in():
        print("Please log in before adding to cart.")
        return
    init_user()

    product_meta = search.search_item(prodname)
    search_res = ProductFactory.create_product(product_meta[0])
    to_add = CartItem(search_res, quantity)
    User.get_current_user().cart.add_item(to_add)
    User.get_current_user().cart.save()
    print(f"{prodname} has been added to cart.")


@cli.command()
@click.argument("prodname")
@click.option("--wishlist", default="default")
def addtowishlist(prodname, wishlist):
    """
    adds an item to the wishlist.
    :param prodname: the full name of the product to be added.
    :param wishlist: the name of the wishlist the product needs to be added to.
    :return: None
    """
    if not AuthAPI.is_logged_in():
        print("Please log in before adding to wishlist.")
        return
    init_user()

    product_meta = search.search_item(prodname)
    search_res = ProductFactory.create_product(product_meta[0])
    try:
        User.get_current_user().get_wishlist(wishlist).add_item(search_res)
        User.get_current_user().save_wishlists()
        print(f"{prodname} has been added to wishlist.")
    except KeyError:
        print("Wishlist does not exist.")


@cli.command()
def viewcart():
    """
    displays the contents of the cart.
    :return: None
    """
    if not AuthAPI.is_logged_in():
        print("Please log in before viewing cart.")
        return
    init_user()

    cart_items = User.get_current_user().cart.items
    if not cart_items:
        print("Cart is empty")
    else:
        for cart_item in cart_items:
            print(cart_item)


@cli.command()
@click.option('--name', default='default')
def viewwishlist(name):
    """
    displays the contents of the wishlist.
    :param name: the name of the wishlist whose contents need to be displayed.
    :return: None
    """
    if not AuthAPI.is_logged_in():
        print("Please log in before viewing wishlist.")
        return
    init_user()

    wishlist_items = User.get_current_user().get_wishlist(name).items
    if not wishlist_items:
        print("Wishlist is empty")
    else:
        for wishlist_item in wishlist_items:
            print(wishlist_item)


@cli.command()
def placeorder():
    """
    places an order.
    :return: None
    """
    if not AuthAPI.is_logged_in():
        print("Please log in before placing order.")
        return
    init_user()

    cart = User.get_current_user().cart
    cart_items = cart.items
    if not cart_items:
        print("Cart is empty")
        return

    print("Order summary: ")
    for cart_item in cart_items:
        print(cart_item)
    print(f"Total: {cart.total_price}")

    payment_method = input("Select payment method:\n1) Cash On Delivery\t2) Cart\n3) Debit\t\t4) UPI\n: ")

    choice = input("Do you want to proceed? (y/n): ")
    if choice == 'n':
        return
    if User.get_current_user().place_order(payment_method):
        print("Order placed.")
    else:
        print("Error placing order.")


@cli.command()
@click.argument('name')
def createwishlist(name):
    """
    creates a wishlist.
    :param name: name of the wishlist to be created.
    :return: None
    """
    if not AuthAPI.is_logged_in():
        print("Please log in before creating wishlist.")
        return
    init_user()
    User.get_current_user().create_wishlist(name)
    User.get_current_user().save_wishlists()
    print("Wishlist created.")


def init():
    """
    Initializes variables.
    :return: None
    """
    global auth, search
    auth = AuthAPI()
    search = SearchAPI()


def init_user():
    """
    Initializes the user.
    :return: None
    """
    auth.signin_from_file()
    User.get_current_user().init()


def dispose():
    """
    performs cleanup.
    :return: None
    """
    global auth, search
    auth.dispose()
    search.dispose()


if __name__ == "__main__":
    init()
    cli()
