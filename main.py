import streamlit as st
from PIL import Image
import io

# 页面配置 - 使用居中布局
st.set_page_config(
    page_title="AI画家 - 图片风格融合",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定义CSS - 实现层面覆盖效果
st.markdown(
    """
    <style>
    /* 全局样式重置 */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* 确保页面占满整个屏幕 */
    html, body {
        height: 100%;
        width: 100%;
        overflow: hidden;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 主容器样式 */
    .stApp {
        height: 100vh;
        width: 100vw;
        overflow: hidden;
        position: relative;
    }
    
    /* 层面0：灰色背景层 - 完全覆盖屏幕 */
    .layer-0 {
        background-color: #808080;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 1;
    }
    
    /* 层面1：白色工作区 - 居中放置，大小为层面0的2/3 */
    .layer-1 {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 66.666%; /* 2/3 宽度 */
        height: 66.666%; /* 2/3 高度 */
        z-index: 2;
        padding: 2%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
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
        color: #ff69b4; /* 粉红色 */
        margin: 0;
    }
    
    /* 三个图片框的主容器 */
    .boxes-main-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex: 1;
        padding: 0 5%;
        margin: 2% 0;
    }
    
    /* 单个图片框样式 */
    .image-box {
        width: 28%;
        aspect-ratio: 3/2;
        border: 2px dashed #d1d5db;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #f8f9fa;
        transition: all 0.3s ease;
        position: relative;
        z-index: 3;
    }
    
    .image-box:hover {
        border-color: #3b82f6;
        background-color: rgba(59, 130, 246, 0.05);
    }
    
    .box-text {
        color: #6b7280;
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
        margin-top: 2%;
        padding-bottom: 2%;
        position: relative;
        z-index: 3;
    }
    
    .generate-button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 1% 3%;
        font-size: 1.2vw;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 30%;
        max-width: 200px;
        height: 5vh;
        display: flex;
        align-items: center;
        justify-content: center;
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
        padding-top: 1%;
        border-top: 1px solid #f0f0f0;
    }
    
    /* 文件上传按钮样式 */
    .stFileUploader label {
        display: none !important;
    }
    
    .stFileUploader div {
        border: none !important;
        background-color: transparent !important;
        padding: 0 !important;
    }
    
    /* 图片样式 */
    img {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 创建主容器
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# 层面0：灰色背景
st.markdown('<div class="layer-0"></div>', unsafe_allow_html=True)

# 层面1：白色工作区
st.markdown('<div class="layer-1">', unsafe_allow_html=True)

# 标题区域
st.markdown('''
<div class="title-section">
    <div class="main-title">🎨 AI图片风格融合工具</div>
</div>
''', unsafe_allow_html=True)

# 三个图片框的主容器
st.markdown('<div class="boxes-main-container">', unsafe_allow_html=True)

# 内容图片框
col1, plus1, col2, plus2, col3 = st.columns([1, 0.05, 1, 0.05, 1])

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
        <div style="text-align: center;">
            <div style="font-size: 3vw; color: #6b7280;"></div>
            <div class="box-text">内容图片</div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with plus1:
    st.markdown('<div class="operator">+</div>', unsafe_allow_html=True)

with col2:
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
        <div style="text-align: center;">
            <div style="font-size: 3vw; color: #6b7280;"></div>
            <div class="box-text">风格图片</div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with plus2:
    st.markdown('<div class="operator">=</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    if 'result_image' in st.session_state and st.session_state.result_image:
        st.image(st.session_state.result_image, caption="融合结果")
    else:
        st.markdown('''
        <div style="text-align: center;">
            <div style="font-size: 3vw; color: #6b7280;">✨</div>
            <div class="box-text">融合结果</div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 关闭boxes-main-container

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
st.markdown('</div>', unsafe_allow_html=True)  # 关闭layer-1

# 关闭主容器
st.markdown('</div>', unsafe_allow_html=True)  # 关闭main-container

# 初始化session state
if 'result_image' not in st.session_state:
    st.session_state.result_image = None