# ONLINE SHOPPING SYSTEM
A mock, command line based, online shopping system written in python for the SDF lab in semester 4.

prerequisites:
- python 3 +
- pip
- virtualenv (optional but recommended)

To run the program:
1) create env<br>
```
$ make venv
```
2) activate env<br>
```
$ source venv/bin/activate
 ```
3) from `src` directory, run the `main.py` file with arguments.

```
$ python main.py --help
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  addtocart       adds an item to the cart.
  addtowishlist   adds an item to the wishlist.
  createwishlist  creates a wishlist.
  placeorder      places an order.
  search          searches for a product given a search string.
  signin          signs the user in.
  signout         signs the user out.
  signup          registers a new user.
  viewcart        displays the contents of the cart.
  viewwishlist    displays the contents of the wishlist.
```