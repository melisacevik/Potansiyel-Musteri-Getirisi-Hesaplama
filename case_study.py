import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)

     ###################################### GÖREV 1 #####################################

# Soru 1:
df = pd.read_csv("datasets/persona.csv")

# Soru 2 + Soru 3 + Soru 4 + Soru 5

df["SOURCE"].unique()
def col_frequency_ratio(dataframe, col_name):
    value_counts = dataframe[col_name].value_counts()
    ratios = value_counts / len(dataframe[col_name]) * 100

    total_count = value_counts.sum()
    total_ratio = ratios.sum()

    result_df = pd.DataFrame({ col_name : value_counts, "Ratio" : ratios})
    result_df.loc["Total"] = [total_count, total_ratio]

    return result_df


result_source = col_frequency_ratio(df,"SOURCE")
result_price = col_frequency_ratio(df,"PRICE")
result_country = col_frequency_ratio(df,"COUNTRY")

print(result_source)
print(result_price)
print(result_country)

# Soru 6

country_total_price = df.groupby(["PRICE", "COUNTRY"]).size().reset_index(name='Sales_Count')

country_total_price['Total_Price'] = country_total_price['PRICE'] * country_total_price['Sales_Count']

total_earnings_by_country = country_total_price.groupby("COUNTRY")["Total_Price"].sum().reset_index(name='Total_Earnings')

def total_earnings_by_col_name(dataframe,group_col_name, col_name):
    col_total_price = dataframe.groupby([group_col_name, col_name]).size().reset_index(name='Sales_Count')
    col_total_price['Total_Price'] = col_total_price[group_col_name] * col_total_price['Sales_Count']
    total_earnings = col_total_price.groupby(group_col_name)["Total_Price"].sum().reset_index(name=f'{col_name}_Total_Earnings')

    return total_earnings

total_earnings_by_country = total_earnings_by_col_name(df, "PRICE","COUNTRY")

# Soru 7
source_total_count = df.groupby(["SOURCE", "COUNTRY"]).size().reset_index(name='Sales_Count')

# Soru 8 + Soru 9

country_price_mean = df.groupby("COUNTRY")["PRICE"].mean().reset_index(name="Price_Mean")
source_price_mean = df.groupby("SOURCE")["PRICE"].mean().reset_index(name="Source_Mean")

# function
def col_groupcol_col(dataframe,group_col,col):
    col_price_mean = dataframe.groupby(group_col)[col].mean()
    return col_price_mean

country_price_mean = col_groupcol_col(df, "COUNTRY", "PRICE")

# Soru 10

pivot_table = pd.pivot_table(df, values='PRICE', index='COUNTRY', columns='SOURCE', aggfunc='mean', fill_value=0).reset_index()
print(pivot_table)

    ###################################### GÖREV 2 #####################################

average_gains = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg(PRICE=('PRICE', 'mean'))

   ###################################### GÖREV 3 #####################################

agg_df = average_gains.sort_values(by="PRICE", ascending=False).reset_index()

###################################### GÖREV 4 #####################################

df.set_index('AGE', inplace=True)

df = df.rename_axis("AGE").reset_index()


###################################### GÖREV 5 #####################################

# pd.cut ile özel aralıklar belirlenir.

bins = [0, 18, 23, 30, 40, 66]
labels = ['0_18', '19_23', '24_30', '31_40', '41_66']
agg_df['AGE_CAT'] = pd.cut(agg_df['AGE'], bins=bins, labels=labels, right=False) # sağ sınırı kabul etme

###################################### GÖREV 6 #####################################

agg_df["customer_level_based"] = (agg_df["COUNTRY"].astype(str) + "_" +
                                  agg_df["SOURCE"].astype(str) + "_" +
                                  agg_df["SEX"].astype(str) + "_" +
                                  agg_df["AGE_CAT"].astype(str)).str.upper()

# Yeni veri çerçevesini oluşturun
customers_level_based = pd.DataFrame({
    "customer_level_based": agg_df["customer_level_based"],
    "price": agg_df["PRICE"]
})

###################################### GÖREV 7 #####################################
agg_df["PRICE"] = pd.to_numeric(agg_df["PRICE"])  # PRICE serisi sayısal veri tipine çevrildi

price_bins = [0, 10, 20, 30, 40, 50, 60]
price_labels = ['F', 'E', 'D', 'C', 'B', 'A']

agg_df['SEGMENT'] = pd.cut(agg_df['PRICE'], bins=price_bins, labels=price_labels, right=False)  # sağ sınırı kabul etme

group_with_segment = agg_df.groupby("SEGMENT")["PRICE"].agg(["mean", "std", "min", "max"])

group_with_segment.dropna()






