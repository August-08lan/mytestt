import streamlit as st
import time

# 设置页面标题
st.title("简易音乐播放器")

# 初始化会话状态
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
