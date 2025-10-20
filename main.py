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

# 自定义CSS - 只修复组件显示，保持原有布局
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
    html, body {
        height: 100vh;
        width: 100vw;
        overflow: hidden !important;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 主容器样式 */
    .stApp {
        height: 100vh;
        width: 100vw;
        overflow: hidden !important;
        position: relative;
    }
    
    /* 修复Streamlit默认容器样式 */
    .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        overflow: hidden !important;
        height: 100vh;
    }
    
    .main {
        padding: 0 !important;
        height: 100vh;
        overflow: hidden !important;
    }
    
    /* 层面0：灰色背景层 */
    .layer-0 {
        background-color: #808080;
        position: absolute;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1;
    }
    
    /* 层面1：白色工作区 */
    .layer-1 {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 70%;
        height: 70%;
        z-index: 2;
        padding: 2%;
        display: flex;
        flex-direction: column;
    }
    
    /* 标题区域 */
    .title-section {
        text-align: center;
        margin-bottom: 2%;
        padding-bottom: 1%;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .main-title {
        font-size: 1.8vw;
        font-weight: bold;
        color: #ff69b4;
        margin: 0;
    }
    
    /* 图片框容器 */
    .image-container {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2%;
        padding: 2%;
    }
    
    /* 单个图片框样式 */
    .image-box {
        width: 28%;
        aspect-ratio: 3/2;
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #f1f8e9;
        transition: all 0.3s ease;
        padding: 1%;
        position: relative;
    }
    
    .image-box:hover {
        border-color: #388E3C;
        background-color: #dcedc8;
    }
    
    .box-text {
        color: #2E7D32;
        font-size: 1vw;
        text-align: center;
        margin-top: 8px;
    }
    
    /* 加号样式 */
    .operator {
        font-size: 2vw;
        color: #6b7280;
        font-weight: 300;
    }
    
    /* 按钮容器 */
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 1%;
        padding-top: 1%;
        border-top: 1px solid #f0f0f0;
    }
    
    .generate-button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.8% 2%;
        font-size: 1.1vw;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 25%;
        max-width: 180px;
    }
    
    .generate-button:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
    }
    
    /* 底部信息 */
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.8vw;
        margin-top: 1%;
    }
    
    /* 关键修复：确保Streamlit组件在正确层级显示 */
    .stFileUploader {
        width: 100% !important;
        height: 100% !important;
        position: relative !important;
        z-index: 3 !important;
    }
    
    .stFileUploader label {
        display: none !important;
    }
    
    .stFileUploader div {
        border: none !important;
        background-color: transparent !important;
        padding: 0 !important;
        width: 100% !important;
        height: 100% !important;
        position: relative !important;
        z-index: 3 !important;
    }
    
    /* 修复按钮显示 */
    .stButton {
        position: relative !important;
        z-index: 3 !important;
    }
    
    .stButton button {
        position: relative !important;
        z-index: 3 !important;
    }
    
    /* 图片样式 */
    img {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
        position: relative;
        z-index: 3;
    }
    
    /* 确保所有内容在正确层级 */
    [data-testid="stVerticalBlock"] {
        position: relative !important;
        z-index: 3 !important;
    }
    
    .stColumn {
        position: relative !important;
        z-index: 3 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 创建层面0：灰色背景
st.markdown('<div class="layer-0"></div>', unsafe_allow_html=True)

# 创建层面1：白色工作区
st.markdown('<div class="layer-1">', unsafe_allow_html=True)

# 标题区域
st.markdown('''
<div class="title-section">
    <div class="main-title">🎨 AI图片风格融合工具</div>
</div>
''', unsafe_allow_html=True)

# 图片框容器
st.markdown('<div class="image-container">', unsafe_allow_html=True)

# 使用Streamlit的columns创建横向布局
col1, col2, col3, col4, col5 = st.columns([1, 0.05, 1, 0.05, 1])

# 内容图片框
with col1:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    content_image = st.file_uploader(
        "内容图片",
        type=['png', 'jpg', 'jpeg'],
        key="content",
        label_visibility="collapsed"
    )
    if content_image:
        image = Image.open(content_image)
        st.image(image)
    else:
        st.markdown('''
        <div style="text-align: center; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 3vw; color: #4CAF50;">📷</div>
            <div class="box-text">内容图片</div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 加号1
with col2:
    st.markdown('<div class="operator">+</div>', unsafe_allow_html=True)

# 风格图片框
with col3:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    style_image = st.file_uploader(
        "风格图片", 
        type=['png', 'jpg', 'jpeg'],
        key="style",
        label_visibility="collapsed"
    )
    if style_image:
        image = Image.open(style_image)
        st.image(image)
    else:
        st.markdown('''
        <div style="text-align: center; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 3vw; color: #4CAF50;">🎨</div>
            <div class="box-text">风格图片</div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 加号2
with col4:
    st.markdown('<div class="operator">=</div>', unsafe_allow_html=True)

# 结果图片框
with col5:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    if 'result_image' in st.session_state and st.session_state.result_image:
        st.image(st.session_state.result_image, caption="融合结果")
    else:
        st.markdown('''
        <div style="text-align: center; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 3vw; color: #4CAF50;">✨</div>
            <div class="box-text">融合结果</div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 关闭图片框容器

# 生成按钮
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button("一键生成", key="generate_btn", use_container_width=False):
    if content_image and style_image:
        # 模拟生成过程
        with st.spinner("正在生成融合图片..."):
            # 这里添加实际的风格融合代码
            # 暂时使用占位图
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

# 关闭层面1
st.markdown('</div>', unsafe_allow_html=True)

# 初始化session state
if 'result_image' not in st.session_state:
    st.session_state.result_image = None




