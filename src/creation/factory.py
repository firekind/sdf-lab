from entities.item import Product


class ProductFactory:
    @staticmethod
    def create_products(products_meta):
        """
        creates objects of `Product` class from the products meta
        :param products_meta: a list containing information about the products
        :return: list of `Product` objects
        """
        products = []
        for product in products_meta:
            products.append(ProductFactory.create_product(product))

        if not products:
            return None
        return products

    @staticmethod
    def create_product(product_meta):
        """
        creates a `Product` from the information given. information consists of a tuple with comma separated
        values.
        :param product_meta: the information about the product.
        :return: object of `Product` class
        """
        return Product(
                id_=product_meta[0],
                name=product_meta[1],
                price=product_meta[2],
                manu_name=product_meta[3]
        )
