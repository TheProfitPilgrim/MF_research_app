import pandas as pd
import numpy as np

df = pd.read_csv('Data\\Input\\mf_eom.csv')
df_in = pd.read_csv('Data\\Input\\nifty_eom.csv')

df_in['Date'] = pd.to_datetime(df_in['Date'])
df['nav_date'] = pd.to_datetime(df['nav_date'])

fund_names = df['scheme_name'].unique()

results = []

def calculate_absolute_return(data, period_months, end_date, value_column):
    start_date = end_date - pd.DateOffset(months=period_months)

    # Ensure fund has existed for at least 'period_months'
    if data['nav_date'].min() > start_date:
        return np.nan  # Not enough data to compute this return

    data_period = data[(data['nav_date'] >= start_date) & (data['nav_date'] <= end_date)]

    if len(data_period) > 1:
        start_value = data_period.iloc[0][value_column]
        end_value = data_period.iloc[-1][value_column]
        return (end_value - start_value) / start_value * 100

    return np.nan

for fund in fund_names:
    fund_data = df[df['scheme_name'] == fund]

    start_date = fund_data['nav_date'].min()
    end_date = fund_data['nav_date'].max()
    start_nav = fund_data.loc[fund_data['nav_date'] == start_date, 'nav'].values[0]
    end_nav = fund_data.loc[fund_data['nav_date'] == end_date, 'nav'].values[0]

    absolute_return = (end_nav - start_nav) / start_nav * 100
    days_held = (end_date - start_date).days

    fund_3m_return = calculate_absolute_return(fund_data, 3, end_date, 'nav')
    fund_6m_return = calculate_absolute_return(fund_data, 6, end_date, 'nav')
    fund_1y_return = calculate_absolute_return(fund_data, 12, end_date, 'nav')
    fund_2y_return = calculate_absolute_return(fund_data, 24, end_date, 'nav')
    fund_3y_return = calculate_absolute_return(fund_data, 36, end_date, 'nav')
    fund_4y_return = calculate_absolute_return(fund_data, 48, end_date, 'nav')
    fund_5y_return = calculate_absolute_return(fund_data, 60, end_date, 'nav')

    if days_held == 0:
        results.append({
            'Fund Name': fund,
            'Absolute Return (%)': absolute_return,
            'Index Return (%)': np.nan,
            'MF Annualized Return (%)': np.nan,
            'Index Annualized Return (%)': np.nan,
            'Excess Return (%)': np.nan,
            'Duration (Days)': days_held,
            '3M Fund Return (%)': np.nan,
            '6M Fund Return (%)': np.nan,
            '1Y Fund Return (%)': np.nan,
            '2Y Fund Return (%)': np.nan,
            '3Y Fund Return (%)': np.nan,
            '4Y Fund Return (%)': np.nan,
            '5Y Fund Return (%)': np.nan,
        })
        continue

    mf_annualized_return = ((1 + (absolute_return / 100)) ** (365 / days_held) - 1) * 100

    index_data = df_in[(df_in['Date'] >= start_date) & (df_in['Date'] <= end_date)]

    if index_data.empty:
        index_return = np.nan
        index_annualized_return = np.nan
        excess_return = np.nan
    else:
        start_index = index_data.loc[index_data['Date'] == start_date, 'Close'].values[0]
        end_index = index_data.loc[index_data['Date'] == end_date, 'Close'].values[0]

        index_return = (end_index - start_index) / start_index * 100
        index_annualized_return = ((1 + (index_return / 100)) ** (365 / days_held) - 1) * 100
        excess_return = mf_annualized_return - index_annualized_return

    results.append({
        'Fund Name': fund,
        'Absolute Return (%)': absolute_return,
        'Index Return (%)': index_return,
        'MF Annualized Return (%)': mf_annualized_return,
        'Index Annualized Return (%)': index_annualized_return,
        'Excess Return (%)': excess_return,
        'Duration (Days)': days_held,
        '3M Fund Return (%)': fund_3m_return,
        '6M Fund Return (%)': fund_6m_return,
        '1Y Fund Return (%)': fund_1y_return,
        '2Y Fund Return (%)': fund_2y_return,
        '3Y Fund Return (%)': fund_3y_return,
        '4Y Fund Return (%)': fund_4y_return,
        '5Y Fund Return (%)': fund_5y_return,
    })

