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

# 自定义CSS - 修复图片显示位置问题
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
    
    /* 层级样式 */
    .layer-0 {
        background-color: #808080;
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1;
    }
    
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
    }
    
    .layer-2 {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 70%;
        height: 70%;
        z-index: 3;
        padding: 2%;
        display: flex;
        flex-direction: column;
        background-color: transparent;
        pointer-events: auto;
    }
    
    /* 标题区域 - 修复显示问题 */
    .title-section {
        text-align: center;
        margin-bottom: 2%;
        padding-bottom: 1%;
        border-bottom: 1px solid #f0f0f0;
        position: relative;
        z-index: 4;
    }
    
    .main-title {
        font-size: 1.8vw;
        font-weight: bold;
        color: #ff69b4;
        margin: 0;
        line-height: 1.5;
    }
    
    .image-container {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5% !important;
        padding: 0.2% !important;
        position: relative;
        z-index: 3;
    }
    
    .image-box {
        width: 35%;
        aspect-ratio: 2/3;
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
        overflow: visible !important;  /* 允许内容溢出，便于图片定位 */
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
    
    .operator {
        font-size: 3vw;
        color: #6b7280;
        font-weight: 400;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 1%;
        padding-top: 1%;
        border-top: 1px solid #f0f0f0;
        position: relative;
        z-index: 3;
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
        max-width: 100px;
    }
    
    .generate-button:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
    }
    
    /* 底部说明 - 修复显示问题 */
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.8vw;
        margin-top: 1%;
        padding-top: 1%;
        position: relative;
        z-index: 4;
        border-top: 1px solid #f0f0f0;
    }
    
    /* 关键修改：强制图片在图片框内部显示 */
    .image-box-wrapper {
        position: relative;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    /* 图片容器 - 绝对定位在图片框内部 */
    .image-preview-container {
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 90% !important;
        height: 90% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        z-index: 10 !important;
    }
    
    /* 上传的图片样式 */
    .image-preview-container img {
        max-width: 100% !important;
        max-height: 100% !important;
        object-fit: contain !important;
        border-radius: 8px !important;
        position: relative !important;
        z-index: 11 !important;
    }
    
    /* 文件上传器样式 - 隐藏默认显示，但保持功能 */
    .stFileUploader {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important;
        z-index: 20 !important;
        cursor: pointer !important;
    }
    
    .stFileUploader label {
        display: none !important;
    }
    
    .stFileUploader > div {
        width: 100% !important;
        height: 100% !important;
        border: none !important;
        background: transparent !important;
    }
    
    .stFileUploader button {
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important;
    }
    
    /* 占位内容样式 */
    .placeholder-content {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        z-index: 5;
        pointer-events: none;
    }
    
    .stColumn, [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
        position: relative !important;
        z-index: 3 !important;
    }
    
    /* 确保图片组件使用我们的容器 */
    .stImage {
        max-width: 100% !important;
        max-height: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 层级结构
st.markdown('<div class="layer-0"></div>', unsafe_allow_html=True)
st.markdown('<div class="layer-1"></div>', unsafe_allow_html=True)
st.markdown('<div class="layer-2">', unsafe_allow_html=True)

# 标题区域
st.markdown('''
<div class="title-section">
    <div class="main-title">🎨 AI图片风格融合</div>
</div>
''', unsafe_allow_html=True)

# 图片框容器
st.markdown('<div class="image-container">', unsafe_allow_html=True)

# 横向布局
col1, col2, col3, col4, col5 = st.columns([1, 0.04, 1, 0.04, 1])

# 辅助函数：创建图片显示
def create_image_display(uploaded_file, default_text, key):
    """创建图片显示，确保在图片框内部"""
    # 创建包装容器
    st.markdown(f'<div class="image-box-wrapper" id="wrapper_{key}">', unsafe_allow_html=True)
    
    if uploaded_file:
        # 如果已上传图片，在图片预览容器中显示
        st.markdown('<div class="image-preview-container">', unsafe_allow_html=True)
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # 如果未上传图片，显示占位内容
        st.markdown(f'''
        <div class="placeholder-content">
            <div style="font-size: 3vw; color: #4CAF50;">📁</div>
            <div class="box-text">{default_text}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 内容图片框
with col1:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    
    # 先创建图片显示
    content_image = st.file_uploader(
        "内容图片",
        type=['png', 'jpg', 'jpeg'],
        key="content",
        label_visibility="collapsed"
    )
    create_image_display(content_image, "内容图片", "content")
    
    st.markdown('</div>', unsafe_allow_html=True)

# 加号
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
    create_image_display(style_image, "风格图片", "style")
    
    st.markdown('</div>', unsafe_allow_html=True)

# 等号
with col4:
    st.markdown('<div class="operator">=</div>', unsafe_allow_html=True)

# 结果图片框
with col5:
    with st.container():
        st.markdown('<div class="image-box">', unsafe_allow_html=True)
        
        if 'result_image' in st.session_state and st.session_state.result_image:
            # 显示结果图片
            st.markdown('<div class="image-preview-container">', unsafe_allow_html=True)
            st.image(st.session_state.result_image, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # 如果未生成结果，显示占位内容
            st.markdown('''
            <div class="placeholder-content">
                <div style="font-size: 3vw; color: #4CAF50;">✨</div>
                <div class="box-text">融合结果</div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("一键生成", key="generate_btn", use_container_width=True):
                if content_image and style_image:
                    with st.spinner("正在生成融合图片..."):
                        st.session_state.result_image = "https://via.placeholder.com/400x300/4CAF50/FFFFFF?text=融合结果"
                        st.success("风格融合完成！")
                        st.rerun()
                else:
                    st.warning("请先上传内容图片和风格图片")

st.markdown('</div>', unsafe_allow_html=True)  # 关闭image-container

# 底部使用说明
st.markdown('''
<div class="footer">
    使用说明：点击图片框上传内容图片和风格图片，点击生成按钮即可获得风格融合后的图片
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 关闭layer-2

# 初始化session state
if 'result_image' not in st.session_state:
    st.session_state.result_image = None