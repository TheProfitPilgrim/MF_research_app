import pandas as pd
from  scipy.stats import skewnorm 
import os
from fitter import Fitter

def calc_prob_lr(current_price, current_pe):
    
    df = pd.read_csv(os.path.join("Data", "india_data", "nifty50_data.csv"))
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df.sort_values("Date", inplace=True)
    
    a1 = -343.73116546017627
    b1 = 23.296543524524147
    df['Predicted_Close'] = a1 + b1 * df['Earnings']
    df['Percentage_Deviation'] = ((df['Predicted_Close'] - df['Close']) / df['Close']) * 100
    
    data = df["Percentage_Deviation"].dropna().values
    f = Fitter(
        data,
        distributions=['norm', 'lognorm', 'gamma', 'beta', 't', 'laplace', 'skewnorm', 'expon', 'uniform'],
        timeout=30
    )
    f.fit()

    best = f.get_best()
    best_name = list(best.keys())[0]
    best_params = best[best_name]
    
    a = best_params["a"]    
    loc = best_params["loc"]  
    scale = best_params["scale"] 

    crt_price = current_price
    crt_pe = current_pe
    crt_earn = crt_price / crt_pe
    pred_price = a1 + b1*crt_earn
    x = (pred_price - crt_price) / crt_price * 100
    p_left = skewnorm.cdf(x, a, loc=loc, scale=scale)
    p_right = round((1 - p_left)*100,2)
    p_left = round(p_left*100,2)
    prob_increasing = p_left
    prob_decreasing = p_right

    return pred_price, x, prob_increasing, prob_decreasing, data, best_params, best_name