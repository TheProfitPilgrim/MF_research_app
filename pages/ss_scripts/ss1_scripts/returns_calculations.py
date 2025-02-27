import pandas as pd
import numpy as np

def mf_returns_calculations(df_mf, df_index):
    
    ''' Convert the date columns in both data frames to correct format in case it already isn't'''
    
    df_mf["nav_date"] = pd.to_datetime(df_mf["nav_date"], format = '%d/%m/%Y')
    df_index["Date"] = pd.to_datetime(df_index["Date"], format = '%d/%m/%Y')
    
    ''' Get a list of all the fund names''' 
    fund_names = df_mf["scheme_name"].unique()
    
    results = []
    
    ''' period_cumulative_return function calculates the cumulative return https://www.investopedia.com/terms/c/cumulativereturn.asp ) for a period of N months. 
    Inputs : 
    1. A data frame containing mf data
    2. A time period in months - if you need 5 year retuns enter 60
    3. An end date - the final date, i.e, the date of the latest available data of the fund
    4. A column name which has the NAV data
    Outputs : The cumulative return for the data for the specific period or Nan 
    '''
    def period_cumulative_return(data, return_period_in_months, end_date, nav_column_name):
                
        return_period_start_date = end_date - pd.DateOffset(months=return_period_in_months)
        
        ''' Different funds have different time since inception. It doesn't make sense to calculate the 5 year return for a fund which has existed only for 6 months. This validation ensures that only applicable returns are shown for each fund and the rest is NaN '''
        
        if data["nav_date"].min() > return_period_start_date:
            return np.nan
        
        '''To get all the nav data for your required time period using start and end dates'''
        
        data_period = data[(data["nav_date"] >= return_period_start_date) & (data["nav_date"] <= end_date)]
        
        '''Actual cumulative return calculations'''
        
        if len(data_period) > 1:
            start_value = data_period.iloc[0][nav_column_name]
            end_value = data_period.iloc[-1][nav_column_name]
            return (end_value - start_value) / start_value * 100
        
        '''For failed cases'''
        return np.nan
    
    '''Iterating through different funds'''
    for fund in fund_names : 
        fund_data = df_mf[df_mf["scheme_name"] == fund]
        return_period_start_date = fund_data["nav_date"].min()
        end_date = fund_data["nav_date"].max()
        '''Finding all time cumulative return and total days since inception'''
        start_nav = fund_data.loc[fund_data["nav_date"] == return_period_start_date, "nav"].values[0]
        end_nav = fund_data.loc[fund_data["nav_date"] == end_date, "nav"].values[0]
        mf_alltime_return = (end_nav - start_nav) / start_nav * 100
        total_days = (end_date - return_period_start_date).days
        
        '''Finding various period returns'''
        fund_3m_return = period_cumulative_return(fund_data, 3, end_date, "nav")
        fund_6m_return = period_cumulative_return(fund_data, 6, end_date, "nav")
        fund_1y_return = period_cumulative_return(fund_data, 12, end_date, "nav")
        fund_2y_return = period_cumulative_return(fund_data, 24, end_date, "nav")
        fund_3y_return = period_cumulative_return(fund_data, 36, end_date, "nav")
        fund_4y_return = period_cumulative_return(fund_data, 48, end_date, "nav")
        fund_5y_return = period_cumulative_return(fund_data, 60, end_date, "nav")

        if total_days == 0:
            results.append({
                "Fund Name": fund,
                "All-time Return (%)": mf_alltime_return,
                "Index All-time Return (%)": np.nan,
                "All-time Annualized Return (%)": np.nan,
                "Index All-time Annualized Return (%)": np.nan,
                "Excess Return (%)": np.nan,
                "Duration (Days)": total_days,
                "3M Fund Return (%)": np.nan,
                "6M Fund Return (%)": np.nan,
                "1Y Fund Return (%)": np.nan,
                "2Y Fund Return (%)": np.nan,
                "3Y Fund Return (%)": np.nan,
                "4Y Fund Return (%)": np.nan,
                "5Y Fund Return (%)": np.nan,
            })
            continue
        
        '''Annualising the all-time returns returns : https://www.investopedia.com/terms/a/annualized-total-return.asp '''
        
        mf_annualised_alltime_return = ((1 + (mf_alltime_return) / 100)**(365/total_days)-1)*100
        
        '''Fetching index data for the same dates of the fund's - Date matching'''
        index_data = df_index[(df_index["Date"] >= return_period_start_date) & (df_index["Date"] <= end_date)]
        
        if index_data.empty:
            index_alltime_return = np.nan
            index_annualized_alltime_return = np.nan
            excess_annualised_alltime_return = np.nan
        else:
            start_index = index_data.iloc[0]["Close"]
            end_index = index_data.iloc[-1]["Close"]

            index_alltime_return = (end_index - start_index) / start_index * 100
            index_annualized_alltime_return = ((1 + (index_alltime_return / 100)) ** (365 / total_days) - 1) * 100
            excess_annualised_alltime_return = mf_annualised_alltime_return - index_annualized_alltime_return
        
        results.append({
            "Fund Name": fund,
        "All-time Return (%)": mf_alltime_return,
        "Index All-time Return (%)": index_alltime_return,
        "All-time Annualized Return (%)": mf_annualised_alltime_return,
        "Index All-time Annualized Return (%)": index_annualized_alltime_return,
        "Excess Return (%)": excess_annualised_alltime_return,
        "Duration (Days)": total_days,
        "3M Fund Return (%)": fund_3m_return,
        "6M Fund Return (%)": fund_6m_return,
        "1Y Fund Return (%)": fund_1y_return,
        "2Y Fund Return (%)": fund_2y_return,
        "3Y Fund Return (%)": fund_3y_return,
        "4Y Fund Return (%)": fund_4y_return,
        "5Y Fund Return (%)": fund_5y_return,
        })
    
    results_df = pd.DataFrame(results)
    return results_df