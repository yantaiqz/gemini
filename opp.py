import streamlit as st
import google.generativeai as genai
# import os # 部署在 Streamlit Cloud 时，不需要 os 模块来读取环境变量

# --- 1. 设置系统指令和模型配置 ---
# 定义律师角色
SYSTEM_INSTRUCTION = """
你是一个专业的AI法律顾问。你的回答必须基于中国法律常识和相关法规，提供清晰、简洁、中立的法律建议。
请注意：你不能代替真正的律师提供正式的法律意见和诉讼服务。始终保持专业、客观的语气。
"""

# 定义常见法律问题
COMMON_LEGAL_QUESTIONS = [
    "劳动合同到期，公司不续签，有经济补偿金吗？",
    "借钱给朋友，没有借条，怎么起诉？",
    "租房合同没到期，房东要提前收回房子怎么办？"
]

# --- 2. 页面配置和模型初始化 ---

st.set_page_config(page_title="AI 法律顾问", page_icon="⚖️")
st.title("⚖️ AI 法律顾问")


# 获取 API Key
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    # 仅在部署时会显示此错误，本地运行需确保环境变量或 secrets 配置正确
    st.error("请配置 GEMINI_API_KEY")
    st.stop()

# 配置 Gemini
genai.configure(api_key=api_key)

# 使用最新的推荐模型，并应用律师角色系统指令
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash-lite', # 更稳定、更快的模型
    system_instruction=SYSTEM_INSTRUCTION
)

# 简单的聊天界面
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. 常见问题按钮逻辑 ---

# 检查是否有按钮被点击
prompt_from_button = None
st.subheader("💡 常见法律问题快速咨询")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("劳动合同不续签补偿？", use_container_width=True):
        prompt_from_button = COMMON_LEGAL_QUESTIONS[0]
with col2:
    if st.button("借钱没借条怎么起诉？", use_container_width=True):
        prompt_from_button = COMMON_LEGAL_QUESTIONS[1]
with col3:
    if st.button("房东提前收房怎么办？", use_container_width=True):
        prompt_from_button = COMMON_LEGAL_QUESTIONS[2]

# --- 4. 核心聊天逻辑 ---

# 显示历史消息
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 确定本次的输入是什么
if prompt_from_button:
    user_input = prompt_from_button
else:
    user_input = st.chat_input("请输入你的法律问题...")


if user_input:
    # 显示用户消息
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 调用 Gemini
    with st.chat_message("assistant"):
        response = model.generate_content(user_input, stream=True)
        # 流式输出
        full_response = st.write_stream(response)
        
        # 保存模型回复到历史
        st.session_state.messages.append({"role": "assistant", "content": full_response})
