--stocks
create table stocks(
    s_ticker varchar(6) not null,
    s_price decimal(4,2) not null,
    s_volume decimal(10,0) not null,
    s_cap decimal(15,2) not null
);

--users
create table users(
    u_userid integer primary key autoincrement,
    u_username text not null,
    u_password text not null,
    u_acctbal decimal(10,2) default 0.00
);

--portfolio
create table portfolio(
    p_userid decimal(8,0) not null,
    p_ticker varchar(6) not null,
    p_quantity decimal(6,0) not null
);

--watchlist
create table watchlist(
    w_userid decimal(8,0) not null,
    w_ticker varchar(6) not null
);

--orders
create table orders(
    o_orderid decimal(8,0) not null,
    o_userid decimal(8,0) not null,
    o_ticker varchar(6) not null,
    o_quantity decimal(6,0) not null,
    o_tickerprice decimal(4,2) not null,
    o_orderdate date not null
);

--crypto
create table crypto(
    c_ticker varchar(6) not null,
    c_price decimal(6,6) not null
);

--populate stocks table
.mode "csv";
.separator ",";
.import sample_stocks.csv stocks;

--insert random users
insert into users (u_username,u_password,u_acctbal) 
values
    ('misa','another',23000),
    ('robert','password',45000),
    ('kevin','1234',300),
    ('sql_expert','fRe5H!',50000),
    ('investor','NuMb3r5',32450),
    ('investor2','wesrd',34213),
    ('investor3','cwrbetrb',54323),
    ('investor4','cw34r',675343),
    ('investor5','byh57654',231),
    ('investor6','dft5y67',8324),
    ('investor7','qwergfd',2341),
    ('investor8','1234dfs',93245),
    ('sql_expert2','7y7dwd',12),
    ('modesto_student','bruh12!',342),
    ('turtlee','sl0w34',5634),
    ('shrek','3rffdww2',9999),
    ('merced_student','rufus',6000),
    ('horsee','mustangs',2),
    ('mac_adam','12edss',534);

insert into portfolio (p_userid, p_ticker, p_quantity)
values 
    (1,'APPL',2),
    (1,'AFL',3),
    (1,'ADSK',1),
    (1,'FFIV',4),
    (2,'APPL',10),
    (2,'GOOGL',2),
    (2,'FOX',4),
    (2,'HAL',2),
    (2,'HP',5),
    (2,'NDAQ',7),
    (3,'NVDA',1),
    (3,'APPL',5),
    (3,'PYPL',2),
    (3,'ROP',3),
    (3,'SIG',4),
    (3,'SNA',9),
    (4,'TAP',12),
    (4,'TRIP',10),
    (4,'TSCO',1),
    (5,'T',23),
    (5,'APPL',18),
    (5,'WAT',43),
    (5,'XRAY',1),
    (5,'ABC',21),
    (6,'ADS',3),
    (6,'AKAM',19),
    (7,'AMZN',2),
    (7,'BSX',11),
    (7,'CL',10),
    (7,'COP',12),
    (8,'AAL',2),
    (8,'CSCO',13),
    (8,'C',1),
    (8,'IBM',28),
    (8,'LB',5),
    (9,'GOOGL',21),
    (9,'APPL',3),
    (9,'FAST',31),
    (10,'KEY',8),
    (11,'AAL',3),
    (11,'AMZN',2),
    (11,'COP',4),
    (12,'IBM',17),
    (12,'APPL',13),
    (12,'XRAY',2),
    (12,'C',15),
    (13,'JEC',13),
    (13,'KMB',17),
    (14,'KO',1),
    (14,'LOW',13),
    (14,'NUE',27),
    (15,'APPl',12),
    (15,'SBUX',11),
    (16,'STZ',2),
    (16,'GOOGL',13),
    (17,'AMZN',19),
    (17,'MSFT',31);

insert into watchlist (w_userid, w_ticker)
values 
    (1,'STZ'),
    (1,'MSFT'),
    (2,'AZO'),
    (2,'BBT'),
    (2,'HCP'),
    (3,'HST'),
    (3,'PRU'),
    (3,'RHI'),
    (4,'DOV'),
    (4,'MSFT'),
    (4,'APPL'),
    (5,'ED'),
    (5,'GOOGL'),
    (5,'HAL'),
    (5,'HCP'),
    (5,'LOW'),
    (6,'ED'),
    (6,'PPL'),
    (6,'MSFT'),
    (6,'SNA'),
    (7,'TXT'),
    (7,'AAL'),
    (7,'COP'),
    (8,'UDR'),
    (8,'NFLX'),
    (8,'NDAQ'),
    (9,'NKE'),
    (9,'NFLX'),
    (10,'MSFT'),
    (10,'AMZN'),
    (18,'STZ'),
    (18,'APPL'),
    (19,'AMZN');
