import streamlit as st
import time
import pandas as pd
import random
import os  # 新增：用于处理文件路径

st.title("选项卡实例")
tab1,tab2,tab3,tab4=st.tabs(["简易音乐播放器","小视频","个人简历生成器","南宁美食数据仪表"])

with tab1:
    st.header("这是第一个选项卡的内容") 
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False
if "progress" not in st.session_state:
    st.session_state.progress = 0

# 歌曲数据
songs = [
    {
        "title": "梦幻诛仙",
        "artist": "张碧晨",
        "duration": "4：04",
        "cover": "http://p2.music.126.net/Lerc6tdw236Nvqtf7eBOVg==/18494885091647682.jpg?param=130y130",
        "audio": "https://music.163.com/song/media/outer/url?id=438456232"
    },
    {
        "title": "一路生花",
        "artist": "温奕芯", 
        "duration": "2:46",
        "cover": "http://p2.music.126.net/3LxRV-THxeSUsTfM-F3WvQ==/109951170731176266.jpg?param=130y130",
        "audio": "https://music.163.com/song/media/outer/url?id=2695879285"
    },
    {
        "title": "解药",
        "artist": "队长",
        "duration": "3:51", 
        "cover": "http://p2.music.126.net/yxVm_vRFOode6yP67NmMcA==/109951166625738075.jpg?param=130y130",
        "audio": "https://music.163.com/song/media/outer/url?id=1895330088"
    }
]

# 切换函数
def prev_song():
    st.session_state.current_idx = (st.session_state.current_idx - 1) % len(songs)
    st.session_state.progress = 0

def next_song():
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(songs)
    st.session_state.progress = 0

# 播放控制
def toggle_play():
    st.session_state.is_playing = not st.session_state.is_playing

# 获取当前歌曲
current_song = songs[st.session_state.current_idx]

# 显示专辑封面和歌曲信息
col1, col2 = st.columns([2, 3])

with col1:
    st.image(current_song["cover"], caption="专辑封面", width=250)

with col2:
    st.markdown(f"## {current_song['title']}")
    st.markdown(f"**歌手**: {current_song['artist']}")
    st.markdown(f"**时长**: {current_song['duration']}")

# 控制按钮
col3, col4 = st.columns(2)
with col3:
    st.button("上一首", on_click=prev_song)
with col4:
    st.button("下一首", on_click=next_song)

# 播放/暂停按钮
play_text = "⏸️ 暂停" if st.session_state.is_playing else "▶️ 播放"
st.button(play_text, on_click=toggle_play)

# 进度条
st.progress(st.session_state.progress / 100)

# 时间显示
st.markdown(f"0:00 / {current_song['duration']}")

# 音频播放器
st.audio(current_song["audio"])








with tab2:
    st.header("小视频")

# 三集视频数据
videos = {
    1: {
        "title": "还珠格格第一部 - 第1集",
        "url": "https://www.w3school.com.cn/example/html5/mov_bbb.mp4"
    },
    2: {
        "title": "还珠格格第一部 - 第2集",
        "url": "https://www.w3schools.com/html/movie.mp4"
    },
    3: {
        "title": "还珠格格第一部 - 第3集",
        "url": "https://media.w3.org/2010/05/sintel/trailer.mp4"
    }
}

# 保存当前集数
if "current" not in st.session_state:
    st.session_state.current = 1

# 视频标题
st.markdown(f"""
<div style="color: white; text-align: center; font-size: 20px; font-weight: bold; margin: 10px 0;">
    {videos[st.session_state.current]["title"]}
</div>
""", unsafe_allow_html=True)

# 播放视频
st.video(videos[st.session_state.current]["url"])

# 三集选择按钮
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("第1集", use_container_width=True, type="primary" if st.session_state.current == 1 else "secondary"):
        st.session_state.current = 1
        st.rerun()

with col2:
    if st.button("第2集", use_container_width=True, type="primary" if st.session_state.current == 2 else "secondary"):
        st.session_state.current = 2
        st.rerun()

with col3:
    if st.button("第3集", use_container_width=True, type="primary" if st.session_state.current == 3 else "secondary"):
        st.session_state.current = 3
        st.rerun()


