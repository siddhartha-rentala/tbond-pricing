import pandas as pd
import numpy as np
import math as math
import datetime as dt


"""
    The inputs for a treasury bond are:
    1. Par Value - here it will be $1000 for a treasury bond
    2. Coupon rate - annual interest rate paid by the bond (here it needs to be semiannual)
    3. Maturity Date
    4. Coupon frequency
    5. Valuation date
    6. YTM
    7. Market Price
    8. Time to maturity
"""
def bond_price(valuation_date, maturity_date, coupon_rate, coupon_freq, par_value, discount_rate):

    date_format = "%m/%d/%Y"

    valuation_date = dt.datetime.strptime(valuation_date, date_format).date()
    maturity_date = dt.datetime.strptime(maturity_date, date_format).date()
    difference = maturity_date - valuation_date
    days_until_maturity = difference.days
    yrs_until_maturity = days_until_maturity / 365

    period = yrs_until_maturity * 2 # This is because it is a semiannual coupon bond
    
    price = 0
    
    duration = 0 
    for t in range (1, int(period)+1):
        coupon_payment = coupon_rate*par_value
        discount_factor = 1/((1+discount_rate)**t)
        price = (1-discount_factor)*coupon_payment
    
    price += par_value / ((1 + discount_rate / coupon_freq) ** int(period))

    return price

    
def duration(valuation_date, maturity_date, coupon_rate, coupon_freq, par_value, discount_rate):
    npv = 0
    duration = 0
    
    date_format = "%m/%d/%Y"
    valuation_date = dt.datetime.strptime(valuation_date, date_format).date()
    maturity_date = dt.datetime.strptime(maturity_date, date_format).date()
    
    difference = maturity_date - valuation_date
    yrs_until_maturity = difference.days / 365

    period = yrs_until_maturity * 2
    for t in range(1, int(period) + 1):
        coupon_payment = coupon_rate * par_value / coupon_freq
        
        discount_factor = (1 + discount_rate / coupon_freq) ** t
        period = yrs_until_maturity * 2 # This is because it is a semiannual coupon bond

        npv += coupon_payment / discount_factor

        # Components of Macaulay duration calculation       
        coupon_payment = coupon_rate * par_value / coupon_freq
        discount_factor = ((1 + discount_rate / coupon_freq) ** t)
        discounted_cash_flow = coupon_payment / discount_factor
        
        duration += t * discounted_cash_flow / coupon_freq
        
    final_period = int(period)

    duration += final_period * (par_value / ((1 + discount_rate / coupon_freq) ** final_period)) / coupon_freq
    
    return duration

dtr_df = pd.read_csv(r'C:\Users\rensi\Desktop\Siddhartha Folder\Fordham University\Semester 1\QFGB 8946 Financial Markets and Modeling\Homework\HW4\daily-treasury-rates.csv')

dtr_df['Date'] = pd.to_datetime(dtr_df['Date'], format='%m/%d/%Y')


def string_to_float(series):
    return pd.to_numeric(series, errors='coerce')

# Create a new DataFrame by making a deep copy of dtr_df - idea is to manipulate the shape of dtr_df without changing the original as 
# it is useful later
dtr_df1 = dtr_df.copy(deep=True)

dtr_df1.iloc[:, 1:] = dtr_df1.iloc[:, 1:].apply(string_to_float)
dtr_dict = dict(zip(dtr_df1.columns, dtr_df1.T.values.tolist()))
dtr_df1.iloc[:, 1:] = dtr_df1.iloc[:, 1:].diff()

min_max = dtr_df1.iloc[:, 1:].agg(['min', 'max']) 
pctiles = dtr_df1.iloc[:, 1:].quantile([0.01, 0.05, 0.95, 0.99])
print("Changes in the interest rate: \n", dtr_df1, '\n\n')
print(min_max, '\n', pctiles)


tenors = ["2 Yr", "3 Yr", "5 Yr", "7 Yr", "10 Yr", "20 Yr", "30 Yr"]
rates = [dtr_df.iloc[-1][tenor] for tenor in tenors]  