--
insert into orders (o_orderid, o_userid, o_ticker, o_quantity, o_tickerprice, o_orderdate)
values 
    (1,1,'APPL',2,14.02,'2014-03-02'),
    (2,1,'AFL',3,34.23,'2014-03-02'),
    (3,1,'ADSK',1,40.21,'2014-03-03'),
    (4,1,'FFIV',4,80.96,'2014-03-23'),
    (5,2,'APPL',10,13.95,'2014-03-29'),
    (6,2,'GOOGL',2,405.87,'2014-04-01'),
    (7,2,'FOX',4,20.45,'2014-04-03'),
    (8,2,'HAL',2,35.67,'2014-04-05'),
    (9,2,'HP',5,32.21,'2014-04-08'),
    (10,2,'NDAQ',7,45.24,'2014-04-08'),
    (11,3,'NVDA',1,11.15,'2014-04-09'),
    (12,3,'APPL',5,16.97,'2014-04-12'),
    (13,3,'PYPL',2,39.23,'2014-04-12'),
    (14,3,'ROP',3,115.03,'2014-04-13'),
    (15,3,'SIG',4,65.55,'2014-04-15'),
    (16,3,'SNA',9,32.22,'2014-04-28'),
    (17,4,'TAP',12,42.12,'2014-05-05'),
    (18,4,'TRIP',10,12.95,'2014-05-20'),
    (19,4,'TSCO',1,50.03,'2014-05-28'),
    (20,5,'T',23,32.39,'2014-06-17'),
    (21,5,'APPL',18,20.19,'2014-06-25'),
    (22,5,'WAT',43,103.44,'2014-06-29'),
    (23,5,'XRAY',1,31.18,'2014-07-04'),
    (24,5,'ABC',21,40.00,'2014-07-15'),
    (25,6,'ADS',3,130.45,'2014-07-30'),
    (26,6,'AKAM',19,30.23,'2014-08-09'),
    (27,7,'AMZN',2,130.99,'2014-08-18'),
    (28,7,'BSX',11,3.45,'2014-08-25'),
    (29,7,'CL',10,78.00,'2014-09-01'),
    (30,7,'COP',12,89.03,'2014-09-14'),
    (31,8,'AAL',2,18.32,'2014-09-27'),
    (32,8,'CSCO',13,27.41,'2014-10-10'),
    (33,8,'C',1,56.92,'2014-10-19'),
    (34,8,'IBM',28,155.19,'2014-10-30'),
    (35,8,'LB',5,50.00,'2014-11-07'),
    (36,9,'GOOGL',21,331.19,'2014-11-13'),
    (37,9,'APPL',3,11.20,'2014-11-26'),
    (38,9,'FAST',31,55.23,'2014-12-01'),
    (39,10,'KEY',8,4.32,'2014-12-05'),
    (40,11,'AAL',3,22.21,'2014-12-16'),
    (41,11,'AMZN',2,230.22,'2014-12-21'),
    (42,11,'COP',4,45.11,'2015-01-19'),
    (43,12,'IBM',17,200.13,'2015-01-28'),
    (44,12,'APPL',13,20.45,'2015-02-02'),
    (45,12,'XRAY',2,43.99,'2015-02-16'),
    (46,12,'C',15,40.56,'2015-02-27'),
    (47,13,'JEC',13,55.65,'2015-03-07'),
    (48,13,'KMB',17,81.15,'2015-03-16'),
    (49,14,'KO',1,51.37,'2015-03-29'),
    (50,14,'LOW',13,62.31,'2015-04-06'),
    (51,14,'NUE',27,34.92,'2015-04-20'),
    (52,15,'APPl',12,63.42,'2015-05-06'),
    (53,15,'SBUX',11,30.54,'2015-05-17'),
    (54,16,'STZ',2,35.62,'2015-05-23'),
    (55,16,'GOOGL',13,385.12,'2015-05-02'),
    (56,17,'AMZN',19,249.38,'2015-05-14'),
    (57,17,'MSFT',31,26.10,'2015-05-30'),
    (58,2,'BTC',2,15384.03,'2015-06-02'),
    (59,3,'ETH',1,1000.00,'2015-06-18'),
    (60,9,'BTC',12,12023.45,'2015-06-20'),
    (61,10,'XRP',3,0.5,'2015-07-01');

insert into crypto (c_ticker, c_price)
values 
    ('BTC',20100.00),
    ('ETH',1476.00),
    ('USDT',1.00),
    ('BNB',286.77),
    ('XRP',0.4626),
    ('BUSD',1.00),
    ('ADA',0.4106);

insert into orders (o_orderid, o_userid, o_ticker, o_quantity, o_tickerprice, o_orderdate)
values 
    (58,2,'BTC',2,15384.03,'2015-06-02'),
    (59,3,'ETH',1,1000.00,'2015-06-18'),
    (60,9,'BTC',12,12023.45,'2015-06-20'),
    (61,10,'XRP',3,0.5,'2015-07-01');

