from idlelib import query
import random
from tabulate import tabulate
import sqlalchemy as db

import warnings

warnings.filterwarnings("ignore")

engine = db.create_engine('mysql+pymysql://root:admin@localhost:3306/DB_0101?charset=utf8mb4')
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


def register(username, password, first_name, last_name, email_address, city, street, phone_number):
    iduser = random.randint(100, 1000)
    role = 'buyer'
    query = db.text('INSERT INTO user (iduser, username, role, password, first_name, last_name, email_address, city, street, phone_number) VALUES (:iduser, :username, :role, :password, :first_name, :last_name, :email_address, :city, :street, :phone_number)')
    raw_result = connection.execute(query, iduser=iduser, username=username, role=role, password=password, first_name=first_name, last_name=last_name, email_address=email_address, city=city, street=street, phone_number=phone_number)

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

    query1 = db.text('SELECT pr.idproduct , sum(ci.sales_number) as sum '
                    'FROM cart_item as ci '
                    'join product_supplier as psu on psu.idproduct_supplier = ci.idproduct_supplier'
                    ' join product as pr on pr.idproduct = ps.product_idproduct'
                    ' join transaction as t'
                    ' WHERE t.status =' + ' and EXTRACT(MONTH FROM b.date) as m'
                    ' group by pr.idproduct order by sum asc limit 5')
    raw_result = connection.execute(query)
    result = raw_result.fetchall()
    return result



def get_the_cheapest_seller_by_item(product):
        query = ('SELECT supplier_idsupplier , sum(s.price) as sum '
                 'FROM product_supplier as s '
                 'WHERE product_idproduct = :product and EXTRACT(MONTH FROM b.date) as m'
                 'group by supplier_idsupplier order by sum asc limit 1 ')
        raw_result = connection.execute(query, product=product)
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
    query = db.text('SELECT score FROM comment as c WHERE c.product_idproduct = :idproduct order by c.score desc limit 3')
    raw_result = connection.execute(query , idproduct = idproduct)
    result = raw_result.fetchall()
    return result

def get_bad_Score(idproduct):
    query = db.text('SELECT score FROM comment as c WHERE c.product_idproduct = :idproduct order by c.score asc limit 3')
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

def get_avg_sell_by_supplier(item):
    query = db.text(
        'SELECT  AVG(c.total_price) as average_sales_per_month '
        'FROM cart  c JOIN cart_item ci ON c.idcart = ci.cart_idcart'
        'JOIN product_supplier ps ON ci.idproduct_supplier = ps.idproduct_supplier'
        'JOIN product p ON ps.product_idproduct = p.idproduct'
        'WHERE c.date BETWEEN (NOW() - INTERVAL 1 MONTH) AND NOW()')
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

def add_product(color, available, name, model, ph_date, supplier_idsupplier):
    idproduct = random.randint(100, 1000)
    query = db.text('INSERT INTO product (idproduct, color, available, name, model, ph_date, supplier_idsupplier) VALUES (:idproduct, :color, :available, :name, :model, :ph_date, :supplier_idsupplier)')
    raw_result = connection.execute(query, idproduct=idproduct, color=color, available=available, name=name, model=model, ph_date=ph_date, supplier_idsupplier=supplier_idsupplier)
    result = raw_result.fetchall()
    return result


