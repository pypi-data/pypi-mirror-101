import numpy as np
import tushare as ts
class wen():

    def get_data_d_tu(self, stock_id, di):
        pro = ts.pro_api()
        return pro.daily(trade_date = di)
    def get_data_ti_tu(self):
        pass
    def cal_ret_an(self, ret_da):
        array_ret = np.array(ret_da)
        return array_ret.sum() / len(array_ret) * 360
    def cal_std_an(self, ret_da):
        array_ret = np.array(ret_da)
        return array_ret.std()  * (360 ** (1/2))

print("wen")