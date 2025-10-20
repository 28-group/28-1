import streamlit as st
from PIL import Image
import io

# 页面配置
st.set_page_config(
    page_title="AI画家 - 图片风格融合",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定义CSS
st.markdown(
    """
    <style>
    /* 隐藏所有Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 层面0：灰色背景（桌子） */
    .stApp {
        background-color: #808080 !important;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }
    
    /* 层面1：白色桌布（包含所有内容） */
    .white-tablecloth {
        background-color: white;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        width: 85%;
        min-height: 80vh;
        padding: 3rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    /* 标题区域 - 在白色桌布上 */
    .title-section {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ff69b4;
        margin: 0;
    }
    
    /* 三个图片框容器 - 在白色桌布上 */
    .boxes-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        margin: 2rem 0;
        flex: 1;
    }
    
    /* 单个图片框 - 在白色桌布上 */
    .image-box {
        width: 280px;
        height: 200px;
        border: 2px dashed #d1d5db;
        border-radius: 15px;
        background-color: #f8f9fa;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .image-box:hover {
        border-color: #3b82f6;
        background-color: rgba(59, 130, 246, 0.05);
        transform: translateY(-5px);
    }
    
    .box-text {
        color: #6b7280;
        font-size: 1.1rem;
        text-align: center;
        margin-top: 1rem;
    }
    
    /* 运算符 - 在白色桌布上 */
    .operator {
        font-size: 2.5rem;
        color: #6b7280;
        font-weight: 300;
    }
    
    /* 按钮容器 - 在白色桌布上 */
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 2rem;
    }
    
    .generate-btn {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 15px 50px;
        font-size: 1.2rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .generate-btn:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
    }
    
    /* 底部信息 - 在白色桌布上 */
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 1rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #e5e7eb;
    }
    
    /* 文件上传器样式 */
    .stFileUploader > label {
        display: none;
    }
    
    .stFileUploader > div {
        border: none !important;
        background: transparent !important;
    }
    
    /* 图片样式 */
    .stImage img {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 白色层面1：桌布（包含所有内容）
st.markdown('<div class="white-tablecloth">', unsafe_allow_html=True)

# 标题 - 在桌布上
st.markdown('''
<div class="title-section">
    <div class="main-title">🎨 AI图片风格融合工具</div>
</div>
''', unsafe_allow_html=True)

# 三个图片框 - 在桌布上
st.markdown('<div class="boxes-container">', unsafe_allow_html=True)

# 内容图片框
st.markdown('<div class="image-box">', unsafe_allow_html=True)
content_image = st.file_uploader(
    "内容图片",
    type=['png', 'jpg', 'jpeg'],
    key="content",
    label_visibility="collapsed"
)
if content_image:
    image = Image.open(content_image)
    st.image(image, width=240)
else:
    st.markdown('''
    <div style="text-align: center; padding: 20px;">
        <div style="font-size: 2.5rem; color: #6b7280;">📷</div>
        <div class="box-text">内容图片</div>
    </div>
    ''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 加号
st.markdown('<div class="operator">+</div>', unsafe_allow_html=True)

# 风格图片框
st.markdown('<div class="image-box">', unsafe_allow_html=True)
style_image = st.file_uploader(
    "风格图片", 
    type=['png', 'jpg', 'jpeg'],
    key="style",
    label_visibility="collapsed"
)
if style_image:
    image = Image.open(style_image)
    st.image(image, width=240)
else:
    st.markdown('''
    <div style="text-align: center; padding: 20px;">
        <div style="font-size: 2.5rem; color: #6b7280;">🎨</div>
        <div class="box-text">风格图片</div>
    </div>
    ''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 等号
st.markdown('<div class="operator">=</div>', unsafe_allow_html=True)

# 结果图片框
st.markdown('<div class="image-box">', unsafe_allow_html=True)
if 'result_image' in st.session_state and st.session_state.result_image:
    st.image(st.session_state.result_image, width=240)
else:
    st.markdown('''
    <div style="text-align: center; padding: 20px;">
        <div style="font-size: 2.5rem; color: #6b7280;">✨</div>
        <div class="box-text">融合结果</div>
    </div>
    ''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 关闭boxes-container

# 生成按钮 - 在桌布上
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button("🚀 一键生成风格融合图片", key="generate_btn"):
    if content_image and style_image:
        with st.spinner("正在生成融合图片..."):
            # 这里添加实际的风格融合代码
            st.session_state.result_image = "https://via.placeholder.com/280x200/4CAF50/FFFFFF?text=融合结果"
            st.success("风格融合完成！")
            st.rerun()
    else:
        st.warning("请先上传内容图片和风格图片")
st.markdown('</div>', unsafe_allow_html=True)

# 底部信息 - 在桌布上
st.markdown('''
<div class="footer">
    使用说明：上传内容图片和风格图片，点击生成按钮即可获得风格融合后的图片
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 关闭white-tablecloth

# 初始化session state
if 'result_image' not in st.session_state:
    st.session_state.result_image = None