def delete_product(idproduct):
    query = db.text('DELETE FROM product where idproduct=:idproduct')
    raw_result = connection.execute(query, idproduct=idproduct)
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
        print('11. Get average sell by supplier')
        print('12. Get last order')
        print('13. Get comment')
        print('14. Get best score')
        print('15. Get bad score')
        print('16. Get user city')
        print('17. Get supplier city')
        print('18. Register')
        print('19. Add product')
        print('20. Edit product')
        print('21. Delete product')
        print('22. Edit users')
        print('23. Logout')
        print('24. Exit')
        print('25. Get supplier product')
        choice = input('Enter your choice: ')
        if choice == '1':
            login(input('Enter username: '), input('Enter password: '))
        elif choice == '18':
            username = input('Enter your username: ')
            password = input('Enter your password: ')
            first_name = input('Enter your first_name: ')
            last_name = input('Enter your last_name: ')
            email_address = input('Enter your email_address: ')
            city = input('Enter your city: ')
            street = input('Enter your street: ')
            phone_number = input('Enter your phone_number: ')
            register(username, password, first_name, last_name, email_address, city, street, phone_number)
            print('User created successfully!')
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
            elif choice == '6':
                best_users = [users.values() for users in get_the_best_users()]
                print(tabulate(best_users, headers=['idcustomer' , 'price']))
            elif choice == '7':
                best_sell = [sell.values() for sell in get_bestselling_products()]
                print(tabulate(best_sell, headers=['idproduct', 'sales_number']))
            elif choice == '8':
                offers = [offer.values() for offer in get_special_offer()]
                print(tabulate(offers, headers=['idproduct']))
            elif choice == '9':
                if IS_ADMIN:
                    seller = [sell.values() for sell in get_item_sale(input('Enter item:'))]
                    print(tabulate(seller, headers=['total_price']))
                else:
                    print('You must be admin to call this function!')
            elif choice == '10':
                if IS_ADMIN:
                    cheapest = [cheap_seller.values() for cheap_seller in
                                get_the_cheapest_seller_by_item(input('Enter product:'))]
                    print(tabulate(cheapest, headers=['idsupplier', 'price']))
                else:
                    print('You must be admin to call this function!')
            elif choice == '11':
                if IS_ADMIN:
                    avg_sell = [avg.values() for avg in get_avg_sell_by_supplier(input('Enter item:'))]
                    print(tabulate(avg_sell, headers=['total_price']))
                else:
                    print('You must be admin to call this function!')
            elif choice == '25':
                if IS_ADMIN:
                    supplier_product = [supplier.values() for supplier in get_supplier_product_for_admin(input('Enter product:'))]
                    print(tabulate(supplier_product, headers=['supplier_idsupplier']))
                else:
                    print('You must be admin to call this function!')
            elif choice == '12':
                last_order = [order.values() for order in get_last_order(input('Enter customer:'))]
                print(tabulate(last_order, headers=['idorder_history']))
            elif choice == '13':
                comment = [product.values() for product in get_comment(input('Enter product:'))]
                print(tabulate(comment, headers=['description']))
            elif choice == '14':
                best_score= [product.values() for product in get_best_Score(input('Enter product:'))]
                print(tabulate(best_score, headers=['score']))
            elif choice == '15':
                bad_Score = [product.values() for product in get_bad_Score(input('Enter product:'))]
                print(tabulate(bad_Score, headers=['score']))
            elif choice == '16':
                user_city = [user.values() for user in get_user_city(input('Enter city:'))]
                print(tabulate(user_city, headers=['username']))
            elif choice == '17':
                supplier_city = [supplier.values() for supplier in get_supplier_city(input('Enter city:'))]
                print(tabulate(supplier_city, headers=['name']))
            elif choice == '19':
                color = input('Enter your color: ')
                available = input('Enter your available: ')
                name = input('Enter your name: ')
                model = input('Enter your model: ')
                ph_date = input('Enter your ph_date: ')
                supplier_idsupplier = input('Enter your supplier_idsupplier: ')
                add_product(color, available, name, model, ph_date, supplier_idsupplier)
                print('Product created successfully!')
            elif choice == '20':
                pass
            elif choice == '21':
                idproduct = input('Enter idproduct:')
                delete_product(idproduct)
                print('Product deleted successfully!')
            elif choice == '22':
                if IS_ADMIN:
                    pass
                else:
                    print('Only admins can edit users')
            elif choice == '23':
                logout()
                print('You are logged out!')
            elif choice == '24':
                print('Thank you for using our shop.')
                exit()
        else:
            print('You are not logged in! Please login first!')
