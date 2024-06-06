# ProgFunA2_s4064801.py
# Author: Jayaweera Patabandige Binith Achintha Jayasinghe
# Student ID: 4064801
# git: https://github.com/jpbinith/COSC2531_Assignment_2
# Highest level: HD

# In HD level question 4 I assumed that customers file and product file are mandatory and order file is optional.
# In the order file assumend all the users and products are valid.
# In product file if the product is invalid an exceprion will ouccur and application will be exit.

import sys
from datetime import datetime

# Customer class
class Customer:
    def __init__(self, ID, name, reward):
        Validations.validate_customer_name(name)
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

    def write_info(self):
        pass

# Basic customer class
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

    # This method used to format class details before saving to the file
    def write_info(self):
        return f'{self.ID}, {self.name}, {self.__reward_rate}, {str(self.reward)}'

    @staticmethod
    def set_reward_rate(rate):
        BasicCustomer.reward_rate = rate

class VIPCustomer(Customer):
    __reward_rate = 1.0

    def __init__(self, ID, name, reward, discount_rate=None):
        super().__init__(ID, name, reward)
        self.__discount_rate = discount_rate if discount_rate is not None else 0.08
    
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
    
    # This method used to format class details before saving to the file
    def write_info(self):
        return f'{self.ID}, {self.name}, {self.__reward_rate}, {self.__discount_rate}, {str(self.reward)}'
    
    @staticmethod
    def set_reward_rate(rate):
        VIPCustomer.__reward_rate = rate
    
    def set_discount_rate(self, rate):
        self.__discount_rate = rate

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

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        self.__price = price

    @property
    def dr_prescription(self):
        return self.__dr_prescription

    @dr_prescription.setter
    def dr_prescription(self, dr_prescription):
        self.__dr_prescription = dr_prescription
    
    def display_info(self):
        print(f"ID: {self.ID}, Name: {self.name}, Price: {self.price} AUD, Doctor's Prescription: {self.dr_prescription}")

    # This method used to format class details before saving to the file
    def write_info(self):
        return f'{self.ID}, {self.name}, {self.price}, {self.dr_prescription}'

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

    # This method used to format class details before saving to the file
    def write_info(self):
        products = ''
        for product in self.__products:
            products += product.ID + ','
        return f'{self.ID}, {self.name}, {self.price}, {products[:-1]}'

class Order:

    def __init__(self, customer, product_list, quantity_list, total_cost=None, earned_rewards=None, date=None):
        self.__customer = customer
        self.__product_list = product_list
        self.__quantity_list = quantity_list
        self.__total_cost = total_cost
        self.__earned_rewards = earned_rewards
        self.__date = date

    @property
    def customer(self):
        return self.__customer
    
    # Calculate order cost
    def compute_cost(self):
        original_cost = sum( product.price * quantity for product, quantity in zip(self.__product_list, self.__quantity_list))
        reward = self.__customer.get_reward(original_cost)
        discount = self.__customer.get_discount(original_cost)
        final_cost = original_cost - discount
        reward_discount = 0
        if (final_cost >= 10 and self.__customer.reward >= 100):
            reward_discount = 10
            final_cost -= reward_discount
            self.__customer.reward = self.__customer.reward - 100
        self.__customer.update_reward(reward)

        # Get the current date and time
        now = datetime.now()

        self.__total_cost = final_cost
        self.__earned_rewards = reward
        self.__date = now.strftime("%d/%m/%Y %H:%M:%S")

        return original_cost, discount, final_cost, reward, reward_discount
    
    def display_info(self):
        products_str = ''
        for product, quantity in zip(self.__product_list, self.__quantity_list):
            products_str += f'{product} x {quantity}, ' 
        print(f"Customer: {self.__customer.name},   Products: { products_str }  Total cost: {self.__total_cost},   Earned rewards: {self.__earned_rewards},   Date: {self.__date}")

    # This method used to format class details before saving to the file
    def write_info(self):
        products_str = ''
        for product, quantity in zip(self.__product_list, self.__quantity_list):
            products_str += f'{product}, {str(quantity)}, ' 
        return f'{self.__customer.name}, {products_str}{self.__total_cost}, {self.__earned_rewards}, {self.__date}'
    
