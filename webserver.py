from typing import List
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import sqlalchemy as db
import warnings

warnings.filterwarnings("ignore")


class LoginModel(BaseModel):
    username: str
    password: str


class ResponseModel(BaseModel):
    message: str
    result: List
    result_count: int


app = FastAPI(title="DB_Project")

engine = db.create_engine('mysql+pymysql://root:admin@localhost:3306/DB_0101?charset=utf8mb4')
connection = engine.connect()

IS_LOGGED_IN = False
IS_ADMIN = False


@app.get("/")
async def root():
    return {"message": "The webserver is running..."}


@app.post("/login", response_model=ResponseModel)
def login(request: LoginModel):
    query = db.text('SELECT * FROM user WHERE username = :username AND password = :password')
    raw_result = connection.execute(query, username=request.username, password=request.password)
    result = raw_result.fetchall()
    if len(result) == 1:
        global IS_LOGGED_IN
        IS_LOGGED_IN = True
        if result[0][2] == 'admin':
            global IS_ADMIN
            IS_ADMIN = True

        message = 'You are logged in!'
    else:
        message = 'Wrong username or password! Please try again.'

    return {'message': message, 'result': [], 'result_count': 0}


@app.get("/logout", response_model=ResponseModel)
def logout():
    global IS_LOGGED_IN
    global IS_ADMIN
    IS_LOGGED_IN = False
    IS_ADMIN = False

    return {'message': 'You are logged out!', 'result': [], 'result_count': 0}


@app.get("/products", response_model=ResponseModel)
async def get_products():
    if IS_LOGGED_IN:
        query = db.text('SELECT idproduct, color, available, price, name, model, ph_date FROM product')
        raw_result = connection.execute(query)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}


@app.get("/users")
async def get_users():
    if IS_LOGGED_IN:
        query = db.text('SELECT * FROM user')
        raw_result = connection.execute(query)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}

@app.get("/categories")
async def get_categories():
    if IS_LOGGED_IN:
        query = db.text('SELECT name FROM category')
        raw_result = connection.execute(query)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}

@app.get("/orders")
async def get_orders():
    if IS_LOGGED_IN:
        query = db.text('SELECT idcart, cart_Detail, total_price FROM cart')
        raw_result = connection.execute(query)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}

@app.get("/special_offer")
async def get_special_offer():
    if IS_LOGGED_IN:
        query = db.text('SELECT product_idproduct as pro '
                    'FROM offer '
                    'WHERE discount_rate > 15')
        raw_result = connection.execute(query)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}

@app.get("/item_sale")
async def get_item_sale(item):
    if IS_LOGGED_IN:
        query = db.text('SELECT SUM(ci.total_price) as total_sales_per_month FROM product p'
                    'JOIN product_supplier ps ON p.idproduct = ps.product_idproduct'
                    'JOIN cart_item ci ON ps.idproduct_supplier = ci.idproduct_supplier'
                    'JOIN cart c ON ci.cart_idcart = c.idcart'
                    'WHERE p.name = :item'
                    'AND c.date BETWEEN (NOW() - INTERVAL 1 MONTH) AND NOW()')
        raw_result = connection.execute(query, item=item)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}

@app.get("/supplier_product_for_admin")
async def get_supplier_product_for_admin(product):
    if IS_LOGGED_IN:
        query = db.text('SELECT supplier_idsupllier  '
                    'FROM product_supplier as s'
                    ' where s.product_idproduct = :product')
        raw_result = connection.execute(query, product=product)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}

@app.get("/best_users")
async def get_the_best_users():
    if IS_LOGGED_IN:
        query = db.text('SELECT c.idcustomer , sum(b.price) as s '
                    'FROM customer as c '
                    'join cart on cart.idcostumer = c.idcustomer '
                    'join transaction as t on t.idcart = cart.idcart '
                    'WHERE t.status = ' + ' and EXTRACT(WEEK FROM b.date) as w '
                                          'FROM bill as b '
                                          'group by c.idcustomer order by s desc limit 10')

        query1 = db.text('SELECT cu.idcustomer , sum(b.price) as sum '
                     'FROM customer as cu '
                     'join cart on cart.idcostumer = cu.idcustomer '
                     'join transaction as tr on tr.idcart = cart.idcart '
                     'WHERE tr.status = ' + ' and EXTRACT(MONTH FROM b.date) as m '
                                            'FROM bill as b '
                                            'group by cu.idcustomer order by sum desc limit 10')
        raw_result = connection.execute(query, query1)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}

