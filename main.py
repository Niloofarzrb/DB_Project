from tabulate import tabulate
import sqlalchemy as db

import warnings

warnings.filterwarnings("ignore")

engine = db.create_engine('mysql+pymysql://root:Niloo8580far@localhost:3306/DB_0101?charset=utf8mb4')
connection = engine.connect()

IS_LOGGED_IN = False
IS_ADMIN = False


def login(username, password):
    query = db.text('SELECT * FROM user WHERE username = :username AND password = :password')
    raw_result = connection.execute(query, username=username, password=password)
    result = raw_result.fetchall()
    if len(result) == 1:
        global IS_LOGGED_IN
        IS_LOGGED_IN = True
        if result[0][2] == 'admin':
            global IS_ADMIN
            IS_ADMIN = True

        print('You are logged in!')
    else:
        print('Wrong username or password! Please try again.')


def logout():
    global IS_LOGGED_IN
    IS_LOGGED_IN = False
    global IS_ADMIN
    IS_ADMIN = False


def get_products():
    query = db.text('SELECT idproduct, color, available, price, name, model, ph_date FROM product')
    raw_result = connection.execute(query)
    result = raw_result.fetchall()
    return result


def get_users():
    query = db.text('SELECT * FROM user')
    raw_result = connection.execute(query)
    result = raw_result.fetchall()
    return result


def get_categories():
    query = db.text('SELECT name FROM category')
    raw_result = connection.execute(query)
    result = raw_result.fetchall()
    return result


def get_orders():
    query = db.text('SELECT idcart, cart_Detail, total_price FROM cart')
    raw_result = connection.execute(query)
    result = raw_result.fetchall()
    return result


def get_the_best_users():
    pass


def get_bestselling_products():
    pass


def get_special_offer():
    # get list of products that have discount more than 15%
    pass


def get_item_seller(item):
    query = db.text(
        'SELECT users.name, users.surname FROM users JOIN products ON users.id = products.seller_id WHERE products.id = :item')
    raw_result = connection.execute(query, item=item)
    result = raw_result.fetchall()
    return result


def get_the_cheapest_seller_by_item(item):
    pass

def avg_sell_by_supplier(item):
    query = db.text(
        'select name, date, avg(cart_item.total_cost) FROM product_supplier, cart'
            'JOIN supplier ON product_supplier.supplier_idsupplier = supplier.idsupplier'
            'JOIN cart_item On cart_item.idproduct_supplier = product_supplier.idproduct_supplier'
            'JOIN cart ON cart_item.cart_idcart = cart.idcart'
            'GROUP BY product_supplier.supplier_idsupplier, date')
    raw_result = connection.execute(query, item=item)
    result = raw_result.fetchall()
    return result

def get_last_order(idcustomer):
    query = db.text('SELECT idorder_history FROM order_history where  idcustomer = :idcustomer '
                    'order  by sum(idorder_history) desc limit 10')
    raw_result = connection.execute(query , idcustomer = idcustomer)
    result = raw_result.fetchall()
    return result


if __name__ == '__main__':
    print('Welcome to our shop!')
    while True:
        print('1. Login')
        print('2. Get products')
        print('3. Get users')
        print('4. Get categories')
        print('5. Get orders')
        print('6. Get the best users')
        print('7. Get best selling products')
        print('8. Get special offer')
        print('9. Get item seller')
        print('10. Get the cheapest seller by item')
        print('11. Logout')
        print('12. Exit')
        choice = input('Enter your choice: ')
        if choice == '1':
            login(input('Enter username: '), input('Enter password: '))
        elif IS_LOGGED_IN:
            if choice == '2':
                products = [product.values() for product in get_products()]
                print(tabulate(products,
                               headers=['idproduct', 'color', 'available', 'price', 'name', 'model', 'ph_date']))
            elif choice == '3':
                users = map(lambda x: list(x), get_users())
                print(tabulate(users, headers=['id', 'password']))
            elif choice == '4':
                categories = [category.values() for category in get_categories()]
                print(tabulate(categories, headers=['name']))
            elif choice == '5':
                orders = [order.values() for order in get_orders()]
                print(tabulate(orders, headers=['idcart', 'cart_Detail', 'total_price']))

        else:
            print('You are not logged in! Please login first!')
