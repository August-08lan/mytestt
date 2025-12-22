import streamlit as st

# 页面基础配置
st.set_page_config(page_title="相册网站", page_icon="🐾", layout="centered")

# 相册数据（可扩展）
image_data = [
    {
        'url': "D:/streamlit_env/1.jpeg",
        'text': "鱼"
    },
    {
        'url': "D:/streamlit_env/2.jpg",
        'text': "鸟"
    },
    {
        'url': "D:/streamlit_env/3.jpeg",
        'text': "猫"
    }
]

# 初始化会话状态（当前图片索引）
if 'ind' not in st.session_state:
    st.session_state['ind'] = 0

# 计算总图片数
total_images = len(image_data)

# 定义按钮点击逻辑（处理边界，避免索引越界）
def prev_img():
    """上一张：索引减1，边界处理（0→最后一张）"""
    st.session_state['ind'] = (st.session_state['ind'] - 1) % total_images

def next_img():
    """下一张：索引加1，边界处理（最后一张→0）"""
    st.session_state['ind'] = (st.session_state['ind'] + 1) % total_images

# 展示当前图片（居中+自适应宽度）
st.image(
    image_data[st.session_state['ind']]['url'],
    caption=image_data[st.session_state['ind']]['text'],
    use_column_width=True  # 自适应列宽度，体验更好
)

# 展示页码提示（提升体验）
st.caption(f"当前：第 {st.session_state['ind'] + 1} 张 / 总 {total_images} 张")

# 按钮布局（2列，宽度自适应）
col1, col2 = st.columns(2)
with col1:
    st.button("上一张", on_click=prev_img, use_container_width=True)
with col2:
    st.button("下一张", on_click=next_img, use_container_width=True)
