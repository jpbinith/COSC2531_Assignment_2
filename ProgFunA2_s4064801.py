# ProgFunA2_s4064801.py
# Author: Jayaweera Patabandige Binith Achintha Jayasinghe
# Student ID: 4064801

import sys
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
    __discount_rate = 0.08

    def __init__(self, ID, name, reward, discount_rate=None):
        super().__init__(ID, name, reward)
        VIPCustomer.__discount_rate = discount_rate if discount_rate is not None else VIPCustomer.__discount_rate
    
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
    
    @staticmethod
    def set_discount_rate(rate):
        VIPCustomer.__discount_rate = rate

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
    def __init__(self, customer, product_list, quantity_list):
        self.__customer = customer
        self.__product_list = product_list
        self.__quantity_list = quantity_list
    
    def compute_cost(self):
        original_cost = sum( product.price * quantity for product, quantity in zip(self.__product_list, self.__quantity_list))
        reward = self.__customer.get_reward(original_cost)
        discount = self.__customer.get_discount(original_cost)
        final_cost = original_cost - discount
        if (final_cost >= 10 and self.__customer.reward >= 100):
            final_cost -= 10
            self.__customer.reward = self.__customer.reward - 100
        self.__customer.update_reward(reward)

        return original_cost, discount, final_cost, reward
    
class Validations:

    @staticmethod
    def validate_customer_name(name):
        if not name.isalpha():
            raise InvalidNameError("Customer name must contain only alphabet characters.")

    @staticmethod
    def validate_prescription_status(prescription):
        if prescription not in ['y', 'n']:
            raise InvalidPrescriptionError("Invalid input. Please enter 'y' or 'n'.")
        return prescription
    
    @staticmethod
    def validate_price(price):
        try:
            float(price)
            if float(price) < 0:
                raise InvalidPriceError(f"Invalid price input {price}. Enter a valid price.")
        except ValueError:
            raise InvalidPriceError(f"Invalid price input {price}. Enter a valid price.")
        
    @staticmethod
    def validate_product_input_format(product_info_list):
        if len(product_info_list) != 3:
            raise InvalidProductInfoFormetError("Invalid product input format. Enter the products again")
        
    @staticmethod
    def validate_reward_rate(reward_rate):
        try:
            float(reward_rate)
            if float(reward_rate) <= 0:
                raise InvalidRewardRateError(f"Invalid reward rate {reward_rate}. Enter a valid reward rate.")
        except ValueError:
            raise InvalidRewardRateError(f"Invalid reward rate {reward_rate}. Enter a valid reward rate.")
    
    @staticmethod
    def validate_VIP_customer(customer, find_customer):
        customer_obj = find_customer(customer)
        if customer_obj == None or customer_obj.name[0] == 'B':
            raise InvalidVIPCustomerError("Invalid VIP customer id or name. Enter a valid customer naim or ID")
    
    @staticmethod
    def validate_discount_rate(discount_rate):
        try:
            float(discount_rate)
            if float(discount_rate) <= 0:
                raise InvalidRewardRateError(f"Invalid discount rate {discount_rate}. Enter a valid discount rate.")
        except ValueError:
            raise InvalidRewardRateError(f"Invalid discount rate {discount_rate}. Enter a valid discount rate.")


