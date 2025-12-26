import streamlit as st
import importlib.util  # 用于动态导入子应用代码

# 初始化选中状态
if "train" not in st.session_state:
    st.session_state.train = "数字档案"

# 实训配置：改为子应用的本地文件路径（需将子应用代码下载到本地）
train_config = {
    "数字档案": {"file_path": "first.py", "desc": "数字档案"},
    "南宁美食数据仪表": {"file_path": "second.py", "desc": "南宁美食数据仪表"},
    "相册": {"file_path": "third.py", "desc": "相册"},
    "音乐播放器": {"file_path": "app.py", "desc": "音乐播放器"},
    "视频网站": {"file_path": "abc.py", "desc": "视频网站"},
    "个人档案生成器": {"file_path": "acc.py", "desc": "个人档案生成器"},
    # 其他实训项同理，需将对应的.py文件放在主应用同一目录
}

# 侧边栏导航
with st.sidebar:
    for t in train_config.keys():
        if st.button(t):
            st.session_state.train = t
            st.rerun()  # 强制刷新

# 主内容区
col1, col2 = st.columns([1, 3])

with col1:
    with st.expander(f"{st.session_state.train} 说明", expanded=True):
        st.write(train_config[st.session_state.train]["desc"])

with col2:
    # 动态导入并运行子应用代码
    try:
        target_file = train_config[st.session_state.train]["file_path"]
        # 加载子应用模块
        spec = importlib.util.spec_from_file_location("sub_app", target_file)
        sub_app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sub_app)
        # 运行子应用（需确保子应用代码是“可导入并执行”的形式）
        # 注：子应用代码中不能有独立的st.run()，直接写UI逻辑即可
    except FileNotFoundError:
        st.error(f"未找到子应用文件：{target_file}")
    except Exception as e:
        st.error(f"加载子应用失败：{str(e)}")













