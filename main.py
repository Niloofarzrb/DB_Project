from idlelib import query

from tabulate import tabulate
import sqlalchemy as db

import warnings

warnings.filterwarnings("ignore")

engine = db.create_engine('mysql+pymysql://root:Yasaminazizi1380@localhost:3306/DB_0101?charset=utf8mb4')
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
def get_special_offer():
    # get list of products that have discount more than 15%
    query = db.text('SELECT product_idproduct as pro '
                    'FROM offer '
                    'WHERE discount_rate > 15')
    raw_result = connection.execute(query)
    result = raw_result.fetchall()
    return result
def get_item_sale(item):
    query = db.text('SELECT SUM(ci.total_price) as total_sales_per_month FROM product p'
    'JOIN product_supplier ps ON p.idproduct = ps.product_idproduct'
    'JOIN cart_item ci ON ps.idproduct_supplier = ci.idproduct_supplier'
    'JOIN cart c ON ci.cart_idcart = c.idcart'
    'WHERE p.name = :item'
    'AND c.date BETWEEN (NOW() - INTERVAL 1 MONTH) AND NOW()')
    raw_result = connection.execute(query, item=item)
    result = raw_result.fetchall()
    return result
def get_supplier_product_for_admin(product):
    query = db.text('SELECT supplier_idsupllier  '
                    'FROM product_supplier as s'
                    ' where s.product_idproduct = :product')
    raw_result = connection.execute(query, product=product)
    result = raw_result.fetchall()
    return result

def get_the_best_users():
    query = db.text('SELECT c.idcustomer , sum(b.price) as s '
                    'FROM customer as c '
                    'join cart on cart.idcostumer = c.idcustomer '
                    'join transaction as t on t.idcart = cart.idcart '
                    'WHERE t.status = '+' and EXTRACT(WEEK FROM b.date) as w '
                    'FROM bill as b '
                    'group by c.idcustomer order by s desc limit 10')

    query1 = db.text('SELECT cu.idcustomer , sum(b.price) as sum '
                    'FROM customer as cu '
                    'join cart on cart.idcostumer = cu.idcustomer '
                    'join transaction as tr on tr.idcart = cart.idcart '
                    'WHERE tr.status = ' + ' and EXTRACT(MONTH FROM b.date) as m '
                    'FROM bill as b '
                    'group by cu.idcustomer order by sum desc limit 10')
    raw_result = connection.execute(query , query1)
    result = raw_result.fetchall()
    return result


def get_bestselling_products():
    query = db.text('SELECT p.idproduct , sum(c.sales_number) as s '
                    'FROM cart_item as c '
                    'join product_supplier as ps on ps.idproduct_supplier = c.idproduct_supplier'
                    ' join product as p on p.idproduct = ps.product_idproduct'
                    'join transaction as tr'
                    'WHERE tr.status ='+' and  EXTRACT(WEEK FROM b.date) as w'
                    'group by p.idproduct order by s asc limit 5')

    query = db.text('SELECT pr.idproduct , sum(ci.sales_number) as sum '
                    'FROM cart_item as ci '
                    'join product_supplier as psu on psu.idproduct_supplier = ci.idproduct_supplier'
                    ' join product as pr on pr.idproduct = ps.product_idproduct'
                    ' join transaction as t'
                    ' WHERE t.status =' + ' and EXTRACT(MONTH FROM b.date) as m'
                    ' group by pr.idproduct order by sum asc limit 5')
    pass



def get_the_cheapest_seller_by_item(product):
    query = ('SELECT supplier_idsupplier , sum(s.price) as sum '
             'FROM product_supplier as s '
             'WHERE product_idproduct = :product and EXTRACT(MONTH FROM b.date) as m'
             'group by supplier_idsupplier order by sum asc limit 1 ')
    raw_result = connection.execute(query , product=product)
    result = raw_result.fetchall()
    return result

def avg_sell_by_supplier(item):
    query = db.text(
        'SELECT  AVG(c.total_price) as average_sales_per_month '
        'FROM cart  c JOIN cart_item ci ON c.idcart = ci.cart_idcart'
        'JOIN product_supplier ps ON ci.idproduct_supplier = ps.idproduct_supplier'
        'JOIN product p ON ps.product_idproduct = p.idproduct'
        'WHERE c.date BETWEEN (NOW() - INTERVAL 1 MONTH) AND NOW()')
    raw_result = connection.execute(query, item=item)
    result = raw_result.fetchall()
    return result

def get_last_order(idcustomer):
    query = db.text('SELECT idorder_history FROM order_history where  idcustomer = :idcustomer '
                    'order  by sum(idorder_history) desc limit 10')
    raw_result = connection.execute(query , idcustomer = idcustomer)
    result = raw_result.fetchall()
    return result

def get_comment(idproduct):
    query = db.text('SELECT description FROM comment as c WHERE c.product_idproduct = :idproduct')
    raw_result = connection.execute(query , idproduct = idproduct)
    result = raw_result.fetchall()
    return result

def get_best_Score(idproduct):
    query = db.text('SELECT descript FROM comment as c WHERE c.product_idproduct = :idproduct order by c.score desc limit 3')
    raw_result = connection.execute(query , idproduct = idproduct)
    result = raw_result.fetchall()
    return result
def get_bad_Score(idproduct):
    query = db.text('SELECT descript FROM comment as c WHERE c.product_idproduct = :idproduct order by c.score asc limit 3')
    raw_result = connection.execute(query , idproduct = idproduct)
    result = raw_result.fetchall()
    return result

def get_user_city(city):
    query = db.text('SELECT username FROM user where user.city = :city')
    raw_result = connection.execute(query , city = city)
    result = raw_result.fetchall()
    return result

def get_supplier_city(city):
    query = db.text('SELECT name FROM supplier as s WHERE s.city = :city ')
    raw_result = connection.execute(query , city = city)
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
