import streamlit as st
from PIL import Image
import io

# 页面配置 - 使用宽屏布局
st.set_page_config(
    page_title="AI画家 - 图片风格融合",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS - 修复定位问题
st.markdown(
    """
    <style>
    /* 全局样式重置 */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* 确保页面占满整个屏幕且不可滚动 */
    html, body, #root, .stApp {
        height: 100vh !important;
        width: 100vw !important;
        overflow: hidden !important;
        position: fixed !important;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 主容器 - 灰色背景 */
    .main-container {
        background-color: #808080;
        height: 100vh;
        width: 100vw;
        display: flex;
        align-items: center;
        justify-content: center;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1;
    }
    
    /* 白色工作区 */
    .white-container {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        width: 80vw;
        height: 80vh;
        padding: 2%;
        display: flex;
        flex-direction: column;
        z-index: 2;
        position: relative;
    }
    
    /* 标题区域 */
    .title-section {
        text-align: center;
        margin-bottom: 2%;
        padding-bottom: 1%;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .main-title {
        font-size: 2.5vw;
        font-weight: bold;
        color: #ff69b4;
        margin: 0;
    }
    
    /* 三个图片框的主容器 */
    .boxes-row {
        flex: 1;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 5%;
        margin: 2% 0;
    }
    
    /* 单个图片框样式 */
    .image-box {
        width: 30%;
        height: 70%;
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #f1f8e9;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .image-box:hover {
        border-color: #388E3C;
        background-color: #dcedc8;
        transform: translateY(-5px);
    }
    
    .box-text {
        color: #2E7D32;
        font-size: 1.2vw;
        text-align: center;
        margin-top: 10px;
    }
    
    /* 运算符样式 */
    .operator {
        font-size: 2.5vw;
        color: #6b7280;
        font-weight: 300;
        margin: 0 1%;
    }
    
    /* 按钮容器 */
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 2%;
        padding-top: 2%;
        border-top: 1px solid #f0f0f0;
    }
    
    .generate-btn {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 15px 40px;
        font-size: 1.2vw;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 25%;
        max-width: 200px;
    }
    
    .generate-btn:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
    }
    
    /* 底部信息 */
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.9vw;
        margin-top: 1%;
    }
    
    /* 文件上传器样式修复 */
    .stFileUploader {
        width: 100% !important;
        height: 100% !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
    }
    
    .stFileUploader > label {
        display: none !important;
    }
    
    .stFileUploader > div {
        border: none !important;
        background: transparent !important;
        width: 100% !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* 按钮样式修复 */
    .stButton > button {
        width: 100% !important;
    }
    
    /* 图片显示修复 */
    .stImage {
        width: 90% !important;
        height: 90% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .stImage img {
        max-width: 100% !important;
        max-height: 100% !important;
        object-fit: contain !important;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 主容器 - 灰色背景
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# 白色工作区
st.markdown('<div class="white-container">', unsafe_allow_html=True)

# 标题
st.markdown('''
<div class="title-section">
    <div class="main-title">🎨 AI图片风格融合工具</div>
</div>
''', unsafe_allow_html=True)

# 三个图片框横向排列
st.markdown('<div class="boxes-row">', unsafe_allow_html=True)

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
    st.image(image, use_column_width=True)
else:
    st.markdown('''
    <div style="text-align: center; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;">
        <div style="font-size: 4vw; color: #4CAF50;">📷</div>
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
    st.image(image, use_column_width=True)
else:
    st.markdown('''
    <div style="text-align: center; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;">
        <div style="font-size: 4vw; color: #4CAF50;">🎨</div>
        <div class="box-text">风格图片</div>
    </div>
    ''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 等号
st.markdown('<div class="operator">=</div>', unsafe_allow_html=True)

# 结果图片框
st.markdown('<div class="image-box">', unsafe_allow_html=True)
if 'result_image' in st.session_state and st.session_state.result_image:
    st.image(st.session_state.result_image, use_column_width=True)
else:
    st.markdown('''
    <div style="text-align: center; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;">
        <div style="font-size: 4vw; color: #4CAF50;">✨</div>
        <div class="box-text">融合结果</div>
    </div>
    ''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 关闭boxes-row

# 生成按钮
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button("🚀 一键生成", key="generate_btn", use_container_width=True):
    if content_image and style_image:
        with st.spinner("正在生成融合图片..."):
            st.session_state.result_image = "https://via.placeholder.com/400x300/4CAF50/FFFFFF?text=融合结果"
            st.success("风格融合完成！")
            st.rerun()
    else:
        st.warning("请先上传内容图片和风格图片")
st.markdown('</div>', unsafe_allow_html=True)

# 底部信息
st.markdown('''
<div class="footer">
    使用说明：上传内容图片和风格图片，点击生成按钮即可获得风格融合后的图片
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 关闭white-container
st.markdown('</div>', unsafe_allow_html=True)  # 关闭main-container

# 初始化session state
if 'result_image' not in st.session_state:
    st.session_state.result_image = Nonee




