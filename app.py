import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# データの読み込み
data = pd.read_csv('sales_data.csv')

# Streamlitアプリのタイトル
st.title('複数のチャートを組み合わせたダッシュボード')

# データの表示
st.subheader('データセット')
st.write(data)

# 日付ごとの売上を集計
daily_sales = data.groupby('Date').sum().reset_index()

# チャートの描画
st.subheader('日付ごとの売上')
fig, ax = plt.subplots()
sns.lineplot(data=daily_sales, x='Date', y='Sales', ax=ax)
st.pyplot(fig)

# 製品ごとの売上を集計
product_sales = data.groupby('Product').sum().reset_index()

# チャートの描画
st.subheader('製品ごとの売上')
fig, ax = plt.subplots()
sns.barplot(data=product_sales, x='Product', y='Sales', ax=ax)
st.pyplot(fig)