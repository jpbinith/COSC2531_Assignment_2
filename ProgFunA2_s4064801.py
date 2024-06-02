# ProgFunA2_s4064801.py
# Author: Jayaweera Patabandige Binith Achintha Jayasinghe
# Student ID: 4064801

class Customer:
    def __init__(self, ID, name, reward):
        self.ID = ID
        self.name = name
        self.reward = reward
    
    def get_reward(self):
        pass
    
    def get_discount(self, total_cost):
        return 0 * total_cost
    
    def update_reward(self):
        pass
    
    def display_info(self):
        pass

class BasicCustomer(Customer):
    reward_rate = 1.0

    def __init__(self, ID, name, reward):
        super().__init__(ID, name, reward)
    
    def get_reward(self, total_cost):
        return round(total_cost * self.reward_rate)
    
    def update_reward(self, reward_value):
        self.reward += reward_value
    
    def display_info(self):
        print(f"ID: {self.ID}, Name: {self.name}, Reward: {self.reward}, Reward Rate: {self.reward_rate}")

    @staticmethod
    def set_reward_rate(rate):
        BasicCustomer.reward_rate = rate

class VIPCustomer(Customer):
    reward_rate = 1.0
    default_discount_rate = 0.08

    def __init__(self, ID, name, reward, discount_rate=None):
        super().__init__(ID, name, reward)
        self.discount_rate = discount_rate if discount_rate is not None else VIPCustomer.default_discount_rate
    
    def get_discount(self, total_cost):
        return total_cost * self.discount_rate
    
    def get_reward(self, total_cost):
        total_cost_after_discount = total_cost - self.get_discount(total_cost)
        return round(total_cost_after_discount * self.reward_rate)
    
    def update_reward(self, reward_value):
        self.reward += reward_value
    
    def display_info(self):
        print(f"ID: {self.ID}, Name: {self.name}, Reward: {self.reward}, Reward Rate: {self.reward_rate}, Discount Rate: {self.discount_rate}")
    
    @staticmethod
    def set_reward_rate(rate):
        VIPCustomer.reward_rate = rate
    
    def set_discount_rate(self, rate):
        self.discount_rate = rate

class Product:
    def __init__(self, ID, name, price):
        self.ID = ID
        self.name = name
        self.price = price
    
    def display_info(self):
        print(f"ID: {self.ID}, Name: {self.name}, Price: {self.price} AUD")

class Order:
    def __init__(self, customer, product, quantity):
        self.customer = customer
        self.product = product
        self.quantity = quantity
    
    def compute_cost(self):
        original_cost = self.product.price * self.quantity
        discount = self.customer.get_discount(original_cost)
        final_cost = original_cost - discount
        reward = self.customer.get_reward(original_cost)
        return original_cost, discount, final_cost, reward

class Records:
    def __init__(self):
        self.customers = []
        self.products = []

    def read_customers(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                if data[0][0] == 'B':
                    customer = BasicCustomer(data[0].strip(), data[1].strip(), int(data[2].strip()))
                elif data[0][0] == 'V':
                    customer = VIPCustomer(data[0].strip(), data[1].strip(), int(data[4].strip()), float(data[3].strip()))
                self.customers.append(customer)

    def read_products(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                product = Product(data[0].strip(), data[1].strip(), float(data[2].strip()))
                self.products.append(product)

    def find_customer(self, search_value):
        for customer in self.customers:
            if customer.ID == search_value or customer.name == search_value:
                return customer
        return None

    def find_product(self, search_value):
        for product in self.products:
            if product.ID == search_value or product.name == search_value:
                return product
        return None

    def list_customers(self):
        for customer in self.customers:
            customer.display_info()

    def list_products(self):
        for product in self.products:
            product.display_info()

class Operations:
    def __init__(self):
        self.records = Records()
        self.records.read_customers('customers.txt')
        self.records.read_products('products.txt')

    def display_menu(self):
        while True:
            print("\nMenu:")
            print("1. Make a purchase")
            print("2. Display existing customers")
            print("3. Display existing products")
            print("4. Exit the program")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.make_purchase()
            elif choice == '2':
                self.records.list_customers()
            elif choice == '3':
                self.records.list_products()
            elif choice == '4':
                print("Exiting the program...")
                break
            else:
                print("Invalid choice. Please try again.")

    def make_purchase(self):
        customer_name = input("Enter customer name: ")
        product_name = input("Enter product name: ")
        quantity = int(input("Enter quantity: "))

        customer = self.records.find_customer(customer_name)
        if customer is None:
            print(f"New customer: {customer_name}. Registering as Basic Customer.")
            customer = BasicCustomer("B" + str(len(self.records.customers) + 1), customer_name, 0)
            self.records.customers.append(customer)
        else:
            print(f"Existing customer: {customer_name}. Type: {'VIP' if isinstance(customer, VIPCustomer) else 'Basic'}")

        product = self.records.find_product(product_name)
        if product is None:
            print(f"Product {product_name} not found.")
            return

        order = Order(customer, product, quantity)
        original_cost, discount, final_cost, reward = order.compute_cost()
        customer.update_reward(reward)

        if isinstance(customer, VIPCustomer):
            print("\n------------------------------ Receipt ------------------------------")
            print(f"Name: {customer_name}")
            print(f"Product: {product_name}")
            print(f"Unit Price: {product.price} (AUD)")
            print(f"Quantity: {quantity}")
            print(f"Original cost: {original_cost} (AUD)")
            print(f"Discount: {discount} (AUD)")
            print("---------------------------------------------------------------------")
            print(f"Total cost: {final_cost} (AUD)")
            print(f"Earned reward: {reward}")
        else:
            print("\n------------------------------ Receipt ------------------------------")
            print(f"Name: {customer_name}")
            print(f"Product: {product_name}")
            print(f"Unit Price: {product.price} (AUD)")
            print(f"Quantity: {quantity}")
            print("---------------------------------------------------------------------")
            print(f"Total cost: {final_cost} (AUD)")
            print(f"Earned reward: {reward}")

operations = Operations()
operations.display_menu()