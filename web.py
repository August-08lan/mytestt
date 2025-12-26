import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 页面设置
st.set_page_config(page_title="销售仪表板", layout="wide")

# 生成模拟数据
def create_sample_data():
    # 时间数据
    hours = list(range(8, 22))
    sales_per_hour = [1200, 1500, 1800, 2100, 2400, 2800, 3200, 3500, 3800, 3400, 3000, 2700, 2400, 2000]
    
    # 产品类型数据
    products = ['电子产品', '服装', '食品饮料', '家居用品', '化妆品', '图书']
    product_sales = [45000, 38000, 52000, 31000, 28000, 25000]
    
    return hours, sales_per_hour, products, product_sales

# 主应用
st.title("销售仪表板")

# 侧边栏筛选器
with st.sidebar:
    st.header("数据筛选")
    option = st.selectbox("选择区域", ["全部", "华北", "华东", "华南", "西南"])
    date_range = st.date_input("选择日期范围", [datetime.today() - timedelta(days=30), datetime.today()])
    st.button("应用筛选", type="primary")

# 三个指标卡片
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("总销售额", "¥307,587", "+12.5%")
with col2:
    st.metric("顾客评分", "7.0", "+0.3")
with col3:
    st.metric("平均客单价", "¥307.59", "+5.2%")

# 两个图表
hours, sales_per_hour, products, product_sales = create_sample_data()

col4, col5 = st.columns(2)

with col4:
    st.subheader("按小时销售统计")
    chart_data1 = pd.DataFrame({
        '小时': [f"{h}:00" for h in hours],
        '销售额': sales_per_hour
    })
    st.bar_chart(chart_data1.set_index('小时'))

with col5:
    st.subheader("按产品类型销售统计")
    chart_data2 = pd.DataFrame({
        '产品类型': products,
        '销售额': product_sales
    })
    st.bar_chart(chart_data2.set_index('产品类型'))

# 显示数据表格
st.subheader("销售数据详情")
data = {
    '订单号': [f'ORD2024{1000+i}' for i in range(10)],
    '城市': ['北京', '上海', '广州', '深圳', '杭州', '成都', '南京', '武汉', '西安', '重庆'],
    '产品类型': np.random.choice(['电子产品', '服装', '食品饮料', '家居用品'], 10),
    '销售额': np.random.randint(200, 2000, 10),
    '评分': np.round(np.random.uniform(6.0, 9.0, 10), 1)
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# 底部信息
st.markdown("---")
st.caption("销售数据仪表板 | 更新时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
