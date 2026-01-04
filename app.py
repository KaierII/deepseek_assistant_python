# -*- coding: utf-8 -*-
import streamlit as st
from openai import OpenAI
import re
import os

# ============ 配置区 ============
# 第一次运行时在这里填入你的DeepSeek Key（免费注册：https://platform.deepseek.com）
API_KEY = ""   # ←←←← 修改这行！！！

# 如果不想改代码，也可以在界面里填
if not API_KEY or API_KEY.startswith("sk-"):
    API_KEY = st.sidebar.text_input("🔑 DeepSeek API Key", type="password")
    if not API_KEY or not API_KEY.startswith("sk-"):
        st.error("请先去 https://platform.deepseek.com 注册并填写API Key")
        st.stop()

client = OpenAI(api_key=API_KEY, base_url="https://api.chatanywhere.tech/v1")

# ============ 侧边栏 ============
st.sidebar.title("🛠️ 设置")
mode = st.sidebar.radio("选择使用模式", ["👨‍🎓 学生答疑", "👩‍🏫 教师出题/生成讲义"])

# ============ 系统提示词（超重要！）============
system_prompt = {
    "👨‍🎓 学生答疑": """你是一个耐心的中国高中教学助手。对每道题都要详细写出解题思路、完整推导过程和最终答案。
    数学公式必须用标准LaTeX格式，行内公式用$包裹（如：$x^2 + y^2 = r^2$），块级公式用$$包裹（如：$$\\int_0^1 x dx = 0.5$$）。
    物理化学画图用文字描述。语言通俗易懂，适合高中生。""",
    "👩‍🏫 教师出题/生成讲义": """你是一个经验丰富的中国高中教师。帮我生成高质量的题目、讲义大纲或答案解析。
    数学公式必须用标准LaTeX格式，行内公式用$包裹（如：$x^2 + y^2 = r^2$），块级公式用$$包裹（如：$$\\int_0^1 x dx = 0.5$$）。
    答案要带详细步骤和评分标准。"""
}[mode]

# ============ 工具函数：处理LaTeX渲染 ============
def render_latex_content(content):
    """
    处理文本中的LaTeX公式，确保Streamlit能正确渲染
    """
    # 确保反斜杠不被转义（处理AI返回的\\为\）
    content = content.replace('\\\\', '\\')
    
    # Streamlit的markdown支持LaTeX，直接返回处理后的内容即可
    return content

# ============ 会话历史 ============
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# 显示历史
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").markdown(render_latex_content(msg["content"]))

# ============ 主界面 ============
st.title("🚀 基于DeepSeek的智能教学助手")
st.caption("完全免费 · 支持离线打包")

if prompt := st.chat_input("在这里输入问题或课题（如：高中数学 一元二次方程讲义）"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("DeepSeek正在思考..."):
            response = client.chat.completions.create(
                model="deepseek-chat",        # 免费额度超大
                messages=st.session_state.messages,
                temperature=0.3,
                stream=False
            )
            answer = response.choices[0].message.content
            # 处理LaTeX并渲染
            rendered_answer = render_latex_content(answer)
            st.markdown(rendered_answer, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# ============ 侧边栏额外功能 ============
if st.sidebar.button("🗑️ 清空对话"):
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.rerun()

st.sidebar.success("每日免费200万tokens，够用一辈子！")
st.sidebar.markdown("[获取免费API Key](https://platform.deepseek.com)")

# 启用Streamlit的LaTeX渲染（确保页面配置正确）
st.set_page_config(
    page_title="智能教学助手",
    page_icon="🚀",
    layout="wide"
)
