import streamlit as st
import pandas as pd
import random
import os  # 新增：用于处理文件路径

# ---------------------- 页面样式配置（深色风格贴合示例） ----------------------
st.set_page_config(
    page_title="南宁美食仪表盘",
    page_icon="🍜",
    layout="centered"
)

# 自定义深色背景样式
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: #ffffff;
    }
    .stHeader {background-color: #1e1e1e;}
    .stSelectbox label, .stSubheader {color: #ffffff;}
    .stMarkdown p, .stMarkdown li {color: #e0e0e0;}
    </style>
""", unsafe_allow_html=True)

# ---------------------- 数据准备 ----------------------
# 基础餐厅数据
restaurants_data = {
    "餐厅": ["蜜雪冰城", "沪上阿姨", "古茗", "爷爷不泡茶","伯牙绝旋"],
    "类型": ["中餐", "中餐", "快餐", "自助餐", "西餐"],
    "评分": [5.0, 4.5, 4.0, 4.7, 4.3],
    "人均消费(元)": [15, 20, 25, 35, 50],
    "latitude": [22.853838, 22.965046, 22.812200, 22.809105, 22.839699],
    "longitude": [108.222177, 108.353921, 108.266629, 108.378664, 108.245804]
}
df_restaurants = pd.DataFrame(restaurants_data)

# 12个月价格走势数据（5家餐厅，12个月）
months = [f"{i}月" for i in range(1, 13)]
price_trend = {"月份": months}
base_prices = df_restaurants["人均消费(元)"].tolist()
for i, rest in enumerate(df_restaurants["餐厅"]):
    # 生成基础价格±5%波动的月度数据
    price_trend[rest] = [round(base_prices[i] * random.uniform(0.95, 1.05), 1) for _ in range(12)]
df_price = pd.DataFrame(price_trend)

# 用餐高峰时段数据（模拟客流量）
peak_times = ["早餐", "午餐", "下午茶", "晚餐", "夜宵"]
peak_data = {"时段": peak_times}
for rest in df_restaurants["餐厅"]:
    # 午餐/晚餐设为高峰值
    peak_data[rest] = [random.randint(10,30), random.randint(80,120), random.randint(20,40), random.randint(90,130), random.randint(30,50)]
df_peak = pd.DataFrame(peak_data)

# ---------------------- 本地图片配置（关键修改） ----------------------
# 方法1：相对路径（推荐）- 将a1图片放在和本脚本同一文件夹下
# 示例：如果图片是a1.jpg，路径写 "a1.jpg"；如果是a1.png，写 "a1.png"
LOCAL_IMAGE_PATH = "a1.jpg"  # 请根据你的图片后缀修改（如.png/.jpeg）

# 方法2：绝对路径（备用，适用于图片在其他文件夹）
# Windows示例：LOCAL_IMAGE_PATH = "C:/Users/你的用户名/Desktop/a1.jpg"
# macOS/Linux示例：LOCAL_IMAGE_PATH = "/Users/你的用户名/Desktop/a1.jpg"

# 餐厅推荐菜品 - 替换为本地图片
recommend_dishes = {
    "蜜雪冰城": {"菜品": "珍珠奶茶", "图": "a1.png"},
    "沪上阿姨": {"菜品": "千目抹茶啵啵", "图": "a2.png"},  # 若每家餐厅要不同图片，可复制a1为a2/a3等，分别指定路径
    "古茗": {"菜品": "生椰抹茶米麻薯", "图": "a3.png"},
    "爷爷不泡茶": {"菜品": "白兰青提", "图": "a4.png"},
    "伯牙绝旋": {"菜品": "千山慕雪", "图":"a5.png" }
}

# 验证图片路径是否存在（可选，方便排错）
if not os.path.exists(LOCAL_IMAGE_PATH):
    st.warning(f"⚠️ 未找到本地图片：{LOCAL_IMAGE_PATH}，请检查路径是否正确！")

# ---------------------- 页面模块布局 ----------------------
st.title("🍲 南宁美食数据仪表盘")

# 1. 餐厅位置地图
st.subheader("🗺️ 餐厅地理位置")
st.map(
    df_restaurants[["latitude", "longitude", "餐厅"]],
    latitude="latitude",
    longitude="longitude",
    zoom=11,
    height=280
)

# 2. 餐厅评分柱状图
st.subheader("⭐ 餐厅评分")
st.bar_chart(
    df_restaurants,
    x="餐厅",
    y="评分",
    color="#00BFFF",
    height=250
)

# 3. 12个月价格走势折线图（5条折线）
st.subheader("📈 不同餐厅价格走势")
st.line_chart(
    df_price.set_index("月份"),
    height=250
)

# 4. 用餐高峰时段面积图
st.subheader("📊 用餐高峰时段")
st.area_chart(
    df_peak.set_index("时段"),
    height=250
)

# 5. 餐厅详情选择器
st.subheader("🏠 餐厅详情")
selected_rest = st.selectbox("选择餐厅", df_restaurants["餐厅"])
rest_detail = df_restaurants[df_restaurants["餐厅"] == selected_rest].iloc[0]
st.markdown(f"""
- 餐厅名称：{rest_detail["餐厅"]}
- 餐饮类型：{rest_detail["类型"]}
- 评分：{rest_detail["评分"]}/5.0
- 人均消费：{rest_detail["人均消费(元)"]}元
""")

# 6. 今日午餐推荐（修复弃用提示）
st.subheader("🥢 今日午餐推荐")
dish = recommend_dishes[selected_rest]
# 去掉use_column_width，仅保留width参数（或设置width="auto"自适应列宽）
st.image(dish["图"], caption=dish["菜品"], width=700)  # 可根据需求调整width数值（如500）
