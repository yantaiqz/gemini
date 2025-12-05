import streamlit as st
import google.generativeai as genai
import io
import tempfile
import json
import datetime
import os
import docx

# -------------------------------------------------------------
# --- 1. 多语言配置与资源字典 (新增模块) ---
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
        "risk_prompt_lang": "请使用中文输出报告。"
    },
    "en": {
        "page_title": "Cross-border Compliance Judi: Laws, Companies & Contracts",
        "daily_visits": "Daily Visits",
        "upload_label": "Contract Risk Review",
        "upload_help": "Gemini can analyze PDF and text files directly.",
        "start_review": "Start Risk Review",
        "review_success": "Review Completed!",
        "file_uploaded": "File uploaded: {file_name}, requesting review.",
        "processing": "Analyzing {file_name}...",
        "common_q_title": "Common Compliance Questions & Company Checks",
        "chat_placeholder": "Enter your compliance question...",
        "clear_history": "🧹 Clear History",
        "clear_help": "Clears all chat history and uploaded files.",
        "welcome": "Hello! I am Judi, your Cross-border Compliance Expert. How can I assist you with legal, regulatory, or qualification issues for your overseas business?",
        "questions": [
            "How to handle a US Amazon TRO?",
            "Key points for manufacturing labor contracts in Vietnam?",
            "Data compliance for car exports to Europe?",
            "Credit status of BYD Brazil?",
            "Safe payment terms for ADNOC (Abu Dhabi)?"
        ],
        "risk_prompt_lang": "Please output the report in English."
    },
    "ar": {
        "page_title": "جودي للامتثال عبر الحدود: القوانين والشركات والعقود",
        "daily_visits": "زيارات اليوم",
        "upload_label": "مراجعة مخاطر العقد",
        "upload_help": "يمكن لـ Gemini تحليل ملفات PDF والنصوص مباشرة.",
        "start_review": "بدء المراجعة",
        "review_success": "تمت المراجعة!",
        "file_uploaded": "تم رفع الملف: {file_name}، جاري طلب المراجعة.",
        "processing": "جاري تحليل {file_name}...",
        "common_q_title": "أسئلة الامتثال الشائعة وفحص الشركات",
        "chat_placeholder": "أدخل سؤال الامتثال الخاص بك...",
        "clear_history": "🧹 مسح السجل",
        "clear_help": "يمسح كل سجل الدردشة والملفات المرفوعة.",
        "welcome": "مرحبًا! أنا جودي، خبيرة الامتثال عبر الحدود. كيف يمكنني مساعدتك في المسائل القانونية أو التنظيمية لأعمالك الخارجية؟",
        "questions": [
            "كيفية التعامل مع أمر تقييدي مؤقت (TRO) من أمازون الأمريكية؟",
            "النقاط الرئيسية لعقود العمل في مصانع فيتنام؟",
            "الامتثال للبيانات لتصدير السيارات إلى أوروبا؟",
            "الوضع الائتماني لشركة BYD البرازيل؟",
            "شروط الدفع الآمنة لشركة أدنوك (أبو ظبي)؟"
        ],
        "risk_prompt_lang": "يرجى إخراج التقرير باللغة العربية."
    },
    "pt": {
        "page_title": "Compliance Transfronteiriço Judi: Leis, Empresas e Contratos",
        "daily_visits": "Visitas Hoje",
        "upload_label": "Revisão de Risco de Contrato",
        "upload_help": "Gemini pode analisar arquivos PDF e texto diretamente.",
        "start_review": "Iniciar Revisão",
        "review_success": "Revisão Concluída!",
        "file_uploaded": "Arquivo enviado: {file_name}, solicitando revisão.",
        "processing": "Analisando {file_name}...",
        "common_q_title": "Perguntas Comuns de Compliance & Verificação de Empresas",
        "chat_placeholder": "Digite sua dúvida de compliance...",
        "clear_history": "🧹 Limpar Histórico",
        "clear_help": "Limpa todo o histórico de chat e arquivos.",
        "welcome": "Olá! Sou a Judi, sua especialista em Compliance Transfronteiriço. Como posso ajudar com questões legais ou regulatórias para seus negócios no exterior?",
        "questions": [
            "Como lidar com uma TRO da Amazon nos EUA?",
            "Pontos chave em contratos de trabalho no Vietnã?",
            "Compliance de dados para exportação de carros para a Europa?",
            "Situação de crédito da BYD Brasil?",
            "Prazos de pagamento seguros para ADNOC (Abu Dhabi)?"
        ],
        "risk_prompt_lang": "Por favor, emita o relatório em Português."
    },
    "es": {
        "page_title": "Cumplimiento Transfronterizo Judi: Leyes, Empresas y Contratos",
        "daily_visits": "Visitas Hoy",
        "upload_label": "Revisión de Riesgos de Contrato",
        "upload_help": "Gemini puede analizar archivos PDF y texto directamente.",
        "start_review": "Iniciar Revisión",
        "review_success": "¡Revisión Completada!",
        "file_uploaded": "Archivo subido: {file_name}, solicitando revisión.",
        "processing": "Analizando {file_name}...",
        "common_q_title": "Preguntas Comunes de Cumplimiento",
        "chat_placeholder": "Ingrese su pregunta de cumplimiento...",
        "clear_history": "🧹 Borrar Historial",
        "clear_help": "Borra todo el historial de chat y archivos.",
        "welcome": "¡Hola! Soy Judi, su experta en Cumplimiento Transfronterizo. ¿Cómo puedo ayudarle con problemas legales o regulatorios en el extranjero?",
        "questions": [
            "¿Cómo manejar una TRO de Amazon EE.UU.?",
            "¿Puntos clave en contratos laborales en Vietnam?",
            "¿Cumplimiento de datos para exportar autos a Europa?",
            "¿Situación crediticia de BYD Brasil?",
            "¿Plazos de pago seguros para ADNOC (Abu Dhabi)?"
        ],
        "risk_prompt_lang": "Por favor, emita el informe en Español."
    }
}

