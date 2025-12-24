import streamlit as st

# 设置页面
st.set_page_config(
    page_title="还珠格格第一部",
    page_icon="▶️",
    layout="centered"
)

# 黑色背景
st.markdown("""
<style>
    body, .stApp { background-color: #000000; }
</style>
""", unsafe_allow_html=True)

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