result_df = pd.DataFrame(results)

treynor_results = []
MAR = 0

for fund in result_df['Fund Name']:
    fund_data = df[df['scheme_name'] == fund].copy()
    start_date = fund_data['nav_date'].min()
    end_date = fund_data['nav_date'].max()
    index_data = df_in[(df_in['Date'] >= start_date) & (df_in['Date'] <= end_date)].copy()

    if len(fund_data) > 1 and len(index_data) > 1:
        fund_data['monthly_return'] = fund_data['nav'].pct_change() * 100
        index_data['monthly_return'] = index_data['Close'].pct_change() * 100

        downside_volatility = np.std(np.minimum(0, MAR - fund_data['monthly_return']))
        downside_deviation = np.sqrt(np.mean(np.square(np.minimum(0, MAR - fund_data['monthly_return']))))

        annualized_excess_return = result_df.loc[result_df['Fund Name'] == fund, 'Excess Return (%)'].values[0]

        if downside_deviation != 0:
            sortino_ratio = annualized_excess_return / downside_deviation
        else:
            sortino_ratio = np.nan

        covariance = np.cov(fund_data['monthly_return'].dropna(), index_data['monthly_return'].dropna())[0, 1]
        variance = np.var(index_data['monthly_return'].dropna())

        if variance != 0:
            beta = covariance / variance
        else:
            beta = np.nan

        if beta != 0:
            treynor_ratio = annualized_excess_return / beta
        else:
            treynor_ratio = np.nan

        treynor_results.append({
            'Fund Name': fund,
            'Downside Volatility (%)': downside_volatility,
            'Sortino Ratio': sortino_ratio,
            'MF Beta': beta,
            'Treynor Ratio': treynor_ratio
        })
    else:
        treynor_results.append({
            'Fund Name': fund,
            'Downside Volatility (%)': np.nan,
            'Sortino Ratio': np.nan,
            'MF Beta': np.nan,
            'Treynor Ratio': np.nan
        })

MF_Sortino_Treynor_df = pd.DataFrame(treynor_results)

MF_calc = pd.merge(result_df, MF_Sortino_Treynor_df, on='Fund Name')

MF_calc.to_csv('Data\\Output\\MF_calc_current.csv', index=False)

# NIFTY RETURNS CALCULATIONS

df_in_index = pd.read_csv('Data\\Input\\nifty_eom.csv')

df_in_index['Date'] = pd.to_datetime(df_in_index['Date'])

nifty_returns = {
    'Period': ['3 Months', '6 Months', '1 Year', '2 Years', '3 Years', '4 Years', '5 Years'],
    'Nifty Return (%)': []
}

periods = {
    '3 Months': 90, '6 Months': 180, '1 Year': 365, '2 Years': 730,
    '3 Years': 1095, '4 Years': 1460, '5 Years': 1825
}

df_in_index = df_in_index.sort_values(by='Date').reset_index(drop=True)

latest_date = df_in_index['Date'].max()

for period_name, days in periods.items():
    target_start_date = latest_date - pd.Timedelta(days=days)

    start_data = df_in_index[df_in_index['Date'] <= target_start_date]

    if not start_data.empty:
        start_value = start_data.iloc[-1]['Close']
        end_value = df_in_index[df_in_index['Date'] == latest_date]['Close'].values[0]

        return_percentage = ((end_value - start_value) / start_value) * 100
    else:
        return_percentage = np.nan

    nifty_returns['Nifty Return (%)'].append(return_percentage)

nifty_returns_df = pd.DataFrame(nifty_returns)

nifty_returns_df.to_csv('Data\\Output\\Nifty_Returns_current.csv', index=False)