import pymysql.cursors
import Deal
import Operator

def filter_main(stock_new,state_dt,predict_dt,poz):
    # 建立数据库连接
    db = pymysql.connect(host='127.0.0.1', user='root', passwd='admin', db='stock', charset='utf8')
    cursor = db.cursor()

    #先更新持股天数
    sql_update_hold_days = 'update my_stock_pool w set w.hold_days = w.hold_days + 1'
    cursor.execute(sql_update_hold_days)
    db.commit()

    #先卖出
    deal = Deal.Deal(state_dt)
    stock_pool_local = deal.stock_pool
    for stock in stock_pool_local:
        sql_predict = "select predict from good_pool_all a where a.state_dt = '%s' and a.stock_code = '%s'"%(predict_dt,stock)
        cursor.execute(sql_predict)
        done_set_predict = cursor.fetchall()
        predict = 0
        if len(done_set_predict) > 0:
            predict = int(done_set_predict[0][0])
        ans = Operator.sell(stock,state_dt,predict)

    #后买入
    for stock_index in range(len(stock_new)):
        deal_buy = Deal.Deal(state_dt)

        # # 如果模型f1分值低于50则不买入
        # sql_f1_check = "select * from good_pool_all a where a.stock_code = '%s' and a.state_dt < '%s' order by a.state_dt desc limit 1"%(stock_new[stock_index],state_dt)
        # cursor.execute(sql_f1_check)
        # done_check = cursor.fetchall()
        # db.commit()
        # if len(done_check) > 0:
        #     if float(done_check[0][4]) < 0.5:
        #         print('F1 Warning !!')
        #         continue


        ans = Operator.buy(stock_new[stock_index],state_dt,poz[stock_index]*deal_buy.cur_money_rest)
        del deal_buy
    db.close()