# -------------------------------------------------------------
# --- 2. 页面初始化与语言选择 ---
# -------------------------------------------------------------

st.set_page_config(page_title="跨境合规专家AI (Global Compliance)", page_icon="⚖️")

# --- 语言选择器 (放在最顶部) ---
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

# 动态生成 System Instruction，确保 AI 知道用什么语言回答
def get_system_instruction(lang_code):
    base_instruction = """
    **Role:**
    You are a "Global Cross-border Compliance Expert and International Lawyer" with 20 years of experience. Your core clients are "Global Expansion Enterprises". Your task is to provide rigorous, professional, and practical compliance advice based on the legal environment of the target country (e.g., USA, EU, Southeast Asia).

    **Core Guidelines:**
    1. **Professional Tone:** Objective, neutral, rigorous. Include necessary legal disclaimers.
    2. **Region Specific:** Answers must be based on the current laws of the target country.
    3. **Structured Output:** Use "Core Risks", "Legal Basis", "Compliance Suggestions".
    4. **Mandatory Citations:** End every answer with a [Data Source/Legal Basis] section.
    5. **Company Reports:** When asked about a specific company, strictly follow the "Corporate Credit Assessment Report" format provided in your knowledge base.

    **Disclaimer:**
    End all responses with: "This response is AI-generated for reference only and does not constitute formal legal advice."
    """
    
    # 语言强制指令
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
Generate a structured report in Markdown format with the following sections:
1. **Core Risk Identification:** Top 3 legal/commercial risks.
2. **Jurisdiction/Choice of Law:** Evaluate the risk level (High/Med/Low).
3. **Termination & Exit Mechanism:** Fairness of termination clauses.
4. **Comprehensive Risk Rating:** High/Medium/Low and short advice.
"""

# API Key 配置
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("请配置 API Key")
    st.stop()
genai.configure(api_key=api_key)

# 缓存模型初始化 (依赖于语言，如果语言变了，System Instruction 变了，需要重新加载)
@st.cache_resource
def initialize_model(lang_code):
    generation_config = {
        "max_output_tokens": 4096 
    }
    
    sys_instruction = get_system_instruction(lang_code)
    
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash', # 建议使用 flash 2.0 或 1.5 flash，速度快且便宜
        system_instruction=sys_instruction,
        generation_config=generation_config
    )
    return model

# 初始化对应语言的模型
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

    # 显示用户消息（翻译）
    user_msg_display = T["file_uploaded"].format(file_name=file_name)
    st.chat_message("user", avatar="👤").write(user_msg_display)

    try:
        with st.spinner(T["processing"].format(file_name=file_name)):
            # 拼接语言要求到 Prompt
            final_risk_prompt = RISK_ANALYSIS_PROMPT_BASE + "\n\n" + T["risk_prompt_lang"]
            
            #prompt_parts = [
            #    final_risk_prompt,
            #    {"mime_type": mime_type, "data": file_bytes}
            #]


            # === 核心修改开始：针对不同文件类型的处理 ===
            prompt_parts = []
            
            if mime_type == "application/pdf":
                # PDF 可以直接传二进制给 Gemini
                prompt_parts = [
                    final_risk_prompt,
                    {"mime_type": mime_type, "data": file_bytes}
                ]
            
            elif mime_type == "text/plain":
                # TXT 文件解码为字符串
                text_content = file_bytes.decode("utf-8")
                prompt_parts = [final_risk_prompt, text_content]
            
            elif "wordprocessingml.document" in mime_type: # 处理 .docx
                # Word 文档需要提取文字
                try:
                    doc = docx.Document(io.BytesIO(file_bytes))
                    full_text = []
                    for para in doc.paragraphs:
                        full_text.append(para.text)
                    # 将提取的文字拼接成一个长字符串
                    text_content = '\n'.join(full_text)
                    
                    # 将文字作为 Prompt 的一部分发送
                    prompt_parts = [final_risk_prompt, text_content]
                except Exception as e:
                    st.error(f"解析 Word 文件失败: {e}")
                    st.stop()
            # === 核心修改结束 ===
            
            
            response_stream = model.generate_content(prompt_parts, stream=True)
            
            with st.chat_message("assistant", avatar="👩‍💼"):
                message_placeholder = st.empty()
                full_review = ""
                for chunk in response_stream:
                    if chunk.text:
                        full_review += chunk.text
                        message_placeholder.markdown(full_review + "▌")
                message_placeholder.markdown(full_review)
                # 记录到历史
                st.session_state.messages.append({"role": "assistant", "content": full_review})
                
        st.success(T["review_success"])

    except Exception as e:
        st.error(f"Error details: {e}")

st.markdown('<hr style="border-top: 2px dashed #8c8c8c; background: none;">', unsafe_allow_html=True)

# -------------------------------------------------------------
# --- 6. 聊天模块与常见问题 ---
# -------------------------------------------------------------

# 初始化聊天历史 (如果语言改变，可以在这里重置，或者保留历史)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": T["welcome"]}
    ]

st.subheader(T["common_q_title"])

# 常见问题按钮 (动态加载当前语言的问题)
cols = st.columns(3)
prompt_from_button = None
current_questions = T["questions"] # 获取当前语言的问题列表

for i, question in enumerate(current_questions):
    with cols[i % 3]: 
        if st.button(question, use_container_width=True, key=f"q_{current_lang_code}_{i}"):
            prompt_from_button = question

# 显示历史消息
for msg in st.session_state.messages:
    icon = USER_ICON if msg["role"] == "user" else ASSISTANT_ICON
    st.chat_message(msg["role"], avatar=icon).write(msg["content"])

# 处理输入
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
            
            # 发送请求时，模型已经配置了对应语言的 System Instruction
            for chunk in model.generate_content(user_input, stream=True):
                full_response += chunk.text if chunk.text else ""
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    except Exception as e:
        st.error(f"API Error: {e}")

# 清空按钮
if st.button(T["clear_history"], help=T["clear_help"]):
    st.session_state.messages = [{"role": "assistant", "content": T["welcome"]}]
    st.rerun()
