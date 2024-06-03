# ProgFunA2_s4064801.py
# Author: Jayaweera Patabandige Binith Achintha Jayasinghe
# Student ID: 4064801

class Customer:
    def __init__(self, ID, name, reward):
        if not name.isalpha():
            raise InvalidNameError("Customer name must contain only alphabet characters.")
        self.__ID = ID
        self.__name = name
        self.__reward = reward

    @property
    def ID(self):
        return self.__ID

    @property
    def name(self):
        return self.__name

    @property
    def reward(self):
        return self.__reward

    @reward.setter
    def reward(self, reward_value):
        self.__reward = reward_value
    
    def get_reward(self):
        pass
    
    def get_discount(self, total_cost):
        return 0 * total_cost
    
    def update_reward(self):
        pass
    
    def display_info(self):
        pass

class BasicCustomer(Customer):
    __reward_rate = 1.0

    def __init__(self, ID, name, reward):
        super().__init__(ID, name, reward)
    
    def get_reward(self, total_cost):
        # Round points to the nearest integer
        return int(total_cost * self.__reward_rate + 0.5)
    
    def update_reward(self, reward_value):
        self.reward = self.reward + reward_value
    
    def display_info(self):
        print(f"ID: {self.ID}, Name: {self.name}, Reward: {self.reward}, Reward Rate: {self.__reward_rate}")

    @staticmethod
    def set_reward_rate(rate):
        BasicCustomer.reward_rate = rate

class VIPCustomer(Customer):
    __reward_rate = 1.0
    __default_discount_rate = 0.08

    def __init__(self, ID, name, reward, discount_rate=None):
        super().__init__(ID, name, reward)
        self.__discount_rate = discount_rate if discount_rate is not None else VIPCustomer.__default_discount_rate
    
    def get_discount(self, total_cost):
        return total_cost * self.__discount_rate
    
    def get_reward(self, total_cost):
        total_cost_after_discount = total_cost - self.get_discount(total_cost)
        # Round points to the nearest integer
        return int(total_cost_after_discount * self.__reward_rate + 0.5)
    
    def update_reward(self, reward_value):
        self.reward = self.reward + reward_value
    
    def display_info(self):
        print(f"ID: {self.ID}, Name: {self.name}, Reward: {self.reward}, Reward Rate: {self.__reward_rate}, Discount Rate: {self.__discount_rate}")
    
    @staticmethod
    def set_reward_rate(rate):
        VIPCustomer.__reward_rate = rate
    
    def set_discount_rate(self, rate):
        self.discount_rate = rate

class Product:
    def __init__(self, ID, name, price, dr_prescription):
        self.__ID = ID
        self.__name = name
        self.__price = price
        self.__dr_prescription = dr_prescription

    @property
    def ID(self):
        return self.__ID

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def dr_prescription(self):
        return self.__dr_prescription

    @property
    def dr_prescription(self):
        return self.__dr_prescription

    @property
    def name(self):
        return self.__name
    
    def display_info(self):
        print(f"ID: {self.ID}, Name: {self.name}, Price: {self.price} AUD, Doctor's Prescription: {self.dr_prescription}")

class Bundle(Product):
    def __init__(self, ID, name, products):
        super().__init__(ID, name, 0, 'y' if any(p.dr_prescription == 'y' for p in products) else 'n')
        self.__products = products
        self.__price = round(0.8 * sum(p.price for p in products), 2)

    @property
    def price(self):
        return self.__price
    
    def display_info(self):
        product_names = ", ".join(p.name for p in self.__products)
        print(f"ID: {self.ID}, Name: {self.name}, Price: {self.__price} AUD, Doctor's Prescription: {self.dr_prescription}, Products: {product_names}")

class Order:
    def __init__(self, customer, product, quantity):
        if not quantity.isdigit() or int(quantity) <= 0:
            raise InvalidQuantityError("Quantity must be a positive integer.")
        self.__customer = customer
        self.__product = product
        self.__quantity = int(quantity)
    
    def compute_cost(self):
        original_cost = self.__product.price * self.__quantity
        discount = self.__customer.get_discount(original_cost)
        final_cost = original_cost - discount
        reward = self.__customer.get_reward(original_cost)
        return original_cost, discount, final_cost, reward

class Records:
    def __init__(self):
        self.__customers = []
        self.__products = []

    @property
    def customers(self):
        return self.__customers
    def read_customers(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                data = [d.strip() for d in line.strip().split(',')]
                if data[0][0] == 'B':
                    customer = BasicCustomer(data[0], data[1], int(data[2]))
                elif data[0][0] == 'V':
                    customer = VIPCustomer(data[0], data[1], int(data[4]), float(data[3]))
                self.__customers.append(customer)

    def read_products(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                data = [d.strip() for d in line.strip().split(',')]
                if data[0][0] == 'B':
                    product_ids = data[2:]
                    products = []
                    for pid in product_ids:
                        searched_product = self.find_product(pid)
                        if (searched_product != None):
                            products.append(searched_product)
                    product = Bundle(data[0], data[1], products)
                else:
                    product = Product(data[0], data[1], float(data[2]), data[3])
                self.__products.append(product)

    def find_customer(self, search_value):
        for customer in self.__customers:
            if customer.ID == search_value or customer.name == search_value:
                return customer
        return None

    def find_product(self, search_value):
        for product in self.__products:
            if product.ID == search_value or product.name == search_value:
                return product
        
        raise InvalidProductError(f"Product {search_value} not found.")

    def list_customers(self):
        for customer in self.__customers:
            customer.display_info()

    def list_products(self):
        for product in self.__products:
            product.display_info()

class InvalidNameError(Exception):
    pass

class InvalidProductError(Exception):
    pass

class InvalidQuantityError(Exception):
    pass

class InvalidPrescriptionError(Exception):
    pass

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
        try:
            customer_name = input("Enter customer name: ")
            
            product_name = input("Enter product name: ")
            product = self.records.find_product(product_name)
            
            quantity = input("Enter quantity: ")

            if product.dr_prescription == 'y':
                prescription = input("Do you have a doctor's prescription? (y/n): ").lower()
                if prescription not in ['y', 'n']:
                    raise InvalidPrescriptionError("Invalid input. Please enter 'y' or 'n'.")
                if prescription == 'n':
                    print("You cannot purchase this product without a doctor's prescription.")
                    return

            customer = self.records.find_customer(customer_name)
            if customer is None:
                print(f"New customer: {customer_name}. Registering as Basic Customer.")
                customer = BasicCustomer("B" + str(len(self.records.customers) + 1), customer_name, 0)
                self.records.customers.append(customer)
            else:
                print(f"Existing customer: {customer_name}. Type: {'VIP' if isinstance(customer, VIPCustomer) else 'Basic'}")


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
    
        except InvalidNameError as e:
            print(e)
        except InvalidProductError as e:
            print(e)
        except InvalidQuantityError as e:
            print(e)
        except InvalidPrescriptionError as e:
            print(e)

operations = Operations()
operations.display_menu()