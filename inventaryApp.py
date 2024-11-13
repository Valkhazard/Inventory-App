#inventary system for a store that sell multiple products as electronic merchandise, clothes and food. 
# Each product has unique characteristics and the system needs to manage the inventary levels, prices and availability of each product. 
# Also, it needs to have a module to manage the customer orders.

from datetime import datetime

class Product():
    def __init__(self, name, price, stock):
        self.name = name
        self.price = float(price)
        self.stock = int(stock)
        
    def restock(self,quantity):
        if quantity > 0:
            self.stock += quantity
        else:
            print("The quantity must be positive")

    def sell(self,quantity):
        if quantity > 0:
            self.stock -= quantity
            print(f"The inventary for {self.name} has been changed and there is now {self.stock} products available. Price: {self.price:,.2f}")
        else:
            print("The quantity entered is not correct")

    def __str__(self):
        return f"The product {self.name} has a current stock of {self.stock}. Price: {self.price:,.2f}"
    
    def __repr__(self):
        return f"The product {self.name} has a current stock of {self.stock}. Price: {self.price:,.2f}"
    

class Electronics(Product):
    def __init__(self, name, price, stock, warranty_period):
        super().__init__(name, price, stock)
        self.warranty_period = warranty_period

    def __str__(self):
        return f"The product {self.name} has a current stock of {self.stock}. Warranty Period: {self.warranty_period}. Price: {self.price:,.2f}"

class Clothing(Product):
    def __init__(self, name, price, stock, size):
        super().__init__(name, price, stock)
        self.size = size
    
    def __str__(self):
        return f"The product {self.name} has a current stock of {self.stock}. Size: {self.size}. Price: {self.price:,.2f}"

class Food(Product):
    def __init__(self, name, price, stock, expiration_date):
        super().__init__(name, price, stock)
        self.name = name
        self.price = price
        self.stock = stock
        self.expiration_date = expiration_date
    
    def __str__(self):
        return f"The product {self.name} has a current stock of {self.stock}. Price: {self.price:,.2f}. Warranty: {self.expiration_date}"

class Inventory():
    def __init__(self):
        self.products_list = []
        self.sales_record = SalesRecord()

    def add_product(self):

        types = ["electronics","food","clothing"]
        product_type = input("What's the product type? Electronics/Food/Clothing: ").strip().lower()

        if product_type in types:

            product_toAdd = input("What's the product you want to add?: ")

            try:
                product_price = float(input("What's the price for this product?: "))
                product_stock = int(input("What's the stock for this product?: "))

            except ValueError:
                print("Only numbers can be entered")
                return

            if product_type == "electronics":
                warranty = input("Please enter the warranty for this product: ")
                product = Electronics(product_toAdd,product_price,product_stock,warranty)
            elif product_type == "food":
                exp_date = input("What's the expiration date: ")
                product = Food(product_toAdd,product_price, product_stock, exp_date)
            elif product_type == "clothing":
                size = input("What's the size for this product?: ")
                product = Clothing(product_toAdd,product_price, product_stock, size)
            else:
                print("Invalid product type")
                return

            self.products_list.append(product)

        else:
            lista_enumerada = enumerate(types,1)
            options = "\n".join(f"{posicion}. {producto}" for posicion, producto in lista_enumerada)
            print(f"Please choose between the following options:\n{options}")

    
    def show_inventory(self):
        if not self.products_list:
            print("Inventory is empty")
        else:
            print("Product list: ")
            for producto in self.products_list:
                print(producto)

    def __repr__(self):
        inventory_list = "\n".join(str(product) for product in self.products_list)
        return f"Current inventory: \n {inventory_list}"

    def sell_product(self):
        available_products = list(filter(lambda producto: producto.stock > 0, self.products_list))
        if not available_products:
            print("No available products")
            return

        print("Available products:")
        for index, producto in enumerate(available_products, 1):
            print(f"{index}. {producto}")

        while True:
            try:
                pick_product = int(input("Which product do you want to sell?\n: "))
                if 1 <= pick_product <= len(available_products):
                    selected_product = available_products[pick_product - 1]
                    print(f"You have selected to sell {selected_product.name}")
                    break
                else:
                    print("The option specified is not within the available options")
            except ValueError:
                print("Please enter a valid number.")

        while True:
            try:
                pick_stock = int(input(f"What's the amount you want to sell for {selected_product.name}?: "))
                if 0 <= pick_stock <= selected_product.stock:
                    confirm_order = input("Please confirm the order Y/N: ").strip().lower()
                    if confirm_order == "y":
                        user = input("Please enter your User Id: ")
                        selected_product.stock -= pick_stock
                        total_price = selected_product.price * pick_stock
                        print(f"Order confirmed! Product purchased: {selected_product.name} \nTotal Sale: {total_price:,.2f}")
                        self.sales_record.add_sale(selected_product.name, pick_stock, total_price, None, user)
                    else:
                        print("Order cancelled.")
                    break
                else:
                    print("The amount selected is not available.")
            except ValueError:
                print(f"Please enter a valid number. Stock available for {selected_product.name}: {selected_product.stock}")


    def check_Stock(self):
        lista_enumerada = enumerate(self.products_list,1)
        options_product = ". ".join(f"{numero}. {producto.name}" for numero,producto in lista_enumerada)
        
        try:
            product_stock = int(input(f"Please select the product you want to check stock to \n {options_product}\n: "))

            if 1 <= product_stock <= len(self.products_list):
                product_selected = self.products_list[product_stock -1]
                print(f"Product: {product_selected.name} \nStock: {product_selected.stock}")
            else:
                print("No stock available for this product")

        except ValueError:
            print("Please enter a valid number.")

class SalesRecord:
    def __init__(self):
 
        self.sales = []
        self.sales_by_product = {}

    def add_sale(self, product_name, quantity, amount_sold,sales_date=None, user_id=None):
        
        if sales_date is None:
            sales_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sale = {"Product": product_name, 
                "Quantity": quantity, 
                "Total Sold": amount_sold,
                "Date": sales_date,
                "Sold By": user_id}
        
        self.sales.append(sale)

        if product_name in self.sales_by_product:
            self.sales_by_product[product_name] += quantity
        else:
            self.sales_by_product[product_name] = quantity

    def get_sales_summary(self):

        for sale in self.sales:
            formatted_total = f"{sale['Total Sold']:,.2f}"
            print(f"Product: {sale['Product']}, Quantity: {sale['Quantity']}, Total Sold: {formatted_total}, Date: {sale['Date']}")

    def get_product_sales(self, product_name):
        return self.sales_by_product.get(product_name, 0)

    def get_total_sales_count(self):
        return len(self.sales)



# Crear el inventario
inventory = Inventory()

# Añadir productos
inventory.add_product()
#venta
inventory.sell_product()
# Mostrar el inventario actual
inventory.check_Stock()
inventory.sales_record.get_sales_summary()