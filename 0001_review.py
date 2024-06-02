class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def sell_product(self, amount):
        self.quantity -= amount

    def __str__(self):
        return "Product: Name: {self.name}, Price: {self.price}, Quantity: {self.quantity}"


class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def __str__(self):
        return self.products


def main():
    inventory = Inventory()

    inventory.add_product(Product("Apple", 1.0, 10))
    inventory.add_product(Product("Banana", 0.5, 15))
    inventory.add_product(Product("Orange", 1.5, 8))

    print("Initial Inventory:")
    print(inventory)
    inventory.products[0].sell_product(3)
    inventory.products[1].sell_product(20)

    print("\nUpdated Inventory:")
    print(inventory)


if __name__ == "__main__":
    main()
