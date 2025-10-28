import streamlit as st
from PIL import Image
import io
#test wu hao ming lai le
# 页面配置
st.set_page_config(
    page_title="AI画家 - 图片风格融合",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 修复后的CSS - 确保所有组件都在白色层级内
st.markdown(
    """
    <style>
    /* 彻底禁止页面滑动 */
    html, body, #root, [data-testid="stAppViewContainer"] {
        height: 100vh !important;
        width: 100vw !important;
        overflow: hidden !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stApp {
        height: 100vh !important;
        width: 100vw !important;
        overflow: hidden !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 第1层级：灰色背景层 */
    .layer-0 {
        background-color: #808080;
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1;
    }
    
    /* 第2层级：白色工作区 - 确保内部内容不溢出 */
    .layer-1 {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 70%;
        height: 70%;
        z-index: 2;
        padding: 2%;
        display: flex;
        flex-direction: column;
        /* 关键：确保内部内容被裁剪 */
        overflow: hidden !important;
    }
    
    /* 内部内容容器 - 限制在白色区域内 */
    .content-wrapper {
        flex: 1;
        display: flex;
        flex-direction: column;
        height: 100%;
        /* 确保内容不溢出白色区域 */
        overflow: hidden !important;
    }
    
    .title-section {
        text-align: center;
        margin-bottom: 2%;
        padding-bottom: 1%;
        border-bottom: 1px solid #f0f0f0;
        flex-shrink: 0;
    }
    
    .main-title {
        font-size: 1.8vw;
        font-weight: bold;
        color: #ff69b4;
        margin: 0;
    }
    
    .image-container {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2%;
        padding: 2%;
        /* 防止内容溢出 */
        min-height: 0;
        overflow: hidden;
    }
    
    .image-box {
        width: 28%;
        height: 100%;
        min-height: 150px;
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
        /* 确保内容在框内 */
        overflow: hidden;
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
        /* 确保文字可见 */
        z-index: 10;
        position: relative;
    }
    
    .operator {
        font-size: 2vw;
        color: #6b7280;
        font-weight: 300;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }
    
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: auto;
        padding-top: 1%;
        border-top: 1px solid #f0f0f0;
        flex-shrink: 0;
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
    
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.8vw;
        margin-top: 1%;
        flex-shrink: 0;
    }
    
    /* 关键修复：强制Streamlit组件在白色区域内 */
    [data-testid="stAppViewContainer"] > div {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        overflow: hidden !important;
    }
    
    /* 修复列布局 */
    .stColumn {
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        overflow: hidden !important;
    }
    
    /* 修复文件上传器 */
    .stFileUploader {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        z-index: 5 !important;
    }
    
    .stFileUploader > section {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        width: 100% !important;
        height: 100% !important;
    }
    
    .stFileUploader > section > div {
        width: 100% !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .stFileUploader label {
        display: none !important;
    }
    
    /* 修复按钮 */
    .stButton {
        position: relative !important;
        z-index: 5 !important;
    }
    
    .stButton > button {
        width: 100% !important;
    }
    
    /* 修复图片显示 */
    .stImage {
        max-width: 100% !important;
        max-height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .stImage img {
        max-width: 90% !important;
        max-height: 90% !important;
        object-fit: contain !important;
    }
    
    /* 修复消息组件 */
    .stSpinner, .stSuccess, .stWarning, .stError {
        position: relative !important;
        z-index: 10 !important;
        font-size: 0.9vw !important;
    }
    
    img {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 第1层级：灰色背景
st.markdown('<div class="layer-0"></div>', unsafe_allow_html=True)

# 第2层级：白色工作区
st.markdown('<div class="layer-1">', unsafe_allow_html=True)

# 内部内容包装器 - 新增：确保所有内容都在白色区域内
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# 标题区域
st.markdown('''
<div class="title-section">
    <div class="main-title">AI图片风格融合工具</div>
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
        try:
            image = Image.open(content_image)
            st.image(image, use_column_width=True)
        except Exception as e:
            st.error(f"图片加载失败: {e}")
    else:
        st.markdown('<div class="box-text">内容图片</div>', unsafe_allow_html=True)
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
        try:
            image = Image.open(style_image)
            st.image(image, use_column_width=True)
        except Exception as e:
            st.error(f"图片加载失败: {e}")
    else:
        st.markdown('<div class="box-text">风格图片</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 加号2
with col4:
    st.markdown('<div class="operator">=</div>', unsafe_allow_html=True)

# 结果图片框
with col5:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    if 'result_image' in st.session_state and st.session_state.result_image:
        st.image(st.session_state.result_image, use_column_width=True)
    else:
        st.markdown('<div class="box-text">融合结果</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 关闭图片框容器

# 生成按钮
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button("一键生成", key="generate_btn", use_container_width=False):
    if content_image and style_image:
        with st.spinner("正在生成融合图片..."):
            # 模拟生成过程
            import time
            time.sleep(2)
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

# 关闭内容包装器
st.markdown('</div>', unsafe_allow_html=True)

# 关闭第2层级
st.markdown('</div>', unsafe_allow_html=True)

# 初始化session state
if 'result_image' not in st.session_state:
    st.session_state.result_image = None