with tab3:
    st.header("个人简历生成器")
# 创建两列布局
col1, col2 = st.columns(2)

with col1:
    st.header("个人信息表单")
    
    # 基本信息
    st.subheader("基本信息")
    name = st.text_input("姓名", "兰汉三")
    position = st.text_input("职位", "学生")
    phone = st.text_input("电话", "19178270201")
    email = st.text_input("邮箱", "3418033800@qq.com")
    birth_date = st.text_input("出生日期", "2025/08/02")
    
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        gender = st.selectbox("性别", ["男", "女"], index=0)
        education = st.selectbox("学历", ["高中", "专科", "本科", "硕士", "博士"], index=2)
    
    with col1_2:
        experience = st.selectbox("工作经验", ["无经验", "1年", "2年", "3年", "4年", "5年", "6年", "7年", "8年", "9年", "10年以上"], index=6)
        expected_salary = st.text_input("期望薪资", "500-500")
    
    # 语言能力
    st.subheader("语言能力")
    languages = st.multiselect(
        "选择语言能力",
        ["中文", "英语", "日语", "韩语", "法语", "德语", "西班牙语"],
        default=["中文", "英语"]
    )
    
    # 专业技能
    st.subheader("专业技能")
    skills = st.multiselect(
        "选择专业技能",
        ["Java", "HTML/CSS", "机器学习", "Python", "JavaScript", "C++", "数据库管理", "网络工程"],
        default=["Java", "HTML/CSS", "机器学习", "Python"]
    )
    
    # 最佳联系时间
    best_time = st.text_input("最佳联系时间", "12：00")
    
    # 个人简介
    st.subheader("个人简介")
    introduction = st.text_area(
        "个人简介",
        "要啥啥不会，干饭第一名，芝士园专业干饭第一名，打游戏苟分第二名",
        height=150
    )
    
    # 座右铭
    motto = st.text_input("座右铭", "欲买桂花同载酒，终不似 少年游。")
    
    # 上传照片
    st.subheader("上传个人照片")
    uploaded_file = st.file_uploader("选择图片文件", type=['png', 'jpg', 'jpeg'])
    
    # 下载按钮
    if st.button("生成并下载简历"):
        st.success("简历已生成！下载功能将在后续版本中实现。")

with col2:
    st.header("简历实时预览")
    
    # 简历预览区域
    with st.container():
        st.markdown("---")
        
        # 简历头部信息
        col2_1, col2_2 = st.columns([1, 3])
        with col2_1:
            if uploaded_file is not None:
                st.image(uploaded_file, width=150)
            else:
                st.markdown("<div style='width:150px; height:150px; border-radius:50%; background-color:#f0f0f0; display:flex; align-items:center; justify-content:center; font-size:48px;'>👤</div>", unsafe_allow_html=True)
        
        with col2_2:
            st.markdown(f"### {name}")
            st.markdown(f"**{position}**")
            st.markdown(f"📱 {phone} | 📧 {email}")
        
        st.markdown("---")
        
        # 个人信息详情
        st.subheader("个人详情")
        col2_3, col2_4 = st.columns(2)
        with col2_3:
            st.markdown(f"**出生日期**: {birth_date}")
            st.markdown(f"**性别**: {gender}")
            st.markdown(f"**工作经验**: {experience}")
        
        with col2_4:
            st.markdown(f"**学历**: {education}")
            st.markdown(f"**期望薪资**: {expected_salary}")
            st.markdown(f"**最佳联系时间**: {best_time}")
        
        if languages:
            st.markdown(f"**语言能力**: {', '.join(languages)}")
        
        st.markdown("---")
        
        # 个人简介
        st.subheader("个人简介")
        st.write(introduction)
        
        # 专业技能
        st.subheader("专业技能")
        for skill in skills:
            st.markdown(f"- {skill}")
        
        # 座右铭
        if motto:
            st.markdown("---")
            st.markdown(f"> *{motto}*")

# 添加页脚说明
st.markdown("---")
st.caption("简历生成器 - 数据会实时更新，左侧表单修改后右侧预览将自动变化")




with tab4:
        st.header("南宁美食数据仪表盘")
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


