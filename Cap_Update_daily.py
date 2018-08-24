import pymysql

def cap_update_daily(state_dt):
    para_norisk = (1.0 + 0.04/365)
    db = pymysql.connect(host='127.0.0.1', user='root', passwd='admin', db='stock', charset='utf8')
    cursor = db.cursor()
    sql_pool = "select * from my_stock_pool"
    cursor.execute(sql_pool)
    done_set = cursor.fetchall()
    db.commit()
    new_lock_cap = 0.00
    for i in range(len(done_set)):
        stock_code = str(done_set[i][0])
        stock_vol = float(done_set[i][2])
        sql = "select * from stock_info a where a.stock_code = '%s' and a.state_dt <= '%s' order by a.state_dt desc limit 1"%(stock_code,state_dt)
        cursor.execute(sql)
        done_temp = cursor.fetchall()
        db.commit()
        if len(done_temp) > 0:
            cur_close_price = float(done_temp[0][3])
            new_lock_cap += cur_close_price * stock_vol
        else:
            print('Cap_Update_daily Err!!')
            raise Exception
    sql_cap = "select * from my_capital order by seq asc"
    cursor.execute(sql_cap)
    done_cap = cursor.fetchall()
    db.commit()
    new_cash_cap = float(done_cap[-1][2]) * para_norisk
    new_total_cap = new_cash_cap + new_lock_cap
    sql_insert = "insert into my_capital(capital,money_lock,money_rest,bz,state_dt)values('%.2f','%.2f','%.2f','%s','%s')"%(new_total_cap,new_lock_cap,new_cash_cap,str('Daily_Update'),state_dt)
    cursor.execute(sql_insert)
    db.commit()
    return 1