# Parameters
date_format = "%m/%d/%Y"
valuation_date = "09/27/2023"
par_value = 1000  
coupon_rate = 0.03  
coupon_freq = 2  
period = 0
valuation_date = dt.datetime.strptime(valuation_date, date_format).date()

bond_prices = []
bond_durations = []

for tenor, rate in zip(tenors, rates):
    maturity_years = int(tenor.split()[0])  
    maturity_date = (valuation_date + dt.timedelta(days=365 * maturity_years)).strftime("%m/%d/%Y")
    
    # Finding bond price and duration
    price = bond_price(valuation_date.strftime(date_format), maturity_date, coupon_rate, coupon_freq, par_value, rate / 100)
    dur = duration(valuation_date.strftime(date_format), maturity_date, coupon_rate, coupon_freq, par_value, rate / 100)

    bond_prices.append((tenor, price))
    bond_durations.append((tenor, dur))

print("Bond Prices:", bond_prices)
print("Bond Durations:", bond_durations)




rate_changes = {
    "2 Yr": 0.005, "3 Yr": 0.010, "5 Yr": 0.015,"7 Yr": 0.020, "10 Yr": 0.025, "20 Yr": 0.030, "30 Yr": 0.030   
}

diff_bond_prices = []

for tenor, rate in zip(tenors, rates):
    maturity_years = int(tenor.split()[0])  
    maturity_date = (dt.datetime.strptime(valuation_date.strftime(date_format), "%m/%d/%Y") + dt.timedelta(days=365 * maturity_years)).strftime("%m/%d/%Y")
    # the maturity date code is basically

    # Bond price at initial t
    initial_price = bond_price(valuation_date.strftime(date_format), maturity_date, coupon_rate, coupon_freq, par_value, rate / 100)
    
    rate_change = rate_changes.get(tenor, 0)  
    new_rate = rate + rate_change * 100  
    new_price = bond_price(valuation_date.strftime(date_format), maturity_date, coupon_rate, coupon_freq, par_value, new_rate / 100)
    
    price_difference = new_price - initial_price
    diff_bond_prices.append((tenor, price_difference))

print("The change in the bond price because of rate changes are:", diff_bond_prices)



bond_hld_df = pd.read_csv(r'C:\Users\rensi\Desktop\Siddhartha Folder\Fordham University\Semester 1\QFGB 8946 Financial Markets and Modeling\Homework\HW4\TreasuryBondHoldings.csv')

pctile_rate_change = {
    '2 Yr': -0.05, '3 Yr': -0.06, '5 Yr': -0.07, '7 Yr': -0.08, 
    '10 Yr': -0.09, '20 Yr': -0.10, '30 Yr': -0.12
}

def tenor_value(tenor_years): 
    if tenor_years == 2:
        return '2 Yr'
    elif tenor_years == 3:
        return '3 Yr'
    elif tenor_years == 5:
        return '5 Yr'
    elif tenor_years == 7:
        return '7 Yr'
    elif tenor_years == 10:
        return '10 Yr'
    elif tenor_years == 20:
        return '20 Yr'
    elif tenor_years == 30:
        return '30 Yr'
    return None

def diff_bond_price(par_notional, rate_change):
    return par_notional * 100 * (rate_change / 100)  

bond_hld_df['Haircut'] = 0.0
for i, row in bond_hld_df.iterrows():
    tenor_years = row['Tenor(Y)']
    par_notional = row['ParNotional($mm)']
    
    tenor_key = tenor_value(tenor_years)
    
    if tenor_key:
        rate_change = pctile_rate_change.get(tenor_key, 0)
        haircut = diff_bond_price(par_notional, rate_change)
        bond_hld_df.at[i, 'Haircut'] = haircut

total_haircut = bond_hld_df['Haircut'].sum()
print(f"The total haircut to the portfolio is: ", total_haircut)