@app.get("/bestselling_products")
async def get_bestselling_products():
    if IS_LOGGED_IN:
        query = db.text('SELECT p.idproduct , sum(c.sales_number) as s '
                    'FROM cart_item as c '
                    'join product_supplier as ps on ps.idproduct_supplier = c.idproduct_supplier'
                    ' join product as p on p.idproduct = ps.product_idproduct'
                    'join transaction as tr'
                    'WHERE tr.status =' + ' and  EXTRACT(WEEK FROM b.date) as w'
                                          'group by p.idproduct order by s asc limit 5')

        query = db.text('SELECT pr.idproduct , sum(ci.sales_number) as sum '
                    'FROM cart_item as ci '
                    'join product_supplier as psu on psu.idproduct_supplier = ci.idproduct_supplier'
                    ' join product as pr on pr.idproduct = ps.product_idproduct'
                    ' join transaction as t'
                    ' WHERE t.status =' + ' and EXTRACT(MONTH FROM b.date) as m'
                                          ' group by pr.idproduct order by sum asc limit 5')
        raw_result = connection.execute(query)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}


@app.get("/item_seller")
async def get_item_seller(item):
    if IS_LOGGED_IN:
        query = db.text('SELECT iduser , username as n FROM user  , product_supplier as ps where ')
        raw_result = connection.execute(query)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}

@app.get("/cheapest_seller_bu_item")
async def get_the_cheapest_seller_by_item(product):
    if IS_LOGGED_IN:
        query = ('SELECT supplier_idsupplier , sum(s.price) as sum '
             'FROM product_supplier as s '
             'WHERE product_idproduct = :product and EXTRACT(MONTH FROM b.date) as m'
             'group by supplier_idsupplier order by sum asc limit 1 ')
        raw_result = connection.execute(query, product=product)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}

@app.get("/avg_sell_by_supplier")
async def avg_sell_by_supplier(item):
    if IS_LOGGED_IN:
        query = db.text(
        'SELECT  AVG(c.total_price) as average_sales_per_month '
        'FROM cart  c JOIN cart_item ci ON c.idcart = ci.cart_idcart'
        'JOIN product_supplier ps ON ci.idproduct_supplier = ps.idproduct_supplier'
        'JOIN product p ON ps.product_idproduct = p.idproduct'
        'WHERE c.date BETWEEN (NOW() - INTERVAL 1 MONTH) AND NOW()')
        raw_result = connection.execute(query, item=item)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}

@app.get("/last_order")
async def get_last_order(idcustomer):
    if IS_LOGGED_IN:
        query = db.text('SELECT idorder_history FROM order_history where  idcustomer = :idcustomer '
                    'order  by sum(idorder_history) desc limit 10')
        raw_result = connection.execute(query, idcustomer=idcustomer)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}

@app.get("/comment")
async def get_comment(idproduct):
    if IS_LOGGED_IN:
        query = db.text('SELECT description FROM comment as c WHERE c.product_idproduct = :idproduct')
        raw_result = connection.execute(query, idproduct=idproduct)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}

@app.get("/best_score")
async def get_best_Score(idproduct):
    if IS_LOGGED_IN:
        query = db.text(
        'SELECT descript FROM comment as c WHERE c.product_idproduct = :idproduct order by c.score desc limit 3')
        raw_result = connection.execute(query, idproduct=idproduct)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}

@app.get("/bad_score")
async def get_bad_Score(idproduct):
    if IS_LOGGED_IN:
        query = db.text(
        'SELECT descript FROM comment as c WHERE c.product_idproduct = :idproduct order by c.score asc limit 3')
        raw_result = connection.execute(query, idproduct=idproduct)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}

@app.get("/user_city")
async def get_user_city(city):
    if IS_LOGGED_IN:
        query = db.text('SELECT username FROM user where user.city = :city')
        raw_result = connection.execute(query, city=city)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}

@app.get("/supplier_city")
async def get_supplier_city(city):
    if IS_LOGGED_IN:
        query = db.text('SELECT name FROM supplier as s WHERE s.city = :city ')
        raw_result = connection.execute(query, city=city)
        result = raw_result.fetchall()
        message = 'Successful operation!'
    else:
        result = []
        message = 'You are not logged in! Please login first!'

    return {'message': message, 'result': result, 'result_count': len(result)}


uvicorn.run(app)
