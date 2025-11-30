import streamlit as st
import google.generativeai as genai

import os

# 确保配置了 API KEY
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"]) 

# --- 1. 设置系统指令和模型配置 ---
# 定义律师角色
SYSTEM_INSTRUCTION = """
**角色定义 (Role):**
你是一位拥有20年经验的“全球跨境合规专家与涉外律师”。你的核心服务对象是“中国出海企业”。你的任务是针对目的国（如美国、欧盟、东南亚等）的法律环境，提供严谨、专业、具有实操性的合规建议。

**核心行为准则 (Core Guidelines):**
1.  **专业语气:** 保持客观、中立、严谨的法律专业人士语气。避免使用模棱两可的词汇，但必须包含必要的法律免责声明。
2.  **地域精准:** 回答必须基于目标国家/地区的现行法律法规（如GDPR, CCPA, 越南劳动法等）。
3.  **结构化输出:** 回答复杂法律问题时，请使用“核心风险点”、“法律依据”、“合规建议”的分层结构。
4.  **强制数据来源:** 每一个回答的末尾，必须设立独立章节【数据来源/法律依据】，明确列出参考的法条、公约、官方指南或权威报告名称。
5.  **企业资质与信用查询 **当提及具体海外公司时，**不要**仅提供一段普通文本。必须按照**简化版邓白氏报告 (Dun & Bradstreet Style)** 的结构进行回复：

--- 报告格式开始 ---
### 🏢 企业资信评估报告 (模拟)
**1. 概要与评级 (Summary)**
* **企业名称:** [英文全称]
* **D-U-N-S® (模拟/未知):** [如有则填，无则标注未知]
* **综合风险评级:** [高/中/低 - 基于公开负面新闻判断]

**2. 基本识别信息 (Identification)**
* **注册地址:** [详细地址]
* **成立时间:** [年份]
* **企业类型:** [如：有限责任公司 / 上市公司]

**3. 运营与业务 (Operations)**
* **主营业务:** [核心产品或服务]
* **行业地位:** [简述]

**4. 合规与法律风险 (Legal & Compliance Risks)**
* **制裁名单扫描:** [是否在实体清单/SDN名单中]
* **公开诉讼记录:** [是否有重大公开诉讼]
* **负面舆情:** [近期相关负面新闻摘要]

**【数据来源】**
* 基于公开商业数据库及网络公开信息检索。
--- 报告格式结束 ---

**免责声明:**
请在所有回复最后注明：“*本回复由AI生成，仅供一般性参考，不构成正式法律意见。重大商业决策请咨询当地持牌律师。*”

"""

# 定义常见法律问题
COMMON_LEGAL_QUESTIONS = [
    "美国亚马逊被法院TRO怎么办？",
    "越南制造业工厂的劳动合同应该注意什么？",
    "汽车出口欧洲如何实现数据合规？",
     "巴西比亚迪的征信情况",
     "阿布扎比国家石油公司的账期多久比较安全"
]


# --- 2. 页面配置和模型初始化 ---
st.set_page_config(page_title="跨境合规专家AI", page_icon="⚖️")
st.title("👩‍💼 跨境合规Judi：查法规、查外企")

# 获取 API Key
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("请配置 API Key")
    st.stop()


# 设置 max_output_tokens 为 4096，以确保回答长度足够
generation_config = {
    "max_output_tokens": 4096 
}
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    generation_config=generation_config
)

# 简单的聊天界面
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# --- 3. 常见问题按钮逻辑 ---

# 检查是否有按钮被点击
prompt_from_button = None
st.subheader("⚖️ 常见合规问题和外企资质快速查询")
col1, col2, col3 , col4, col5 = st.columns(5)

with col1:
    if st.button("美国亚马逊被法院TRO怎么办？", use_container_width=True):
        prompt_from_button = COMMON_LEGAL_QUESTIONS[0]
with col2:
    if st.button("越南制造业工厂的劳动合同应该注意什么？", use_container_width=True):
        prompt_from_button = COMMON_LEGAL_QUESTIONS[1]
with col3:
    if st.button("汽车出口欧洲如何实现数据合规？", use_container_width=True):
        prompt_from_button = COMMON_LEGAL_QUESTIONS[2]
with col4:
    if st.button("巴西比亚迪的征信情况", use_container_width=True):
        prompt_from_button = COMMON_LEGAL_QUESTIONS[3]
with col5:
    if st.button("阿布扎比国家石油公司的账期多久比较安全", use_container_width=True):
        prompt_from_button = COMMON_LEGAL_QUESTIONS[4]

# --- 4. 核心聊天逻辑 (已修正) ---

# 定义头像常量，确保一致性
USER_ICON = "👤"
ASSISTANT_ICON = "👩‍💼"

# 1. 显示历史消息 (修正：添加头像参数)
for msg in st.session_state.messages:
    icon = USER_ICON if msg["role"] == "user" else ASSISTANT_ICON
    st.chat_message(msg["role"], avatar=icon).write(msg["content"])

# 2. 【关键修正】将 chat_input 提到前面，确保它始终渲染
chat_input_text = st.chat_input("请输入你的合规问题...")

# 3. 确定本次的输入是什么 (合并来源)
# 注意：prompt_from_button 应该在 app.py 的顶部被定义和赋值
if prompt_from_button:
    user_input = prompt_from_button
elif chat_input_text:
    user_input = chat_input_text
else:
    user_input = None

# 4. 处理输入
if user_input:
    # 显示用户消息
    st.chat_message("user", avatar=USER_ICON).write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 调用 Gemini (修正：使用流式输出，并添加错误捕捉)
    try:
        with st.chat_message("assistant", avatar=ASSISTANT_ICON):
            # 使用 stream=True 实现流式输出，提升用户体验
            response = model.generate_content(user_input, stream=True)
            full_response = st.write_stream(response)
            
            # 保存回复到历史
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        # 捕捉可能出现的 ResourceExhausted 或 NotFound 错误
        st.error(f"发生错误: {e}")

