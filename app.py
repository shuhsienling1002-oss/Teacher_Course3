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
    
    /* 單字卡片：白底紅框 */
    .card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 15px;
        border: 2px solid #FFCDD2;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
    }
    .card:hover {
        transform: translateY(-3px);
        border-color: #E53935;
    }

    /* 句子卡片：金黃色背景，像春聯 */
    .sentence-card {
        background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        border-left: 6px solid #D32F2F; /* 左邊紅條 */
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    .big-font {
        font-size: 28px !important;
        font-weight: 800;
        color: #C62828;
        margin: 5px 0;
    }
    .med-font {
        font-size: 16px !important;
        color: #888;
        font-weight: 500;
        margin-bottom: 10px;
    }
    .emoji-icon {
        font-size: 45px;
        margin-bottom: 5px;
    }
    
    /* 講師資訊框 */
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
    
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #fff;
        border-radius: 15px;
        padding: 10px 20px;
        font-weight: 600;
        color: #555;
    }
    .stTabs [aria-selected="true"] {
        background-color: #E53935 !important;
        color: #FFEB3B !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 數據結構 (已更新標點符號) ---

# 單字表 (5個)
VOCABULARY = [
    {"amis": "Sa'eto",   "zh": "全部是/都是", "emoji": "👐", "action": "雙手畫大圓", "file": "saeto"},
    {"amis": "Fangcal",  "zh": "好/美好",     "emoji": "✨", "action": "比讚",         "file": "fangcal"},
    {"amis": "Payso",    "zh": "錢",          "emoji": "💰", "action": "數錢手勢",     "file": "payso"},
    {"amis": "Tayal",    "zh": "工作/事業",   "emoji": "💼", "action": "握拳加油",     "file": "tayal"},
    {"amis": "Lipahak",  "zh": "快樂",        "emoji": "😄", "action": "拍手笑",       "file": "lipahak"},
]

# 句子表 (5句，加上標點)
SENTENCES = [
    {"amis": "O maan sa'eto fangcal.",            "zh": "甚麼都好。",     "file": "s_omaan"},
    {"amis": "Tangsol fangcal.",                  "zh": "馬上就好。",     "file": "s_tangsol_fangcal"},
    {"amis": "Tangsol si payso.",                 "zh": "馬上有錢。",     "file": "s_tangsol_payso"},
    {"amis": "Malaheci'ay ko tayal.",             "zh": "事業成功。",     "file": "s_tayal"},
    {"amis": "Nanay lipahak ko fa'elohay a mihecaan!", "zh": "新年快樂！", "file": "s_newyear"},
]

# --- 1.5 智慧語音核心 ---
def play_audio(text, filename_base=None):
    if filename_base:
        # 優先找 m4a，再找 mp3
        for ext in ['m4a', 'mp3']:
            path = f"audio/{filename_base}.{ext}"
            if os.path.exists(path):
                st.audio(path, format=f'audio/{ext}')
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
            <h2 style='color: #C62828; font-size: 26px; margin: 0;'>Tangsol si Payso</h2>
            <div style='color: #FF8F00; font-size: 16px; margin-top: 5px;'>
                — 馬上有錢・新年快樂 —
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("💡 點擊播放按鈕，跟著伊莉絲老師一起唸！")
    
    # --- 單字區 ---
    st.markdown("### 🧧 重點單字")
    col1, col2 = st.columns(2)
    
    for idx, item in enumerate(VOCABULARY):
        with (col1 if idx % 2 == 0 else col2):
            st.markdown(f"""
            <div class="card">
                <div class="emoji-icon">{item['emoji']}</div>
                <div class="big-font" style="font-size:24px!important;">{item['amis']}</div>
                <div class="med-font">{item['zh']}</div>
                <div style="color: #C62828; font-size: 12px; background: #FFEBEE; padding: 2px 8px; border-radius: 10px; display:inline-block;">
                    {item['action']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            play_audio(item['amis'], filename_base=item['file'])

    st.markdown("---")
    
    # --- 句子區 ---
    st.markdown("### 🏮 吉祥話練習")
    
    for s in SENTENCES:
        st.markdown(f"""
        <div class="sentence-card">
            <div style="font-size: 20px; font-weight:900; color:#D84315; margin-bottom: 5px;">
                {s['amis']}
            </div>
            <div style="color:#8D6E63; font-size: 16px;">{s['zh']}</div>
        </div>
        """, unsafe_allow_html=True)
        play_audio(s['amis'], filename_base=s['file'])

def show_quiz_mode():
    st.markdown("<h3 style='text-align: center; color: #D32F2F; margin-bottom: 20px;'>🏆 新年挑戰賽</h3>", unsafe_allow_html=True)
    
    st.progress(st.session_state.current_q / 3)
    st.write("") 

    if st.session_state.current_q == 0:
        # Q1: 聽力測驗 (馬上有錢)
        st.markdown("**第 1 關：大家最喜歡的祝福！**")
        st.markdown("請聽音檔，這是什麼意思？")
        play_audio("Tangsol si payso", filename_base="s_tangsol_payso")
        
        st.write("")
        if st.button("💼 事業成功"): st.error("那是 Malaheci'ay ko tayal")
        if st.button("💰 馬上有錢"):
            st.balloons()
            st.success("答對了！Tangsol si payso！")
            time.sleep(1.0)
            st.session_state.score += 100
            st.session_state.current_q += 1
            st.rerun()
        if st.button("✨ 什麼都好"): st.error("那是 O maan sa'eto fangcal")

    elif st.session_state.current_q == 1:
        # Q2: 填空 (新年快樂)
        st.markdown("**第 2 關：新年快樂**")
        st.markdown("請完成句子：")
        st.markdown("""
        <div style="background:#fff; color:#000000; padding:15px; border-radius:10px; border-left: 5px solid #D32F2F; margin: 10px 0;">
            <span style="font-size:18px;">Nanay <b>_______</b> ko fa'elohay a mihecaan!</span>
            <br><span style="color:#999; font-size:14px;">(祝你新年快樂！)</span>
        </div>
        """, unsafe_allow_html=True)
        
        play_audio("Nanay lipahak ko fa'elohay a mihecaan", filename_base="s_newyear")
        
        options = ["Lipahak (快樂)", "Tayal (工作)", "Sa'eto (全部)"]
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
        # Q3: 單字測驗 (Fangcal)
        st.markdown("**第 3 關：美好的一天**")
        st.markdown("「美好、好」的阿美語怎麼說？")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Fangcal"):
                st.snow()
                st.success("沒錯！Fangcal 就是好！")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c2:
            if st.button("Tayal"): st.error("Tayal 是工作喔！")

    else:
        # 結算
        st.markdown(f"""
        <div class="sentence-card" style="text-align:center; border-left:none; border: 2px solid #D32F2F;">
            <h1 style="margin-bottom:0;">🎉 挑戰完成！</h1>
            <h2 style="color: #D32F2F; margin-top:0;">得分：{st.session_state.score}</h2>
            <hr style="border-top: 1px dashed #D32F2F;">
            <p style="font-size: 20px; color: #555;">Malaheci'ay ko tayal! (事業成功)</p>
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

tab1, tab2 = st.tabs(["📖 學習單詞與句子", "🎮 新年挑戰"])

with tab1:
    show_learning_mode()

with tab2:
    show_quiz_mode()

