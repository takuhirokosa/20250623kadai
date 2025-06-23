import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ページの設定
st.set_page_config(
    page_title="都道府県別売上ダッシュボード",
    page_icon="📊",
    layout="wide"
)

# タイトル
st.title("📊 都道府県別売上ダッシュボード")

# サンプルデータの作成（CSVファイルがない場合）
@st.cache_data
def load_data():
    # サンプルデータ
    data = {
        'prefecture': ['Tokyo', 'Osaka', 'Kanagawa', 'Aichi', 'Hokkaido', 'Fukuoka', 'Hyogo'],
        'sales': [300, 200, 250, 180, 220, 150, 170]
    }
    df = pd.DataFrame(data)
    return df

# データの読み込み
try:
    # CSVファイルがある場合は読み込み（複数のパスを試行）
    import os
    possible_paths = [
        'sales_data.csv',  # 現在のディレクトリ
        os.path.expanduser('~/sales_data.csv'),  # ホームディレクトリ
        './sales_data.csv'  # 相対パス
    ]
    
    df = None
    for path in possible_paths:
        try:
            df = pd.read_csv(path)
            st.success(f"✅ {path} からデータを読み込みました")
            break
        except FileNotFoundError:
            continue
    
    if df is None:
        raise FileNotFoundError("CSVファイルが見つかりません")
except FileNotFoundError:
    # CSVファイルがない場合はサンプルデータを使用
    df = load_data()
    st.info("ℹ️ CSVファイルが見つからないため、サンプルデータを使用しています")

# 売上データセクション
st.subheader("売上データ")
st.dataframe(
    df,
    use_container_width=True,
    column_config={
        "prefecture": st.column_config.TextColumn("prefecture"),
        "sales": st.column_config.NumberColumn("sales")
    },
    hide_index=True
)

# 売上でフィルタリングセクション
st.subheader("売上でフィルタリング")

# 売上の最小値と最大値を取得
min_sales = int(df['sales'].min())
max_sales = int(df['sales'].max())

# スライダーで売上の最小値を設定
min_sales_filter = st.slider(
    "",
    min_value=min_sales,
    max_value=max_sales,
    value=min_sales,
    step=10
)

# データのフィルタリング
filtered_df = df[df['sales'] >= min_sales_filter]

# フィルタリングされたデータセクション
st.subheader("フィルタリングされたデータ")
if not filtered_df.empty:
    st.dataframe(
        filtered_df,
        use_container_width=True,
        column_config={
            "prefecture": st.column_config.TextColumn("prefecture"),
            "sales": st.column_config.NumberColumn("sales")
        },
        hide_index=True
    )
else:
    st.write("表示するデータがありません")

# 売上の棒グラフセクション
st.subheader("売上の棒グラフ")

if not filtered_df.empty:
    # 棒グラフの作成
    fig = px.bar(
        filtered_df,
        x='prefecture',
        y='sales',
        title='Sales by Prefecture',
        labels={'prefecture': 'Prefecture', 'sales': 'Sales'},
        color_discrete_sequence=['#1f77b4']  # 青色で統一
    )
    
    # グラフの見た目を調整
    fig.update_layout(
        xaxis_title="Prefecture",
        yaxis_title="Sales",
        showlegend=False,
        height=500,
        title_x=0.5,  # タイトルを中央揃え
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # グラフの表示
    st.plotly_chart(fig, use_container_width=True)
    
else:
    st.warning("⚠️ 指定した条件に該当するデータがありません")