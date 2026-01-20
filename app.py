import streamlit as st
import time
import os
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語小教室 - Unit 3", 
    page_icon="🧧", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 極致美化 (喜氣洋洋主題) ---
st.markdown("""
    <style>
    /* 全局背景：溫暖的宣紙色 */
    .stApp { background-color: #FFF5F2; }
    
    .block-container { padding-top: 2rem !important; padding-bottom: 5rem !important; }
    
    /* 標題漸層：紅金配色 */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        background: -webkit-linear-gradient(45deg, #D32F2F, #FFC107);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important;
        text-align: center;
        padding-bottom: 10px;
    }
    
    /* 按鈕：像紅包一樣，紅底金字 */
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        font-size: 18px;
        font-weight: 700;
        background: linear-gradient(135deg, #E53935 0%, #C62828 100%);
        color: #FFEB3B;
        border: 2px solid #FFC107;
        padding: 15px 0px;
        box-shadow: 0px 5px 15px rgba(211, 47, 47, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0px 8px 20px rgba(211, 47, 47, 0.6);
        background: linear-gradient(135deg, #FF5252 0%, #D32F2F 100%);
    }
    
    /* 卡片設計：白底紅框 */
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 20px;
        border: 2px solid #FFCDD2;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        border-color: #E53935;
        box-shadow: 0 15px 30px rgba(229, 57, 53, 0.2);
    }
    
    .big-font {
        font-size: 32px !important;
        font-weight: 800;
        color: #C62828; /* 深紅色字體 */
        margin: 10px 0;
        letter-spacing: 1px;
    }
    .med-font {
        font-size: 18px !important;
        color: #888;
        font-weight: 500;
        margin-bottom: 15px;
    }
    .emoji-icon {
        font-size: 55px;
        margin-bottom: 5px;
        filter: drop-shadow(0 3px 5px rgba(0,0,0,0.1));
    }
    
    /* 講師資訊框：金黃色系 */
    .instructor-box {
        text-align: center;
        color: #8D6E63;
        font-size: 14px;
        background: linear-gradient(to right, #FFF8E1, #FFECB3);
        padding: 8px 20px;
        border-radius: 20px;
        display: inline-block;
        margin: 0 auto 25px auto;
        border: 1px solid #FFE082;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tab 標籤頁設計 */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #fff;
        border-radius: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        padding: 10px 20px;
        font-weight: 600;
        color: #555;
    }
    .stTabs [aria-selected="true"] {
        background-color: #E53935 !important; /* 選中變紅色 */
        color: #FFEB3B !important; /* 金字 */
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 數據結構 ---
# 選出三個核心單字 + 一句祝福語
VOCABULARY = {
    "Payso":    {"zh": "錢", "emoji": "💰", "action": "做出數錢的手勢", "file": "Payso"},
    "Fangcal":  {"zh": "漂亮/好", "emoji": "✨", "action": "雙手比讚", "file": "Fangcal"},
    "Lipahak":  {"zh": "快樂", "emoji": "😄", "action": "開心地拍手", "file": "Lipahak"}
}

SENTENCES = [
    {
        "amis": "Nanay lipahak ko fa'elohay a mihecaan.", 
        "zh": "祝你新年快樂。", 
        "file": "sentence_newyear"
    }
]

# --- 1.5 智慧語音核心 ---
def play_audio(text, filename_base=None):
    if filename_base:
        path_m4a = f"audio/{filename_base}.m4a"
        if os.path.exists(path_m4a):
            st.audio(path_m4a, format='audio/mp4')
            return
        path_mp3 = f"audio/{filename_base}.mp3"
        if os.path.exists(path_mp3):
            st.audio(path_mp3, format='audio/mp3')
            return
        st.error(f"⚠️ 找不到音檔：audio/{filename_base}.m4a")

    try:
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
    except:
        st.caption("🔇")

# --- 2. 狀態管理 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0

# --- 3. 介面邏輯 ---

def show_learning_mode():
    st.markdown("""
        <div style='text-align: center; margin-bottom: 25px;'>
            <h2 style='color: #C62828; font-size: 28px; margin: 0;'>Tangsol si Payso</h2>
            <div style='color: #FF8F00; font-size: 18px; font-weight: 400; letter-spacing: 2px; margin-top: 5px;'>
                — 馬上有錢・新年快樂 —
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("💡 點擊播放按鈕，跟著伊莉絲老師一起唸！")
    
    col1, col2 = st.columns(2)
    words = list(VOCABULARY.items())
    
    for idx, (amis, data) in enumerate(words):
        with (col1 if idx % 2 == 0 else col2):
            st.markdown(f"""
            <div class="card">
                <div class="emoji-icon">{data['emoji']}</div>
                <div class="big-font">{amis}</div>
                <div class="med-font">{data['zh']}</div>
                <div style="color: #C62828; font-size: 13px; font-weight:bold; background: #FFEBEE; padding: 4px 10px; border-radius: 10px; display:inline-block;">
                    {data['action']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            play_audio(amis, filename_base=data.get('file'))

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🗣️ 句型練習")
    
    s1 = SENTENCES[0]
    
    # 句型卡片：金黃色背景，象徵富貴
    st.markdown(f"""
    <div class="card" style="background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%); border: 2px solid #FFC107;">
        <div style="font-size: 20px; font-weight:900; color:#D84315; margin-bottom: 8px; text-shadow: 1px 1px 0px #fff;">
            {s1['amis']}
        </div>
        <div style="color:#8D6E63; font-size: 18px;">{s1['zh']}</div>
    </div>
    """, unsafe_allow_html=True)
    play_audio(s1['amis'], filename_base=s1.get('file')) 

def show_quiz_mode():
    st.markdown("<h3 style='text-align: center; color: #D32F2F; margin-bottom: 20px;'>🏆 小勇士挑戰</h3>", unsafe_allow_html=True)
    
    st.progress(st.session_state.current_q / 3)
    st.write("") 

    if st.session_state.current_q == 0:
        # Q1: 聽力測驗 (錢)
        st.markdown("**第 1 關：大家最喜歡的東西！**")
        st.markdown("請聽音檔，選出正確的意思：")
        play_audio("Payso", filename_base="Payso")
        
        st.write("")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("✨ 漂亮"): st.error("那是 Fangcal 喔！")
        with c2:
            if st.button("💰 錢"):
                st.balloons()
                st.success("答對了！馬上有錢！")
                time.sleep(1.0)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c3:
            if st.button("😄 快樂"): st.error("那是 Lipahak 喔！")

    elif st.session_state.current_q == 1:
        # Q2: 填空 (新年快樂)
        st.markdown("**第 2 關：新年祝福**")
        st.markdown("請完成句子：")
        st.markdown("""
        <div style="background:#fff; padding:15px; border-radius:10px; border-left: 5px solid #D32F2F; margin: 10px 0;">
            <span style="font-size:18px;">Nanay <b>_______</b> ko fa'elohay a mihecaan.</span>
            <br><span style="color:#999; font-size:14px;">(祝你新年快樂)</span>
        </div>
        """, unsafe_allow_html=True)
        
        play_audio("Nanay lipahak ko fa'elohay a mihecaan", filename_base="sentence_newyear")
        
        options = ["Lipahak (快樂)", "Payso (錢)", "Tayal (工作)"]
        choice = st.radio("請選擇正確的單字：", options)
        
        st.write("")
        if st.button("✅ 確定送出"):
            if "Lipahak" in choice:
                st.success("太棒了！新年快樂！")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.error("再試一次！提示：我們在說快樂喔")

    elif st.session_state.current_q == 2:
        # Q3: 意思測驗 (漂亮/好)
        st.markdown("**第 3 關：稱讚別人**")
        st.markdown("如果你覺得這件事情 **很棒、很好**，阿美語怎麼說？")
        
        if st.button("Fangcal! (好/漂亮)"):
            st.snow()
            st.success("沒錯！O maan sa'eto fangcal (樣樣都好)！")
            time.sleep(1.5)
            st.session_state.score += 100
            st.session_state.current_q += 1
            st.rerun()
        if st.button("Takola! (青蛙)"): st.error("那是青蛙啦！")
        if st.button("Mata! (眼睛)"): st.error("那是眼睛喔！")

    else:
        # 結算卡片
        st.markdown(f"""
        <div class="card" style="background: linear-gradient(180deg, #FFEBEE 0%, #FFCDD2 100%); border: 2px solid #D32F2F;">
            <h1 style="margin-bottom:0;">🎉 挑戰完成！</h1>
            <h2 style="color: #D32F2F; margin-top:0;">得分：{st.session_state.score}</h2>
            <hr style="border-top: 1px dashed #D32F2F;">
            <p style="font-size: 20px; color: #555;">Tangsol si payso! 💰</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再玩一次"):
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.rerun()

# --- 4. 主程式入口 ---
st.title("阿美語小教室 🧧")

st.markdown("""
    <div style="text-align: center;">
        <span class="instructor-box">
            講師：伊莉絲 &nbsp;|&nbsp; 教材提供者：伊莉絲
        </span>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📖 學習單詞", "🎮 練習挑戰"])

with tab1:
    show_learning_mode()

with tab2:
    show_quiz_mode()
