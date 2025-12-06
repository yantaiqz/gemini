import streamlit as st
import google.generativeai as genai
import io
import tempfile
import json
import datetime
import os
import docx

# -------------------------------------------------------------
# --- 1. 多语言配置与资源字典 ---
# -------------------------------------------------------------

# 语言选项映射
LANG_OPTIONS = {
    "中文 (默认)": "zh",
    "English": "en",
    "العربية (Arabic)": "ar",
    "Português": "pt",
    "Español": "es"
}

# 界面文本翻译字典
TRANSLATIONS = {
    "zh": {
        "page_title": "跨境合规Judi：查法规、查外企、审合同",
        "daily_visits": "今日访问",
        "upload_label": "合同文件风险审核",
        "upload_help": "Gemini 可以直接读取 PDF 和文本文件进行分析",
        "start_review": "立即启动风险审查",
        "review_success": "合同审查完成！",
        "file_uploaded": "已上传文件: {file_name}，正在请求风险审查。",
        "processing": "正在分析 {file_name}...",
        "common_q_title": "常见合规问题和外企资质快速查询",
        "chat_placeholder": "请输入你的合规问题...",
        "clear_history": "🧹 清空聊天记录",
        "clear_help": "点击后将清除所有历史对话和文件上传记录",
        "welcome": "您好！我是您的跨境合规专家Judi。请问您在中国企业出海过程中遇到了哪些法律、监管或商业资质方面的问题？",
        "questions": [
            "美国亚马逊被法院TRO怎么办？",
            "越南制造业工厂的劳动合同应该注意什么？",
            "汽车出口欧洲如何实现数据合规？",
            "巴西比亚迪的征信情况",
            "阿布扎比国家石油公司的账期多久比较安全"
        ],
        "risk_prompt_lang": "请使用中文输出报告。",
        # --- 导航栏 (保持不变的内容) ---
        "nav_1": "财富排行", 
        "nav_2": "世界房产", 
        "nav_3": "城市房价", 
        "nav_4": "全球法律", 
        "nav_5": "全球企业", 
        "nav_6": "合同审查", 
        "nav_7": "德国财税", 
        "nav_8": "深圳房市"
    },
    "en": {
        "page_title": "Cross-border Compliance Judi",
        "daily_visits": "Daily Visits",
        "upload_label": "Contract Risk Review",
        "upload_help": "Gemini can analyze PDF and text files directly.",
        "start_review": "Start Risk Review",
        "review_success": "Review Completed!",
        "file_uploaded": "File uploaded: {file_name}, requesting review.",
        "processing": "Analyzing {file_name}...",
        "common_q_title": "Common Questions",
        "chat_placeholder": "Enter your compliance question...",
        "clear_history": "🧹 Clear History",
        "clear_help": "Clears all chat history.",
        "welcome": "Hello! I am Judi, your Cross-border Compliance Expert.",
        "questions": [
            "How to handle a US Amazon TRO?",
            "Vietnam labor contract key points?",
            "EU data compliance for car exports?",
            "Credit status of BYD Brazil?",
            "Safe payment terms for ADNOC?"
        ],
        "risk_prompt_lang": "Please output the report in English.",
        # --- Navbar (Content Unchanged) ---
        "nav_1": "Wealth Rank", 
        "nav_2": "Global Real Estate",  
        "nav_3": "Urban Housing",  
        "nav_4": "Global Legal",  
        "nav_5": "Global Enterprises",  
        "nav_6": "Contract Review",  
        "nav_7": "German Tax",  
        "nav_8": "Shenzhen Property" 
    },
    "ar": {
        "page_title": "جودي للامتثال عبر الحدود",
        "daily_visits": "زيارات اليوم",
        "upload_label": "مراجعة مخاطر العقد",
        "upload_help": "تحليل PDF والنصوص.",
        "start_review": "بدء المراجعة",
        "review_success": "تمت المراجعة!",
        "file_uploaded": "تم رفع الملف: {file_name}",
        "processing": "جاري تحليل {file_name}...",
        "common_q_title": "أسئلة شائعة",
        "chat_placeholder": "أدخل سؤالك...",
        "clear_history": "🧹 مسح السجل",
        "clear_help": "يمسح السجل.",
        "welcome": "مرحبًا! أنا جودي، خبيرة الامتثال.",
        "questions": [
            "التعامل مع TRO من أمازون؟",
            "عقود العمل في فيتنام؟",
            "الامتثال للبيانات في أوروبا؟",
            "الوضع الائتماني لشركة BYD؟",
            "شروط الدفع لأدنوك؟"
        ],
        "risk_prompt_lang": "يرجى إخراج التقرير باللغة العربية.",
        # --- Navbar (Mapped to English for consistency or translated) ---
        "nav_1": "Wealth Rank", 
        "nav_2": "Global Real Estate",  
        "nav_3": "Urban Housing",  
        "nav_4": "Global Legal",  
        "nav_5": "Global Enterprises",  
        "nav_6": "Contract Review",  
        "nav_7": "German Tax",  
        "nav_8": "Shenzhen Property" 
    },
    "pt": {
        "page_title": "Compliance Judi",
        "daily_visits": "Visitas Hoje",
        "upload_label": "Revisão de Contrato",
        "upload_help": "Analisa PDF e texto.",
        "start_review": "Iniciar Revisão",
        "review_success": "Concluído!",
        "file_uploaded": "Arquivo enviado: {file_name}",
        "processing": "Analisando {file_name}...",
        "common_q_title": "Perguntas Comuns",
        "chat_placeholder": "Digite sua dúvida...",
        "clear_history": "🧹 Limpar",
        "clear_help": "Limpa histórico.",
        "welcome": "Olá! Sou a Judi, especialista em Compliance.",
        "questions": [
            "Como lidar com TRO da Amazon?",
            "Contratos de trabalho no Vietnã?",
            "Compliance de dados na Europa?",
            "Crédito da BYD Brasil?",
            "Pagamento ADNOC?"
        ],
        "risk_prompt_lang": "Por favor, emita o relatório em Português.",
        # --- Navbar ---
        "nav_1": "Wealth Rank", 
        "nav_2": "Global Real Estate",  
        "nav_3": "Urban Housing",  
        "nav_4": "Global Legal",  
        "nav_5": "Global Enterprises",  
        "nav_6": "Contract Review",  
        "nav_7": "German Tax",  
        "nav_8": "Shenzhen Property" 
    },
    "es": {
        "page_title": "Cumplimiento Judi",
        "daily_visits": "Visitas Hoy",
        "upload_label": "Revisión de Contrato",
        "upload_help": "Analiza PDF y texto.",
        "start_review": "Iniciar Revisión",
        "review_success": "¡Completado!",
        "file_uploaded": "Archivo subido: {file_name}",
        "processing": "Analizando {file_name}...",
        "common_q_title": "Preguntas Comunes",
        "chat_placeholder": "Ingrese su pregunta...",
        "clear_history": "🧹 Borrar",
        "clear_help": "Borra historial.",
        "welcome": "¡Hola! Soy Judi, experta en Cumplimiento.",
        "questions": [
            "¿Manejo de TRO de Amazon?",
            "¿Contratos laborales en Vietnam?",
            "¿Datos para Europa?",
            "¿Crédito de BYD Brasil?",
            "¿Pago seguro ADNOC?"
        ],
        "risk_prompt_lang": "Por favor, emita el informe en Español.",
        # --- Navbar ---
        "nav_1": "Wealth Rank", 
        "nav_2": "Global Real Estate",  
        "nav_3": "Urban Housing",  
        "nav_4": "Global Legal",  
        "nav_5": "Global Enterprises",  
        "nav_6": "Contract Review",  
        "nav_7": "German Tax",  
        "nav_8": "Shenzhen Property" 
    }
}

