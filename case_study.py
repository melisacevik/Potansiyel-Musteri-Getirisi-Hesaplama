import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)

     ###################################### GÖREV 1 #####################################

#Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.

df = pd.read_csv("datasets/persona.csv")


#Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
df.nunique()

#Soru 3:Kaç unique PRICE vardır?
df["PRICE"].nunique() #6 tane eşsiz değer var.

#Soru 4:Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
print("PRICE sütununun frekansları:")
print(df["PRICE"].value_counts())
print("\n")

#Soru 5:Hangi ülkeden kaçar tane satış olmuş?
df["COUNTRY"].value_counts()

# Tüm kolonların sayıları için fonksiyon

for col in df.columns:
    print(f"{col} sütununun frekansları:")
    print(df[col].value_counts())
    print("\n")

# frekans ve oranlar için fonksiyon
def col_frequency_ratio(dataframe, col_name):
    value_counts = dataframe[col_name].value_counts()
    ratios = value_counts / len(dataframe[col_name]) * 100

    total_count = value_counts.sum()
    total_ratio = ratios.sum()

    result_df = pd.DataFrame({ col_name : value_counts,
                               "Ratio" : ratios})

   # result_df.loc["Total"] = [total_count, total_ratio]

    return result_df


result_source = col_frequency_ratio(df,"SOURCE")
result_country = col_frequency_ratio(df,"COUNTRY")

print(result_source)
print(result_country)

#Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?

df.groupby("COUNTRY")["PRICE"].sum()


# Toplamları için Fonksiyon hali!
def total_earnings_by_col_name(dataframe,group_col_name, col_name):
        total_earnings = dataframe.groupby(group_col_name)[col_name].sum()
        return total_earnings

total_earnings_by_country = total_earnings_by_col_name(df, "COUNTRY","PRICE")

#Soru 7: SOURCE türlerine göre satış sayıları nedir?
df.groupby(["SOURCE", "COUNTRY"]).size()

# Soru 8:Ülkelere göre PRICE ortalamaları nedir?

df.groupby("COUNTRY")["PRICE"].mean()

# Soru 9:SOURCE'lara göre PRICE ortalamaları nedir?

df.groupby("SOURCE")["PRICE"].mean()

# ORTALAMALARI için function
def col_groupcol_col(dataframe,group_col,col):
    col_price_mean = dataframe.groupby(group_col)[col].mean()
    return col_price_mean

country_price_mean = col_groupcol_col(df, "COUNTRY", "PRICE")

# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?

df.groupby(["COUNTRY","SOURCE"])["PRICE"].mean()

    ###################################### GÖREV 2 #####################################
#Görev2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
#1. çözüm
df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"])["PRICE"].mean()
#2. çözüm
df.groupby(['COUNTRY', 'SOURCE', 'SEX', 'AGE'], as_index=False)['PRICE'].mean()

   ###################################### GÖREV 3 #####################################
#Görev 3:  Çıktıyı PRICE’a göre sıralayınız.

agg_df = df.groupby(["COUNTRY","SOURCE","SEX","AGE"])["PRICE"].mean()
agg_df.sort_values(ascending=False)

###################################### GÖREV 4 #####################################
#Görev 4:  Indekste yer alan isimleri değişken ismine çeviriniz.

agg_df = agg_df.reset_index()

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

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
print(agg_df)

agg_df.groupby("SEGMENT").agg({"PRICE": ["mean", "max", "sum"]})

#Görev 8:  Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini  tahmin ediniz

agg_df[agg_df['customer_level_based'].str.contains("TUR_ANDROID_FEMALE_31_40")]['PRICE'].mean()
agg_df[agg_df['customer_level_based'].str.contains("FRA_IOS_FEMALE_31_40")]['PRICE'].mean()
agg_df[agg_df['customer_level_based'].str.contains("USA_IOS_MALE_41_46")]['PRICE'].mean()