class Records:
    __next_customer_number = 1
    __next_product_number = 1
    
    def __init__(self):
        self.__customers = []
        self.__products = []

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
    
    def read_customers(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                data = [d.strip() for d in line.strip().split(',')]
                self.set_next_customer_number(int(''.join(filter(lambda i: i.isdigit(), data[0]))) + 1)
                if data[0][0] == 'B':
                    customer = BasicCustomer(data[0], data[1], int(data[2]))
                elif data[0][0] == 'V':
                    customer = VIPCustomer(data[0], data[1], int(data[4]), float(data[3]))
                self.__customers.append(customer)

    def read_products(self, filename):
        try:
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
                                raise InvalidProductError(f"Product {pid} not found. Check the product file.")
                        product = Bundle(data[0], data[1], products)
                    else:
                        product = Product(data[0], data[1], float(data[2]), data[3])
                    self.__products.append(product)
        except InvalidProductError as e:
            print(e)
            sys.exit();

    def find_customer(self, search_value):
        for customer in self.__customers:
            if customer.ID == search_value or customer.name == search_value:
                return customer
        return None

    def find_product(self, search_value):
        for product in self.__products:
            if product.ID == search_value or product.name == search_value:
                return product
    
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
                    if (product != None):
                        product.price = product_info_list[1]
                        product.dr_prescription = product_info_list[2]
                    else:
                        product = Product("P" + str(self.get_next_product_number()), product_info_list[0], product_info_list[1], product_info_list[2])
                        self.__products.append(product)
                        self.set_next_product_number(self.get_next_customer_number() + 1)
                break
            except InvalidPrescriptionError as e:
                print(e)
            except InvalidProductInfoFormetError as e:
                print(e)
            except InvalidPriceError as e:
                print(e)

class InvalidNameError(Exception):
    pass

class InvalidProductError(Exception):
    pass

class InvalidVIPCustomerError(Exception):
    pass

class InvalidQuantityError(Exception):
    pass

class InvalidPrescriptionError(Exception):
    pass

class InvalidQuantitiesError(Exception):
    pass

class NoPrescriptionError(Exception):
    pass

class InvalidProductInfoFormetError(Exception):
    pass

class InvalidPriceError(Exception):
    pass

class InvalidRewardRateError(Exception):
    pass

class Operations:
    validations = Validations()
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
            print("4. Add/update products")
            print("5. Adjust the reward rate of all Basic customers")
            print("6. Adjust the discount rate of a VIP customer")
            print("7. Display customer order history")
            print("8. Exit the program")
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
                print("Exiting the program...")
                break
            else:
                print("Invalid choice. Please try again.")

    def make_purchase(self):
        try:
            customer_name = input("Enter customer name: ")
            
            product_List = self.read_product_list()
            
            quantity_list = self.read_quantity_list(len(product_List))

            customer = self.records.find_customer(customer_name)
            if customer is None:
                print(f"New customer: {customer_name}. Registering as Basic Customer.")
                customer = BasicCustomer("B" + str(self.records.get_next_customer_number()), customer_name, 0)
                self.records.set_next_customer_number(self.records.get_next_customer_number() + 1)
                self.records.customers.append(customer)
            else:
                print(f"Existing customer: {customer_name}. Type: {'VIP' if isinstance(customer, VIPCustomer) else 'Basic'}")


            order = Order(customer, product_List, quantity_list)
            original_cost, discount, final_cost, reward = order.compute_cost()

            if isinstance(customer, VIPCustomer):
                print("\n------------------------------ Receipt ------------------------------")
                print(f"Name: {customer_name}")
                print(f"Product: {product.name}")
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
                for product, quantity in zip(product_List, quantity_list):
                    print(f"Product: {product.name}")
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
        except InvalidQuantitiesError as e:
            print(e)
        except NoPrescriptionError as e:
            print(e)

    def list_customers(self):
        for customer in self.records.customers:
            customer.display_info()

    def list_products(self):
        for product in self.records.products:
            product.display_info()

    def read_quantity_list(self, number_of_products):
        while True:
            final_quantity_list = []
            quantity_list = input("Enter quantity: ")
            quantity_list = [quantity.strip() for quantity in quantity_list.split(',')]

            try:
                if (number_of_products != len(quantity_list)):
                    raise InvalidQuantitiesError("\nError: Number of products and quantities should be the same. Re Enter the quantities.\n\n")
            
                for quantity in quantity_list:
                    if not quantity.isdigit() or int(quantity) <= 0:
                        raise InvalidQuantityError("Quantity must be a positive integer.")
                    final_quantity_list.append(int(quantity))
            except InvalidQuantityError as e:
                print(e)
                continue
            except InvalidQuantitiesError as e:
                print(e)
                continue
            return final_quantity_list

    def read_product_list(self):
        while True:
            try:
                product_name_list = input("Enter the list of Product's name seperated by commas: ")
                product_name_list = [product_name.strip() for product_name in product_name_list.split(',')]

                product_List = []
                for product_name in product_name_list:
                    product = self.records.find_product(product_name)
                    if (product == None):
                        raise InvalidProductError("Invalid product. Enter the products again")
                    if product.dr_prescription == 'y':
                        while True:
                            try:
                                prescription = input(f"Do you have a doctor's prescription for {product_name}? (y/n): ").lower()
                                Validations.validate_prescription_status(prescription)
                                if prescription == 'n':
                                    print(f"You cannot purchase this product {product_name} without a doctor's prescription.")
                                    break
                                else:
                                    product_List.append(product)
                                    break
                            except InvalidPrescriptionError as e:
                                print(e)
                    else:
                        product_List.append(product)

                return product_List
            except InvalidProductError as e:
                print(e)

    def adjust_the_reward_rate(self):
        while True:
            try:
                reward_rate = input("Enter reward rate: ")
                Validations.validate_reward_rate(reward_rate)
                BasicCustomer.set_reward_rate(reward_rate)
                break
            except InvalidRewardRateError as e:
                print(e)

    def adjust_the_discount_rate(self):
        while True:
            try:
                customer = input("Enter VIP customer id or name: ")
                Validations.validate_VIP_customer(customer, self.records.find_customer)
                discount_rate = input("Enter discount rate: ")
                Validations.validate_discount_rate(discount_rate)
                VIPCustomer.set_discount_rate(discount_rate)
                break
            except InvalidRewardRateError as e:
                print(e)
            except InvalidVIPCustomerError as e:
                print(e)

operations = Operations()
operations.display_menu()