insert into watchlist (w_userid, w_ticker)
values 
    (18,'STZ'),
    (18,'APPL'),
    (19,'AMZN');

-- update a user's portfolio when they make an order on pre-existing stocks in their portfolio
update portfolio (p_userid,p_ticker,p_quantity)
set p_quantity = p_quantity + orders.o_quantity
from (select o_quantity,o_userid from orders)
where portfolio.p_userid=orders.o_userid and 
portfolio.p_ticker=orders.o_ticker

-- admin deletes users who terminate their account
delete from users 
where u_userid=4

-- user deletes from their watchlist
delete from watchlist
where u_userid=5

-- cancel transaction
delete from orders 
where u_userid=8

--Q1: get all stocks
select * from stocks;

--Q2: get all stocks beginning with the letter A
select * from stocks
where s_ticker like 'A%';

--Q3: get all stocks with a greater price than the avg price
select * from stocks
where s_price >
(select avg(s_price) from stocks);

--Q4: get all users that don't have a portfolio
select u_username from users
where u_userid not in
(select p_userid from portfolio);

--Q5: get the most popular stock
select pop_ticker from
(select p_ticker pop_ticker,count(p_ticker) cnt from portfolio
group by p_ticker
order by cnt desc
limit 1);

--Q6: get count of users who own amzn shares
select count(u_userid) from users
join portfolio on p_userid = u_userid
where p_ticker = 'AMZN';

--Q7: get all users who have enough balance to buy 10 shares of GOOGL
select u_username from users
where u_acctbal >=
(select 10*s_price from stocks
where s_ticker='GOOGL');

--Q8: get all orders for the month of july in 2014
select * from orders
where strftime('%Y-%m',o_orderdate) = '2014-07';

--Q9: get the user who made the most orders
select u_username from 
(select u_username, count(u_userid) cnt from users
join orders on o_userid=u_userid
group by u_username
order by cnt desc
limit 1
);

--Q10: get the user who made the biggest purchase
select u_username,purchase from
(select u_username, max(o_quantity*o_tickerprice) purchase from orders
join users on u_userid=o_userid);

--Q11: get all the stocks that haven't been ordered
select s_ticker from stocks
where s_ticker not in 
(select o_ticker from orders);

--Q12: get the users who are interested in a stock but have not bought yet
select distinct(u_username) from users
join watchlist on w_userid=u_userid
except 
select distinct(u_username) from users 
join portfolio on p_userid=u_userid;

--Q13: get the users who have at least one stock in which the return is negative
select distinct(u_username) from users 
join orders on o_userid=u_userid
join stocks on s_ticker=o_ticker
where o_tickerprice < s_price;

--Q14: order the stocks that have been purchsed by their market cap
select distinct(s_ticker),s_cap from stocks
join orders on o_ticker=s_ticker
order by s_cap desc;

--Q15: get the avg return for googl
select avg(((s_price-o_tickerprice)*o_quantity)/(o_quantity*o_tickerprice) * 100) as return from stocks
join orders on o_ticker=s_ticker
where s_ticker='GOOGL';


--Q16: get the all the users and the stocks that have yielded the highest return
select u_username,o_ticker, max(((s_price-o_tickerprice)*o_quantity)/(o_quantity*o_tickerprice) * 100) return from users
join orders on o_userid=u_userid
join stocks on s_ticker=o_ticker
group by u_username
order by return desc;

--Q17: Let's say a stock grows proportionally to the avg return rate of orders on the stock.
-- calculate how long it will take AMZN to reach $600/share
--refer to script.py 

--Q18: get the history of orders from a user
select u_username,o_ticker,o_quantity,o_tickerprice,o_orderdate from users 
join orders on o_userid=u_userid
where u_username = 'robert'
order by o_orderdate;

--Q19: get stocks that are on both of the watchlists of users misa and sql_expert
SELECT w_ticker
FROM stocks, users, watchlist
WHERE u_userid = w_userid
AND s_ticker = w_ticker
AND u_username = 'misa'
INTERSECT
SELECT w_ticker 
FROM stocks, users, watchlist
WHERE u_userid = w_userid
AND s_ticker = w_ticker
AND u_username = 'sql_expert';

--Q20: get the difference in average roi between stocks and crypto
select crypto_return-stock_return from 
(select avg(((s_price-o_tickerprice)*o_quantity)/(o_quantity*o_tickerprice) * 100) as stock_return 
from stocks
join orders on o_ticker=s_ticker),
(select avg(((c_price-o_tickerprice)*o_quantity)/(o_quantity*o_tickerprice) * 100) as crypto_return 
from crypto
join orders on o_ticker=c_ticker);

-- Get all the tickers from the portfolio of an individual
SELECT p_ticker, p_quantity FROM portfolio, users
WHERE u_userid = p_userid
AND u_username = 'misa';