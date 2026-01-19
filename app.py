import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音，最接近南島語韻律
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 19: O Dikuc", page_icon="👕", layout="centered")

# --- CSS 美化 (時尚紫) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #F3E5F5 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #AB47BC;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #8E24AA; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #F3E5F5;
        border-left: 5px solid #BA68C8;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #E1BEE7; color: #4A148C; border: 2px solid #AB47BC; padding: 12px;
    }
    .stButton>button:hover { background-color: #CE93D8; border-color: #8E24AA; }
    .stProgress > div > div > div > div { background-color: #AB47BC; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 19 嚴格校對版) ---
vocab_data = [
    {"amis": "Dikuc", "chi": "衣服", "icon": "👕", "source": "Standard Dict"},
    {"amis": "Kiping", "chi": "上衣", "icon": "👚", "source": "Standard Dict"},
    {"amis": "Talaw", "chi": "褲子", "icon": "👖", "source": "Standard Dict"},
    {"amis": "Tupel", "chi": "帽子", "icon": "🧢", "source": "Standard Dict"},
    {"amis": "Cukap", "chi": "鞋子", "icon": "👟", "source": "Standard Dict"},
    {"amis": "Cidikuc", "chi": "穿著衣服 (有衣服)", "icon": "🕴️", "source": "Ci+Dikuc"},
    {"amis": "Kohecal", "chi": "白色", "icon": "⚪", "source": "Basic Colors"},
    {"amis": "Kahengang", "chi": "紅色", "icon": "🔴", "source": "Basic Colors"},
    {"amis": "Koheting", "chi": "黑色", "icon": "⚫", "source": "Basic Colors"},
    {"amis": "Fangcal", "chi": "漂亮 / 好看", "icon": "✨", "source": "Basic Adjectives"},
]

sentences = [
    {"amis": "Fangcal ko dikuc no miso.", "chi": "你的衣服很漂亮。", "icon": "✨", "source": "Fangcal + Dikuc"},
    {"amis": "Citalaw to kohetingay.", "chi": "穿著黑色的褲子。", "icon": "👖", "source": "Ci- (Wear) + Color"},
    {"amis": "Citupel ci mama.", "chi": "爸爸戴(有)帽子。", "icon": "🧢", "source": "Ci- + Tupel"},
    {"amis": "Micakay kako to cukap.", "chi": "我買鞋子。", "icon": "👟", "source": "Mi-cakay (Buy)"},
    {"amis": "Kahengang ko kiping ni Panay.", "chi": "Panay的上衣是紅色的。", "icon": "🔴", "source": "Color + Item"},
]

# --- 3. 隨機題庫 (定義) ---
raw_quiz_pool = [
    {
        "q": "Fangcal ko dikuc no miso.",
        "audio": "Fangcal ko dikuc no miso",
        "options": ["你的衣服很漂亮", "你的衣服很貴", "你的衣服很便宜"],
        "ans": "你的衣服很漂亮",
        "hint": "Fangcal 是漂亮/美好"
    },
    {
        "q": "Citalaw to kohetingay.",
        "audio": "Citalaw to kohetingay",
        "options": ["穿著黑色的褲子", "穿著紅色的褲子", "穿著白色的褲子"],
        "ans": "穿著黑色的褲子",
        "hint": "Koheting 是黑色 (像炭一樣)"
    },
    {
        "q": "單字測驗：Tupel",
        "audio": "Tupel",
        "options": ["帽子", "鞋子", "褲子"],
        "ans": "帽子",
        "hint": "戴在頭上的"
    },
    {
        "q": "單字測驗：Talaw",
        "audio": "Talaw",
        "options": ["褲子", "衣服", "鞋子"],
        "ans": "褲子",
        "hint": "穿在腿上的"
    },
    {
        "q": "單字測驗：Cukap",
        "audio": "Cukap",
        "options": ["鞋子", "襪子", "手套"],
        "ans": "鞋子",
        "hint": "穿在腳上的 (不是襪子)"
    },
    {
        "q": "Citupel ci mama.",
        "audio": "Citupel ci mama",
        "options": ["爸爸戴帽子", "爸爸買帽子", "爸爸洗帽子"],
        "ans": "爸爸戴帽子",
        "hint": "Ci- 表示「有/穿戴」"
    },
    {
        "q": "「紅色」的阿美語怎麼說？",
        "audio": None,
        "options": ["Kahengang", "Kohecal", "Koheting"],
        "ans": "Kahengang",
        "hint": "像火一樣的顏色"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌
    selected_questions = random.sample(raw_quiz_pool, 3)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #8E24AA;'>Unit 19: O Dikuc</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>服裝與穿著 (Clothing)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #8E24AA;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 3)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 3**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #E1BEE7; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #4A148C;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會描述穿著了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 3)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()
