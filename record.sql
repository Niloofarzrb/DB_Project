CREATE SCHEMA IF NOT EXISTS DB_0101;
USE DB_0101;


CREATE TABLE IF NOT EXISTS bill (
  idbill INT NOT NULL,
  date DATETIME NOT NULL,
  price VARCHAR(45) NOT NULL,
  PRIMARY KEY (idbill));

insert into bill values(1100 ,'2022-08-15 02:41' , 10000000);
insert into bill values(1200 ,'2021-07-15 12:32' , 2500000);
insert into bill values(1300 ,'2022-02-15 14:29' , 3700000);
insert into bill values(1400 ,'2022-05-15 06:41' , 5900000);
insert into bill values(1500 ,'2021-11-15 14:51' , 8700000);
insert into bill values(1600 ,'2022-03-15 16:51' , 9700000);

CREATE TABLE IF NOT EXISTS transaction (
  idtransaction INT NOT NULL,
  bank_name VARCHAR(45) NULL,
  type VARCHAR(45) NULL,
  date DATETIME NOT NULL,
  status VARCHAR(45) NOT NULL,
  pro_name MEDIUMTEXT NULL,
  bill_idbill INT NOT NULL,
  PRIMARY KEY (idtransaction),
  INDEX fk_transaction_bill1_idx (bill_idbill ASC),
  CONSTRAINT fk_transaction_bill1
    FOREIGN KEY (bill_idbill)
    REFERENCES bill (idbill)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

insert into transaction values(1 , 'tejarat' , '' , '2022-08-15 02:41' , '+' , 'galaxys7' , 1100  );
insert into transaction values(2 , 'tejarat' , '' , '2021-07-15 12:32' , '+' , 'galaxys7' , 1200  );
insert into transaction values(3 , 'tejarat' , '' , '2022-02-15 14:29' , '+' , 'galaxys7' , 1300  );
insert into transaction values(4 , 'tejarat' , '' , '2022-05-15 06:41' , '+' , 'galaxys7' , 1400  );
insert into transaction values(5 , 'tejarat' , '' , '2021-11-15 14:51' , '+' , 'galaxys7' , 1500  );
insert into transaction values(6 , 'tejarat' , '' , '2022-03-15 16:51' , '+' , 'galaxys7' , 1600  );

CREATE TABLE IF NOT EXISTS user (
	iduser int not null,
	username varchar(45) NOT NULL,
	role varchar(45) NOT NULL,
	password VARCHAR(45) NOT NULL,
    first_name VARCHAR(45) NULL,
	last_name VARCHAR(45) NOT NULL,
	email_address VARCHAR(45) NOT NULL,
	city MEDIUMTEXT NULL,
	street MEDIUMTEXT NULL,
	phone_number varchar(45) NOT NULL,
	PRIMARY KEY (iduser),
    CONSTRAINT UC_Person UNIQUE (username));

insert into user values(1,'majidrahnavard' , 'admin', 'a','majid' , 'rahnavard', 'majidrahnavard@gmail.com' , 'mashhad' , 'babak' , 09158675342 );
 insert into user values(2,'nikashakarami' , 'seller', 'c'  , 'nika' , 'shakarami'   , 'nikashakarmi@gmail.com' , 'tehran' , 'pirozi' , 09128794626 );
 insert into user values(3,'hamidrezarohi' , 'buyer', '5' , 'hamidreza' , 'rohi' ,   'hamidrezarohi@gmail.com' , 'karaj' , 'gohardasht' , 09336758421 );
 insert into user values(4,'hoseintorkaman' , 'buyer', 'vn' , 'hosein' , 'torkaman'   , 'mhosseintorkaman@gmail.com' , 'gorgan' , 'azadi' , 0935987462);
 insert into user values(5,'mahsaamini' , 'admin', 'm' , 'mahsa' , 'amini' ,   'mahsaamini@gmail.com' , 'sanandaj' , 'saghez' , 0912874563 );
 insert into user values(6,'sarinaesmaeilzadeh' , 'buyer', 'adv' ,'sarina' , 'esamaeilzadeh'  , 'sarinaesmaeilzadeh@gmail.com' , 'tehran' , 'tajrish' , 09336548792 );


CREATE TABLE IF NOT EXISTS customer (
  idcustomer INT NOT NULL,
  user_iduser INT NOT NULL,
  PRIMARY KEY (idcustomer, user_iduser),
  INDEX fk_customer_user1_idx (user_iduser ASC) ,
  CONSTRAINT fk_customer_user1
    FOREIGN KEY (user_iduser)
    REFERENCES user (iduser)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

insert into customer values(2 , 1);
insert into customer values(5 , 1);
insert into customer values(8 , 2);
insert into customer values(11 , 4);
insert into customer values(14 , 3);
insert into customer values(17 , 6);
insert into customer values(20 , 4);
insert into customer values(23 , 6);
insert into customer values(26 , 4);
insert into customer values(29 , 6);

CREATE TABLE IF NOT EXISTS supplier (
  idsupplier INT NOT NULL,
  name MEDIUMTEXT NULL,
  phone_number VARCHAR(63) NOT NULL,
  sales_number INT NOT NULL,
  user_iduser INT NOT NULL,
  PRIMARY KEY (idsupplier),
  INDEX fk_supplier_user1_idx (user_iduser ASC) ,
  CONSTRAINT fk_supplier_user1
    FOREIGN KEY (user_iduser)
    REFERENCES user (iduser)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

insert into supplier values(150 , 'mohammadi' , 09356487562 , 52 ,1  );
insert into supplier values(151 , 'sirosi' , 0933654821 , 35 , 2);
insert into supplier values(152 , 'nejati' , 0912054876 , 25 , 3 );
insert into supplier values(153 , 'razavi' , 0933654128 , 65 , 4);
insert into supplier values(154 , 'saadati' , 0915874963  , 69, 5);
insert into supplier values(155 , 'haraati' , 0936584216 ,53 , 6);

CREATE TABLE IF NOT EXISTS cart (
  idcart INT NOT NULL,
  cart_Detail LONGTEXT NOT NULL,
  date DATETIME NULL,
  total_price INT NOT NULL,
  customer_idcustomer INT NOT NULL,
  customer_user_iduser INT NOT NULL,
  bill_idbill INT NOT NULL,
  INDEX fk_cart_customer1_idx (customer_idcustomer ASC, customer_user_iduser ASC) ,
  INDEX fk_cart_bill1_idx (bill_idbill ASC) ,
  PRIMARY KEY (idcart),
  CONSTRAINT fk_cart_customer1
    FOREIGN KEY (customer_idcustomer , customer_user_iduser)
    REFERENCES customer (idcustomer , user_iduser)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_cart_bill1
    FOREIGN KEY (bill_idbill)
    REFERENCES bill (idbill)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

 INSERT INTO cart values (123 , ''  , '2022-08-15 02:41' , 10000000 , 2 , 1 , 1100 );
 INSERT INTO cart values (345 , ''  , '2022-02-15 14:29' , 2500000  , 5 , 2 , 1200 );
 INSERT INTO cart values (567 , ''  , '2022-05-15 06:41' , 3700000 , 20 , 3 , 1300  );
 INSERT INTO cart values (789 , ''  , '2021-11-15 14:51' ,  5900000 , 11 , 4 , 1400  );
 INSERT INTO cart values (258  , '' , '2022-03-15 16:51' ,  8700000 , 14 , 5 , 1500  );
 INSERT INTO cart values (369 , ''  , '2022-03-12 16:51' ,  9700000, 26 , 6 , 1600 );

CREATE TABLE IF NOT EXISTS post (
  delivery_code INT NOT NULL,
  date DATETIME NOT NULL,
  cart_idcart INT NOT NULL,
  PRIMARY KEY (delivery_code),
  INDEX fk_post_cart1_idx (cart_idcart ASC) ,
  CONSTRAINT fk_post_cart1
    FOREIGN KEY (cart_idcart)
    REFERENCES cart (idcart)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

 insert into post values(4534 , '2022-08-15 11:41' , 123);
 insert into post values(5307 , '2022-08-12 12:41' , 345);
 insert into post values(6104 , '2022-08-15 15:41' , 567);
 insert into post values(6538 , '2022-08-14 16:41' , 789);
 insert into post values(3721 , '2022-08-11 09:41' , 258);
 insert into post values(4185 , '2022-08-12 15:41' , 369);

CREATE TABLE IF NOT EXISTS price_history (
  ph_date DATETIME NOT NULL,
  value VARCHAR(45) NOT NULL,
  supplier_idsupplier INT NOT NULL,
  PRIMARY KEY (ph_date),
  INDEX fk_price_history_supplier1_idx (supplier_idsupplier ASC) ,
  CONSTRAINT fk_price_history_supplier1
    FOREIGN KEY (supplier_idsupplier)
    REFERENCES supplier (idsupplier)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

 insert into price_history values('2022-08-15 02:41' , 4500000 , 150 );
 insert into price_history values('2021-07-15 12:32' , 8500000 , 151 );
 insert into price_history values('2022-02-15 14:29' , 9600000 , 152 );
 insert into price_history values('2022-05-15 06:41' , 2500000 , 153);
 insert into price_history values('2021-11-15 14:51' , 3500000 , 154 );
 insert into price_history values('2022-03-12 16:51' , 1200000 , 155 );
 
CREATE TABLE IF NOT EXISTS product (
  idproduct INT NOT NULL,
  color TINYTEXT NOT NULL,
  available varchar(45) NOT NULL,
  name LONGTEXT NOT NULL,
  model MEDIUMTEXT NOT NULL,
  ph_date DATETIME NOT NULL,
  supplier_idsupplier INT NOT NULL,
  PRIMARY KEY (idproduct),
  INDEX fk_product_price_history1_idx (ph_date ASC) ,
  INDEX fk_product_supplier1_idx (supplier_idsupplier ASC) ,
  CONSTRAINT fk_product_price_history1
    FOREIGN KEY (ph_date)
    REFERENCES price_history (ph_date)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_product_supplier1
    FOREIGN KEY (supplier_idsupplier)
    REFERENCES supplier (idsupplier)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

INSERT INTO product values (1 , 'red' , '+' , 'galaxys7','sumsung' ,'2022-08-15 02:41' , 150);
INSERT INTO product values (2 , 'gold' , '+'  ,'iphone12promax','iphone' ,'2021-07-15 12:32' , 151);
INSERT INTO product values (3 , 'black' , '+'  ,'galaxynote10', 'sumsung' ,'2022-02-15 14:29' , 152);
INSERT INTO product values (4 , 'white' , '+'  ,'iphonex','iphone' ,'2022-05-15 06:41' , 153);
INSERT INTO product values (5 , 'black' , '+'  ,'sonyxperia','sony' ,'2021-11-15 14:51' , 154);
INSERT INTO product values (6 , 'rosegold' , '+' , 'a7','sumsung' ,'2022-03-12 16:51' , 155);

create table product_supplier
(
	idproduct_supplier int not null,
    product_idproduct   int not null,
    supplier_idsupplier int not null,
    price               int not null,
    primary key(idproduct_supplier),
    constraint product_idproduct_fk
        foreign key (product_idproduct) references product (idproduct),
    constraint supplier_idsupplier_fk
        foreign key (supplier_idsupplier) references supplier (idsupplier)
);

insert into product_supplier values(0,1, 150 , 15000000);
insert into product_supplier values(1,1, 151 , 14900000);
insert into product_supplier values(2,1, 152 , 16000000);
insert into product_supplier values(3,1, 153 , 15500000);
insert into product_supplier values(4,1, 154 , 17000000);
insert into product_supplier values(5,1, 155 , 14000000);
insert into product_supplier values(6,2, 150 , 80000000);
insert into product_supplier values(7,2, 151 , 75000000);
insert into product_supplier values(8,2, 152 , 68000000);
insert into product_supplier values(9,3, 153 , 20000000);
insert into product_supplier values(10,3, 154 , 22000000);
insert into product_supplier values(11,3, 155 , 21000000);
insert into product_supplier values(12,4, 150 , 35000000);
insert into product_supplier values(13,4, 152 , 38000000);
insert into product_supplier values(14,4, 154 , 37000000);
insert into product_supplier values(15,5, 151 , 32000000);
insert into product_supplier values(16,5, 153 , 38000000);
insert into product_supplier values(17,6, 155 , 8000000);
insert into product_supplier values(18,6, 150 , 6000000);



CREATE TABLE IF NOT EXISTS cart_item (
  idcart_item INT NOT NULL,
  total_price INT NOT NULL,
  sales_number INT NULL,
  total_cost INT NOT null,
  cart_idcart INT NOT NULL,
  idproduct_supplier int not null,
  PRIMARY KEY (idcart_item),
constraint priduct_supplier_idproduct_supplier_fk
        foreign key (idproduct_supplier)
        references product_supplier (idproduct_supplier),
  INDEX fk_cart_item_cart1_idx (cart_idcart ASC),
  CONSTRAINT fk_cart_item_cart1
    FOREIGN KEY (cart_idcart)
    REFERENCES cart (idcart)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

insert into cart_item values(1 , 10000000 , 5  , 9000000 , 123 ,0);
insert into cart_item values(2 , 2500000 , 2  , 2000000  , 345 ,0);
insert into cart_item values(3 , 3700000 , 3 , 2900000 , 567 ,1);
insert into cart_item values(4 , 5900000 , 1  , 5100000  , 789 ,1);
insert into cart_item values(5 , 8700000 , 3  , 7500000 , 258 ,2);
insert into cart_item values(6 , 9700000 , 2  , 9100000 , 369 ,2);

create table IF not exists cart_item_costumer(
	id int not null,
    idbill int not null, 
    idcustomer int not null,
    number  int not null,
    primary key(id),
    INDEX fk_cart_item_bill_idx (idbill ASC),
	CONSTRAINT fk_cart_item_has_bill_bill1
    FOREIGN KEY (idbill)
    REFERENCES bill (idbill)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
	INDEX fk_cart_item_customer1_idx (idcustomer ASC) ,
  CONSTRAINT fk_cart_item_customer1
    FOREIGN KEY (idcustomer)
    REFERENCES customer (idcustomer)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

insert into cart_item_costumer values(1 , 1100 ,1 , 1);
insert into cart_item_costumer values(2 , 1100 ,1 , 2);
insert into cart_item_costumer values(3 , 1200 ,2 , 3);
insert into cart_item_costumer values(4 , 1200 , 3, 4);
insert into cart_item_costumer values(5 , 1300 ,4, 2);
insert into cart_item_costumer values(6 , 1100 ,2 , 3);
insert into cart_item_costumer values(7 , 1400 ,3 , 1);
insert into cart_item_costumer values(8 , 1500 ,5 , 2);
insert into cart_item_costumer values(9 , 1600 ,4, 5);
insert into cart_item_costumer values(10 , 1300 ,6 , 5);

CREATE TABLE IF NOT EXISTS offer (
  idoffer INT NOT NULL,
  start_date DATETIME NULL,
  end_date DATETIME NULL,
  discount_rate VARCHAR(45) NULL,
  offercol VARCHAR(45) NULL,
  product_idproduct INT NOT NULL,
  PRIMARY KEY (idoffer),
  INDEX fk_offer_product1_idx (product_idproduct ASC) ,
  CONSTRAINT fk_offer_product1
    FOREIGN KEY (product_idproduct)
    REFERENCES product (idproduct)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

 INSERT INTO offer  values (20 ,'2022-06-15 00:00', '2022-08-20 00:00','11' , '' , 1);
 INSERT INTO offer  values (21 ,'2021-01-1 00:00', '2021-01-5 00:00','25' , '' , 2);
 INSERT INTO offer  values (22 ,'2022-06-5 00:00', '2022-08-8 00:00','27' , '' , 3);
 INSERT INTO offer  values (23 ,'2022-08-12 00:00', '2022-09-23 00:00','15' , '' , 4);
 INSERT INTO offer  values (24 ,'2022-01-27 00:00', '2021-02-17 00:00','16' , '' , 5);
 INSERT INTO offer  values (25 ,'2022-03-27 00:00', '2022-04-12 00:00','5' , '' , 6);


CREATE TABLE IF NOT EXISTS category (
  idcategory INT NOT NULL,
  name VARCHAR(63) NULL,
  product_idproduct INT NOT NULL,
  PRIMARY KEY (idcategory),
  INDEX fk_category_product1_idx (product_idproduct ASC) ,
  CONSTRAINT fk_category_product1
    FOREIGN KEY (product_idproduct)
    REFERENCES product (idproduct)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

insert into category values(1 , 'galaxy-s7' , 1);
insert into category values(2 , 'iphone-14-pro-max' , 2);
insert into category values(3 , 'honor-8-lite' , 3);
insert into category values(4 , 'redmi-k60' , 4);
insert into category values(5 , 'sumsung-galaxy-A52s' , 5);
insert into category values(6, 'ipad-pro-12.9' , 6);





CREATE TABLE IF NOT EXISTS comment (
  idcomment INT NOT NULL,
  description longtext NULL,
  score smallint not null,
  product_idproduct INT NOT NULL,
  customer_idcustomer INT NOT NULL,
  PRIMARY KEY (idcomment),
  INDEX fk_comment_product1_idx (product_idproduct ASC),
  CONSTRAINT fk_comment_product1
    FOREIGN KEY (product_idproduct)
    REFERENCES product (idproduct)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  INDEX fk_comment_customer1_idx (customer_idcustomer ASC) ,
  CONSTRAINT fk_comment_customer1
    FOREIGN KEY (customer_idcustomer)
    REFERENCES customer (idcustomer)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

    insert into comment values(147 , 'perfect' , 4 , 1 , 2);
    insert into comment values(123 , 'good' , 3 , 2 , 5);
    insert into comment values(159 , 'bad' , 1 , 3 , 8);
    insert into comment values(357 , 'good' , 4 , 4 , 11);
    insert into comment values(456 , 'perfect' , 4 , 5 , 14);
    insert into comment values(251 , 'aowful' , 0 , 6 , 17);