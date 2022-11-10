import math
import sqlite3 

def sqlite_ln(x):
    return math.log(x)

def main():
    con = sqlite3.connect("main.sqlite")
    con.create_function("ln",1,sqlite_ln)
    cur = con.cursor()
    sql = """select ln(600/s_price)/(365*(ln(1+((return_rate/100)/365)))) from
(select s_price,avg(((s_price-o_tickerprice)*o_quantity)/(o_quantity*o_tickerprice) * 100) as return_rate from stocks
join orders on o_ticker=s_ticker
where s_ticker='AMZN');"""
    cur.execute(sql)
    print("{:.3f}".format(round(cur.fetchone()[0],3)) + ' years')

if __name__ == "__main__":
    main()