# Validation class (All the validation related functions done in this class)
class Validations:

    @staticmethod
    def validate_customer_name(name):
        if not name.isalpha():
            raise InvalidNameException("Customer name must contain only alphabet characters.")

    @staticmethod
    def validate_prescription_status(prescription):
        if prescription not in ['y', 'n']:
            raise InvalidPrescriptionException("Invalid input. Please enter 'y' or 'n'.")
        return prescription
    
    @staticmethod
    def validate_price(price):
        try:
            float(price)
            if float(price) < 0:
                raise InvalidPriceException(f"Invalid price input {price}. Enter a valid price.")
        except ValueException:
            raise InvalidPriceException(f"Invalid price input {price}. Enter a valid price.")
        
    @staticmethod
    def validate_product_input_format(product_info_list):
        if len(product_info_list) != 3:
            raise InvalidProductInfoFormetException("Invalid product input format. Enter the products again")
        
    @staticmethod
    def validate_reward_rate(reward_rate):
        try:
            float(reward_rate)
            if float(reward_rate) <= 0:
                raise InvalidRewardRateException(f"Invalid reward rate {reward_rate}. Enter a valid reward rate.")
        except ValueException:
            raise InvalidRewardRateException(f"Invalid reward rate {reward_rate}. Enter a valid reward rate.")
    
    @staticmethod
    def validate_VIP_customer(customer):
        if customer == None or customer.name[0] == 'B':
            raise InvalidVIPCustomerException("Invalid VIP customer id or name. Enter a valid customer naim or ID")
    
    @staticmethod
    def validate_discount_rate(discount_rate):
        try:
            float(discount_rate)
            if float(discount_rate) <= 0:
                raise InvalidRewardRateException(f"Invalid discount rate {discount_rate}. Enter a valid discount rate.")
        except ValueException:
            raise InvalidRewardRateException(f"Invalid discount rate {discount_rate}. Enter a valid discount rate.")

# Utill class (Utill functions added to this class)
class Utill:
    # This method used to pair neighbour elements in a array
    @staticmethod
    def pairwise(iterable):
        a = iter(iterable)
        return zip(a, a)