# -------------------------------------------------------------
# --- 2. 页面初始化、CSS样式与语言选择 ---
# -------------------------------------------------------------

st.set_page_config(page_title="跨境合规专家AI (Global Compliance)", page_icon="⚖️", layout="wide")

# --- 注入 CSS 样式 (使用 WealthRank 的纯文字导航样式) ---
st.markdown("""
<style>
    /* 1. 隐藏 Streamlit 默认元素 */
    header, [data-testid="stSidebar"], footer, .stDeployButton, [data-testid="stToolbar"] {
        display: none !important;
    }

    /* 2. 全局容器调整 */
    .stApp {
        background-color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
        padding-bottom: 80px !important; /* 关键：防止内容被导航栏遮挡 */
        margin: 0 !important;
    }

    /* 3. 底部导航核心样式 - 纯文字现代风 (8个项) */
    .bottom-nav {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 60px !important;
        background-color: rgba(255, 255, 255, 0.90) !important;
        backdrop-filter: blur(16px) !important;
        border-top: 1px solid rgba(226, 232, 240, 0.8) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        padding: 0 10px !important;
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.03) !important;
        z-index: 9999 !important;
        box-sizing: border-box !important;
    }
    
    /* 4. 导航项样式 */
    .nav-item {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        height: 40px !important;
        color: #94a3b8 !important;
        text-decoration: none !important;
        font-size: 0.70rem !important; /* 缩小适配8个项 */
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        margin: 0 2px !important;
        white-space: nowrap !important; /* 禁止换行 */
        overflow: hidden !important; /* 超出隐藏 */
        text-overflow: ellipsis !important; /* 超长显示省略号 */
    }
    
    .nav-item:hover {
        background-color: rgba(241, 245, 249, 0.8) !important;
        color: #64748b !important;
    }
    
    .nav-item.active {
        color: #2563eb !important;
        background-color: rgba(59, 130, 246, 0.1) !important;
    }
    
    .nav-item.active::before {
        display: none !important;
    }
    
    /* 适配手机端，避免8个字太拥挤 */
    @media (max-width: 640px) {
        .nav-item {
            font-size: 0.65rem !important;
            margin: 0 1px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- 语言选择器 ---
selected_lang_label = st.selectbox(
    "🌐 Language / 语言 / لغة / Idioma",
    options=list(LANG_OPTIONS.keys()),
    index=0
)
current_lang_code = LANG_OPTIONS[selected_lang_label]
T = TRANSLATIONS[current_lang_code] # 获取当前语言的翻译包

st.title(T["page_title"])

# -------------------------------------------------------------
# --- 3. 常量定义、系统指令和模型配置 ---
# -------------------------------------------------------------

USER_ICON = "👤"
ASSISTANT_ICON = "👩‍💼"

# 动态生成 System Instruction
def get_system_instruction(lang_code):
    base_instruction = """
    **Role:**
    You are a "Global Cross-border Compliance Expert and International Lawyer".
    
    **Core Guidelines:**
    1. **Professional Tone:** Objective, neutral, rigorous.
    2. **Region Specific:** Based on current laws.
    3. **Structured Output:** Use "Core Risks", "Legal Basis", "Compliance Suggestions".
    4. **Mandatory Citations:** End with [Data Source/Legal Basis].
    
    **Disclaimer:**
    End all responses with: "This response is AI-generated for reference only and does not constitute formal legal advice."
    """
    
    lang_directive = {
        "zh": "请务必使用**中文**回答所有问题。",
        "en": "Please answer all questions in **English**.",
        "ar": "Please answer all questions in **Arabic**.",
        "pt": "Please answer all questions in **Portuguese**.",
        "es": "Please answer all questions in **Spanish**."
    }
    
    return base_instruction + "\n\n" + lang_directive.get(lang_code, "Answer in English.")

RISK_ANALYSIS_PROMPT_BASE = """
Please act as a "Cross-border Compliance Expert" and strictly review this contract file. 
Generate a structured report in Markdown format with:
1. **Core Risk Identification**
2. **Jurisdiction/Choice of Law**
3. **Termination & Exit Mechanism**
4. **Comprehensive Risk Rating**
"""

# API Key 配置
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("请配置 API Key")
    st.stop()
genai.configure(api_key=api_key)

# 缓存模型初始化
@st.cache_resource
def initialize_model(lang_code):
    generation_config = {
        "max_output_tokens": 4096 
    }
    sys_instruction = get_system_instruction(lang_code)
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash', 
        system_instruction=sys_instruction,
        generation_config=generation_config
    )
    return model

model = initialize_model(current_lang_code)

# -------------------------- 4. 访问计数器 --------------------------
COUNTER_FILE = "visit_stats.json"

def update_daily_visits():
    try:
        today_str = datetime.date.today().isoformat()
        if "has_counted" in st.session_state:
            if os.path.exists(COUNTER_FILE):
                try:
                    with open(COUNTER_FILE, "r") as f:
                        return json.load(f).get("count", 0)
                except:
                    return 0
            return 0

        data = {"date": today_str, "count": 0}
        if os.path.exists(COUNTER_FILE):
            try:
                with open(COUNTER_FILE, "r") as f:
                    file_data = json.load(f)
                    if file_data.get("date") == today_str:
                        data = file_data
            except:
                pass 
        
        data["count"] += 1
        with open(COUNTER_FILE, "w") as f:
            json.dump(data, f)
        
        st.session_state["has_counted"] = True
        return data["count"]
    except Exception:
        return 0

daily_visits = update_daily_visits()
visit_text = f"{T['daily_visits']}: {daily_visits}"

st.markdown(f"""
<div style="text-align: center; color: #64748b; font-size: 0.7rem; margin-top: 10px; padding-bottom: 20px;">
    {visit_text}
</div>
""", unsafe_allow_html=True)

st.markdown('<hr style="border-top: 2px dashed #8c8c8c; background: none;">', unsafe_allow_html=True)

# -------------------------------------------------------------
# --- 5. 合同风险审核工具 ---
# -------------------------------------------------------------

uploaded_file = st.file_uploader(
    T["upload_label"], 
    type=['pdf', 'docx', 'txt'], 
    help=T["upload_help"]
)

if uploaded_file and st.button(T["start_review"], key="review_start_btn"):
    file_bytes = uploaded_file.getvalue()
    mime_type = uploaded_file.type
    file_name = uploaded_file.name

    user_msg_display = T["file_uploaded"].format(file_name=file_name)
    st.chat_message("user", avatar="👤").write(user_msg_display)

    try:
        with st.spinner(T["processing"].format(file_name=file_name)):
            final_risk_prompt = RISK_ANALYSIS_PROMPT_BASE + "\n\n" + T["risk_prompt_lang"]
            prompt_parts = []
            
            if mime_type == "application/pdf":
                prompt_parts = [
                    final_risk_prompt,
                    {"mime_type": mime_type, "data": file_bytes}
                ]
            elif mime_type == "text/plain":
                text_content = file_bytes.decode("utf-8")
                prompt_parts = [final_risk_prompt, text_content]
            elif "wordprocessingml.document" in mime_type:
                try:
                    doc = docx.Document(io.BytesIO(file_bytes))
                    full_text = []
                    for para in doc.paragraphs:
                        full_text.append(para.text)
                    text_content = '\n'.join(full_text)
                    prompt_parts = [final_risk_prompt, text_content]
                except Exception as e:
                    st.error(f"解析 Word 文件失败: {e}")
                    st.stop()
            
            response_stream = model.generate_content(prompt_parts, stream=True)
            
            with st.chat_message("assistant", avatar="👩‍💼"):
                message_placeholder = st.empty()
                full_review = ""
                for chunk in response_stream:
                    if chunk.text:
                        full_review += chunk.text
                        message_placeholder.markdown(full_review + "▌")
                message_placeholder.markdown(full_review)
                st.session_state.messages.append({"role": "assistant", "content": full_review})
                
        st.success(T["review_success"])

    except Exception as e:
        st.error(f"Error details: {e}")

st.markdown('<hr style="border-top: 2px dashed #8c8c8c; background: none;">', unsafe_allow_html=True)

# -------------------------------------------------------------
# --- 6. 聊天模块与常见问题 ---
# -------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": T["welcome"]}
    ]

st.subheader(T["common_q_title"])

cols = st.columns(3)
prompt_from_button = None
current_questions = T["questions"]

for i, question in enumerate(current_questions):
    with cols[i % 3]: 
        if st.button(question, use_container_width=True, key=f"q_{current_lang_code}_{i}"):
            prompt_from_button = question

for msg in st.session_state.messages:
    icon = USER_ICON if msg["role"] == "user" else ASSISTANT_ICON
    st.chat_message(msg["role"], avatar=icon).write(msg["content"])

chat_input_text = st.chat_input(T["chat_placeholder"])

if prompt_from_button:
    user_input = prompt_from_button
elif chat_input_text:
    user_input = chat_input_text
else:
    user_input = None

if user_input:
    st.chat_message("user", avatar=USER_ICON).write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        with st.chat_message("assistant", avatar=ASSISTANT_ICON):
            message_placeholder = st.empty()
            full_response = ""
            for chunk in model.generate_content(user_input, stream=True):
                full_response += chunk.text if chunk.text else ""
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    except Exception as e:
        st.error(f"API Error: {e}")

if st.button(T["clear_history"], help=T["clear_help"]):
    st.session_state.messages = [{"role": "assistant", "content": T["welcome"]}]
    st.rerun()

# -------------------------------------------------------------
# --- 7. 渲染底部导航栏 (保持不变的8个链接内容) ---
# -------------------------------------------------------------

def render_bottom_nav(text):
    nav_html = f"""
    <div class="bottom-nav">
        <a href="https://youqian.streamlit.app/" class="nav-item active" target="_self">
            {text['nav_1']}
        </a>
        <a href="https://fangchan.streamlit.app/" class="nav-item" target="_blank">
            {text['nav_2']}
        </a>
        <a href="https://fangjia.streamlit.app/" class="nav-item" target="_blank">
            {text['nav_3']}
        </a>
        <a href="https://chuhai.streamlit.app/" class="nav-item" target="_blank">
            {text['nav_4']}
        </a>
        <a href="https://chuhai.streamlit.app/" class="nav-item" target="_blank">
            {text['nav_5']}
        </a>
        <a href="https://chuhai.streamlit.app/" class="nav-item" target="_blank">
            {text['nav_6']}
        </a>
        <a href="https://qfschina.streamlit.app/" class="nav-item" target="_blank">
            {text['nav_7']}
        </a>
        <a href="https://fangjia.streamlit.app/" class="nav-item" target="_blank">
            {text['nav_8']}
        </a>
    </div>
    """
    st.markdown(nav_html, unsafe_allow_html=True)

# 调用导航渲染
render_bottom_nav(T)
