from copy import copy
from typing import Union, TypeVar

T = TypeVar("T", bound=object)


def class_wrapper(instance: T):
    class_name = instance.__class__.__name__
    s = '— ' * len(class_name) * 2
    return f"\n{s} {class_name} {s}"


class Store:
    def __init__(self):
        self._products = {}

    @property
    def products(self) -> str:
        """ Returns the stored products """
        items = [str(item) for item in self._products.values()]
        return class_wrapper(self) + "\n".join(items)

    def product(self, name: str) -> Union["Product", None]:
        """ Returns the product with the given name if it exists """
        return next((product for product in self._products.values() if product.name == name), None)

    def rename_product(self, old_name: str, new_name: str) -> None:
        """ Renames the product if it exists """
        product = self.product(old_name)
        if not product:
            raise ValueError(f'Product "{old_name}" does not exist')
        product.update_name(new_name)

    def add_product(self, name: str, price: int | float, quantity: int) -> None:
        """ Adds new product to the store or updates the price and quantity of the product """
        product = self.product(name)

        if product:
            product.update(price, quantity)
        else:
            self._products.update({len(self._products) + 1: Product(name, price, quantity)})

    def sell_product(self, name: str, quantity: int) -> "Product":
        """ Sells the product if it exists """
        product = self.product(name)
        sell_product = copy(product)

        if not product:
            raise ValueError(f'Product "{name}" not found!')

        if product.quantity < quantity:
            raise ValueError(f'Quantity of {product.name} is {product.quantity}. You add to cart {quantity}')

        product.update_quantity(-quantity)
        return sell_product


class Product:

    def __init__(self, name: str, price: int | float, quantity: int):
        self._quantity = 0
        self.name = name
        self.price = price
        self.quantity = quantity

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value == "":
            raise ValueError(f"Name cannot be empty string!")
        self._name = value

    def update_name(self, name: str):
        self.name = name

    @property
    def price(self) -> int | float:
        return self._price

    @price.setter
    def price(self, value: int | float):
        if value < 0:
            raise ValueError("Price cannot be negative!")
        elif value == 0:
            raise ValueError("Price cannot be zero!")
        self._price = value

    def update_price(self, value: int | float):
        self.price = value

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        if value < 0:
            raise ValueError("Quantity of product cannot be negative!")
        self._quantity = value

    def update_quantity(self, value: int):
        self.quantity += value

    def update(self, price: int | float, quantity: int):
        self.update_price(price)
        self.update_quantity(quantity)

    def __repr__(self):
        return self.name

    def __str__(self):
        return (
            f"\nProduct:"
            f"\n  — Name: {self.name}"
            f"\n  — Price: ${self.price:,}"
            f"\n  — Quantity: {self.quantity:,}"
        )


class Cart:
    def __init__(self, store: Store):
        super().__init__()
        self._store = store
        self._cart = []

    def put(self, name: str, quantity: int):
        """ Add a product to the cart """
        product = self._store.sell_product(name, quantity)
        product.quantity = quantity
        self._cart.append(product)

    def remove(self, name: str, quantity: int):
        """ Remove a product from the cart """
        cart_product = next((product for product in self._cart if product.name == name), None)
        if not cart_product:
            raise ValueError(f'You have not product "{name}" in cart!')

        if quantity > cart_product.quantity:
            raise ValueError(f'You have {cart_product.quantity}x of "{name}" in yor cart. '
                             f'You try to remove {quantity}x!')

        elif quantity == cart_product.quantity:
            self._cart.remove(cart_product)
        else:
            cart_product.quantity -= quantity

        product = self._store.product(name)
        product.quantity += quantity

    @property
    def show(self) -> str:
        """ Returns the saved items in the cart """
        items = [str(item) for item in self._cart]
        return class_wrapper(self) + "\n".join(items)


def main():
    store = Store()
    store.add_product("Apple", 1.0, 10)
    store.add_product("Apple", 5, 5)
    store.add_product("Banana", 0.5, 15)
    store.add_product("Orange", 1.5, 8)

    print(store.products)

    # store.rename_product("Apple", "Golden Apple")
    # print(store.product("Apple"))

    cart = Cart(store)
    cart.put("Apple", 14)
    cart.put("Banana", 15)
    print(cart.show)

    cart.remove("Apple", 14)

    print(store.products)
    print(cart.show)


if __name__ == "__main__":
    main()