class Records:
    __next_customer_number = 1
    __next_product_number = 1
    
    def __init__(self):
        self.__customers = []
        self.__products = []
        self.__orders = []

    @staticmethod
    def get_next_customer_number():
        return Records.__next_customer_number
    
    @staticmethod
    def set_next_customer_number(customer_number):
        Records.__next_customer_number = customer_number

    @staticmethod
    def get_next_product_number():
        return Records.__next_product_number
    
    @staticmethod
    def set_next_product_number(product_number):
        Records.__next_product_number = product_number

    @property
    def customers(self):
        return self.__customers

    @property
    def products(self):
        return self.__products

    @property
    def orders(self):
        return self.__orders
    
    # This method used to read customers from the file
    def read_customers(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                data = [d.strip() for d in line.strip().split(',')]
                self.set_next_customer_number(int(''.join(filter(lambda i: i.isdigit(), data[0]))) + 1)
                if data[0][0] == 'B':
                    customer = BasicCustomer(data[0], data[1], int(data[3]))
                elif data[0][0] == 'V':
                    customer = VIPCustomer(data[0], data[1], int(data[4]), float(data[3]))
                self.__customers.append(customer)

    # This method used to read products from the file
    def read_products(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                data = [d.strip() for d in line.strip().split(',')]
                self.set_next_product_number(int(''.join(filter(lambda i: i.isdigit(), data[0]))) + 1)
                if data[0][0] == 'B':
                    product_ids = data[2:]
                    products = []
                    for pid in product_ids:
                        searched_product = self.find_product(pid)
                        if (searched_product != None):
                            products.append(searched_product)
                        else:
                            raise InvalidProductException(f"Product {pid} not found. Check the product file.")
                    product = Bundle(data[0], data[1], products)
                else:
                    product = Product(data[0], data[1], float(data[2]), data[3])
                self.__products.append(product)
    
    # This method used to read orders from the file
    def read_orders(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                data = [d.strip() for d in line.strip().split(',')]
                item_list = data[1:-3]
                product_list = []
                quantity_list = []
                for product, quantity in Utill.pairwise(item_list):
                    product_list.append(product)
                    quantity_list.append(quantity)
                customer = self.find_customer(data[0])
                order = Order(customer, product_list, quantity_list, data[-3], data[-2], data[-1])
                self.__orders.append(order)

    def find_customer(self, search_value):
        for customer in self.__customers:
            if customer.ID == search_value or customer.name == search_value:
                return customer
        return None

    def find_product(self, search_value):
        for product in self.__products:
            if product.ID == search_value or product.name == search_value:
                return product
    
    # Add or remove products
    def add_update_products(self):
        while True:
            try:
                product_info_input_list = input("Enter products (name price dr_prescription, comma-separated): ").split(',')
                for product_info_input in product_info_input_list:
                    product_info_list = [product_info.strip() for product_info in product_info_input.split()]
                    Validations.validate_product_input_format(product_info_list)
                    Validations.validate_price(product_info_list[1])
                    Validations.validate_prescription_status(product_info_list[2])
                    product = self.find_product(product_info_list[0])
                    # Checking existing product or not
                    if (product != None):
                        # is existing product update it
                        product.price = product_info_list[1]
                        product.dr_prescription = product_info_list[2]
                    else:
                        # if a new product create new one
                        product = Product("P" + str(self.get_next_product_number()), product_info_list[0], product_info_list[1], product_info_list[2])
                        self.__products.append(product)
                        self.set_next_product_number(self.get_next_customer_number() + 1)
                break
            except InvalidPrescriptionException as e:
                print(e)
            except InvalidProductInfoFormetException as e:
                print(e)
            except InvalidPriceException as e:
                print(e)

    # Write customer details to the file
    def write_customers(self, customers_filename):
        f = open(customers_filename, "w")
        customers_data = ''
        for customer_data in self.__customers:
            customers_data += customer_data.write_info() + '\n'
        f.write(customers_data)
        f.close()

    # Write product details to the file
    def write_products(self, products_filename):
        f = open(products_filename, "w")
        products_data = ''
        for product_data in self.__products:
            products_data += product_data.write_info() + '\n'
        f.write(products_data)
        f.close()

    # # Write order details to the file
    def write_orders(self, orders_filename):
        f = open(orders_filename, "w")
        orders_data = ''
        for order_data in self.__orders:
            orders_data += order_data.write_info() + '\n'
        f.write(orders_data)
        f.close()


# Custom Exception classes
class InvalidNameException(Exception):
    pass

class InvalidProductException(Exception):
    pass

class InvalidVIPCustomerException(Exception):
    pass

class InvalidQuantityException(Exception):
    pass

class InvalidPrescriptionException(Exception):
    pass

class InvalidQuantitiesException(Exception):
    pass

class NoPrescriptionException(Exception):
    pass

class InvalidProductInfoFormetException(Exception):
    pass

class InvalidPriceException(Exception):
    pass

class InvalidRewardRateException(Exception):
    pass

class Operations:
    
    def __init__(self, customers_filename, products_filename, orders_filename):
        self.records = Records()
        self.__customer_filename = customers_filename
        self.records.read_customers(customers_filename)
        self.__products_filename = products_filename
        self.records.read_products(products_filename)
        self.__orders_filename = orders_filename
        self.records.read_orders(orders_filename)

    # display menu
    def display_menu(self):
        while True:
            print("\nMenu:")
            print("1. Make a purchase")
            print("2. Display existing customers")
            print("3. Display existing products")
            print("4. Add/update products")
            print("5. Adjust the reward rate of all Basic customers")
            print("6. Adjust the discount rate of a VIP customer")
            print("7. Display all orders")
            print("8. Display a customer order history")
            print("9. Exit the program")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.make_purchase()
            elif choice == '2':
                self.list_customers()
            elif choice == '3':
                self.list_products()
            elif choice == '4':
                self.records.add_update_products()
            elif choice == '5':
                self.adjust_the_reward_rate()
            elif choice == '6':
                self.adjust_the_discount_rate()
            elif choice == '7':
                self.list_orders()
            elif choice == '8':
                self.list_customer_orders()
            elif choice == '9':
                self.update_files(self.__customer_filename, self.__products_filename, self.__orders_filename)
                sys.exit()
            else:
                print("Invalid choice. Please try again.")

    # make purchase
    def make_purchase(self):
        try:
            # read customer name
            customer_name = self.read_customer_name()
            # read product list
            product_List = self.read_product_list()
            # read quantity list
            quantity_list = self.read_quantity_list(len(product_List))
            # find existing customer or not
            customer = self.records.find_customer(customer_name)
            # if not an existing customer create a new customer
            if customer is None:
                print(f"New customer: {customer_name}. Registering as Basic Customer.")
                customer = BasicCustomer("B" + str(self.records.get_next_customer_number()), customer_name, 0)
                self.records.set_next_customer_number(self.records.get_next_customer_number() + 1)
                self.records.customers.append(customer)
            # else:
            #     print(f"Existing customer: {customer_name}. Type: {'VIP' if isinstance(customer, VIPCustomer) else 'Basic'}")

            # create order instance
            order = Order(customer, product_List, quantity_list)
            # calculate order cost
            original_cost, discount, final_cost, reward, reward_discount = order.compute_cost()

            # Print receipt
            if isinstance(customer, VIPCustomer):
                print("\n------------------------------ Receipt ------------------------------")
                print(f"Name: {customer_name}")
                for product, quantity in zip(product_List, quantity_list):
                    print(f"Product: {product.name}")
                    print(f"Unit Price: {product.price} (AUD)")
                    print(f"Quantity: {quantity}")
                print(f"Original cost: {original_cost} (AUD)")
                print(f"Discount: {discount} (AUD)")
                print("---------------------------------------------------------------------")
                print(f"Total cost: {final_cost + reward_discount} (AUD)")
                print(f"Earned reward: {reward}")
                if (reward_discount > 0):
                    print(f"Reward discount: {reward_discount}")
                    print(f"Total after reward discount: {final_cost}")
            else:
                print("\n------------------------------ Receipt ------------------------------")
                print(f"Name: {customer_name}")
                for product, quantity in zip(product_List, quantity_list):
                    print(f"Product: {product.name}")
                    print(f"Unit Price: {product.price} (AUD)")
                    print(f"Quantity: {quantity}")
                print("---------------------------------------------------------------------")
                print(f"Total cost: {final_cost + reward_discount} (AUD)")
                print(f"Earned reward: {reward}")
                if (reward_discount > 0):
                    print(f"Reward discount: {reward_discount}")
                    print(f"Total after reward discount: {final_cost}")
    
        except InvalidNameException as e:
            print(e)
        except InvalidProductException as e:
            print(e)
        except InvalidQuantityException as e:
            print(e)
        except InvalidPrescriptionException as e:
            print(e)
        except InvalidQuantitiesException as e:
            print(e)
        except NoPrescriptionException as e:
            print(e)

    # Print all customers
    def list_customers(self):
        for customer in self.records.customers:
            customer.display_info()

    # Print all products
    def list_products(self):
        for product in self.records.products:
            product.display_info()

    # read quantity list and validate
    def read_quantity_list(self, number_of_products):
        while True:
            final_quantity_list = []
            quantity_list = input("Enter quantity: ")
            quantity_list = [quantity.strip() for quantity in quantity_list.split(',')]

            try:
                if (number_of_products != len(quantity_list)):
                    raise InvalidQuantitiesException("\nException: Number of products and quantities should be the same. Re Enter the quantities.\n\n")
            
                for quantity in quantity_list:
                    if not quantity.isdigit() or int(quantity) <= 0:
                        raise InvalidQuantityException("Quantity must be a positive integer.")
                    final_quantity_list.append(int(quantity))
            except InvalidQuantityException as e:
                print(e)
            except InvalidQuantitiesException as e:
                print(e)
            return final_quantity_list
        
    # read customer name and validate
    def read_customer_name(self):
        while True:
            try:
                customer_name = input("Enter customer name: ")
                Validations.validate_customer_name(customer_name)
                return customer_name
            except InvalidNameException as e:
                print(e)

    # read product list and validate
    def read_product_list(self):
        while True:
            try:
                product_name_list = input("Enter the list of Product's name seperated by commas: ")
                product_name_list = [product_name.strip() for product_name in product_name_list.split(',')]

                product_List = []
                for product_name in product_name_list:
                    product = self.records.find_product(product_name)
                    if (product == None):
                        raise InvalidProductException("Invalid product. Enter the products again")
                    if product.dr_prescription == 'y':
                        while True:
                            try:
                                prescription = input(f"Do you have a doctor's prescription for {product_name}? (y/n): ").lower()
                                Validations.validate_prescription_status(prescription)
                                if prescription == 'n':
                                    raise NoPrescriptionException(f"You cannot purchase this product {product_name} without a doctor's prescription.")
                                else:
                                    product_List.append(product)
                                    break
                            except InvalidPrescriptionException as e:
                                print(e)
                            except NoPrescriptionException as e:
                                print(e)
                                break
                    else:
                        product_List.append(product)

                return product_List
            except InvalidProductException as e:
                print(e)

    # set reward rate for all basic customers
    def adjust_the_reward_rate(self):
        while True:
            try:
                reward_rate = input("Enter reward rate: ")
                Validations.validate_reward_rate(reward_rate)
                BasicCustomer.set_reward_rate(reward_rate)
                break
            except InvalidRewardRateException as e:
                print(e)

    # set discount rate of a specific VIP customer
    def adjust_the_discount_rate(self):
        while True:
            try:
                customer = input("Enter VIP customer id or name: ")
                customer_obj = self.records.find_customer(customer)
                Validations.validate_VIP_customer(customer_obj)
                break
            except InvalidVIPCustomerException as e:
                print(e)
        while True:
            try:
                discount_rate = input("Enter discount rate: ")
                Validations.validate_discount_rate(discount_rate)
                customer_obj.set_discount_rate(discount_rate)
                break
            except InvalidRewardRateException as e:
                print(e)

    # print all orders
    def list_orders(self):
        for order in self.records.orders:
            order.display_info()

    # print order history of a customer
    def list_customer_orders(self):
        while True:
            try:
                customer_name = input("Enter customer name: ")
                customer = self.records.find_customer(customer_name)
                for order in self.records.orders:
                    if (order.customer.name == customer.name):
                        order.display_info()
                break
            except Exception as e:
                print(e)

    def update_files(self, customers_filename, products_filename, orders_filename):
        self.records.write_customers(customers_filename)
        self.records.write_products(products_filename)
        self.records.write_orders(orders_filename)

# read file names
customers_filename = input("Enter customer filename: ")
products_filename = input("Enter products filename: ")
# check for optional order filename and read if needed
is_order_filename = ''
while True:
    is_order_filename = input("Do you want to enter orders filename (y, n):")
    if (is_order_filename .lower() in ['y', 'n']):
        break
    else:
        print('Invalid input. Enter a valid input. (y-Yes, n-No)')
if (is_order_filename.lower() == 'y'):
    orders_filename = input("Enter orders filename: ")
else:
    orders_filename = 'orders.txt'

try:
    # operations = Operations('customers.txt', 'products.txt', 'orders.txt')
    operations = Operations(customers_filename, products_filename, orders_filename)
    operations.display_menu()
except FileNotFoundError as e:
    print(e)
    sys.exit()