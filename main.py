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

# 自定义CSS - 强制缩小间距（使用更精确的选择器和!important增强优先级）
st.markdown(
    """
    <style>
    /* 基础样式保持不变 */
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
    
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    
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
    
    /* 标题区域 */
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
    
    /* 核心修改：强制缩小容器间距 */
    .image-container {
        flex: 1;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 0.5% !important;  /* 强制缩小到原间距的1/4 */
        padding: 0 1% !important;  /* 左右内边距减小 */
        position: relative;
        z-index: 3;
        width: 100% !important;
    }
    
    /* 图片框样式 */
    .image-box {
        width: 32% !important;  /* 略微增加宽度以填充空间 */
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
    }
    
    /* 运算符样式调整 */
    .operator {
        font-size: 2.5vw !important;  /* 进一步缩小运算符 */
        color: #6b7280;
        font-weight: 400;
        margin: 0 !important;  /* 清除默认外边距 */
        padding: 0 !important;
        text-align: center;
    }
    
    /* 按钮和底部说明样式保持不变 */
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
    }
    
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
    
    /* 确保文件上传组件不占用额外空间 */
    .stFileUploader {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stFileUploader div {
        width: 100% !important;
        height: auto !important;
    }
    
    /* 调整列布局 */
    [data-testid="column"] {
        padding: 0 !important;
        margin: 0 !important;
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

# 横向布局 - 进一步缩小运算符列宽
col1, col2, col3, col4, col5 = st.columns([1, 0.02, 1, 0.02, 1])  # 运算符列宽缩至0.02

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
            <div style="font-size: 3vw; color: #4CAF50;"></div>
            <div class="box-text">内容图片</div>
        </div>
        ''', unsafe_allow_html=True)
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
    if style_image:
        image = Image.open(style_image)
        st.image(image)
    else:
        st.markdown('''
        <div style="text-align: center; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 3vw; color: #4CAF50;"></div>
            <div class="box-text">风格图片</div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 等号
with col4:
    st.markdown('<div class="operator">=</div>', unsafe_allow_html=True)

# 结果图片框
with col5:
    with st.container():
        st.markdown('<div class="image-box">', unsafe_allow_html=True)
        if 'result_image' in st.session_state and st.session_state.result_image:
            st.image(st.session_state.result_image, caption="融合结果")
        else:
            st.markdown('''
            <div style="text-align: center; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size: 3vw; color: #4CAF50;"></div>
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
    使用说明：上传内容图片和风格图片，点击生成按钮即可获得风格融合后的图片
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 关闭layer-2

# 初始化session state
if 'result_image' not in st.session_state:
    st.session_state.result_image = None