import pandas as pd
import numpy_financial as npf

def max_buyable_calc(period, bench_exp_ret, stk_exp_ret, cmp):
    bench_exp_ret = bench_exp_ret/100
    stk_exp_ret = stk_exp_ret/100
    future_stk_val = npf.fv(rate=stk_exp_ret, nper=period, pmt=0, pv=-cmp)
    max_buyable = round(npf.pv(rate=bench_exp_ret, nper=period, pmt=0, fv=-future_stk_val),2)
    return max_buyable

def risk_determination(eq_exposure, risk_per_trade, sl, cmp):
    risk_per_trade = risk_per_trade / 100 * eq_exposure
    per_sh_loss = cmp - sl
    max_pos_0 = round(risk_per_trade / per_sh_loss)
    return max_pos_0

    
    #tradebook = pd.DataFrame(columns=['Sno.', 'Allowed Qty', 'Qty bought', 'Price', 'Value'])
