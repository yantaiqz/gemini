import streamlit as st
import google.generativeai as genai

import os

# 确保配置了 API KEY
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"]) 

print("正在列出可用模型...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)


st.title("我的 Gemini 助手")

# 获取 API Key
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("请配置 API Key")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# 简单的聊天界面
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("说点什么..."):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = model.generate_content(prompt)
    st.chat_message("assistant").write(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
