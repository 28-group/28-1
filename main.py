import streamlit as st
from PIL import Image
import io

st.set_page_config(
    page_title="AI画家 - 图片风格融合",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
    }
    
    #MainMenu, footer, header {visibility: hidden !important;}
    
    /* 白色区域和层级样式 */
    .layer-0 {
        background-color: #808080;
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1;
    }
    
    .layer-1, .layer-2 {
        width: 70% !important;
        height: 70% !important;
        padding: 2% !important;
        box-sizing: border-box !important;
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
    
    /* 图片容器间距压缩 */
    [data-testid="stHorizontalBlock"] {
        gap: 0.2% !important;
        padding: 0 1% !important;
        justify-content: center !important;
    }
    
    /* 图片框样式 */
    .image-box {
        width: 35% !important;
        aspect-ratio: 2/3 !important;
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        background-color: #f1f8e9;
        padding: 1% !important;
        box-sizing: border-box !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    /* 运算符区域压缩 */
    [data-testid="column"]:nth-child(2),
    [data-testid="column"]:nth-child(4) {
        width: 2% !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .operator {
        font-size: 2.5vw !important;
        text-align: center !important;
        margin: 0 !important;
    }
    
    /* 核心修改：隐藏上传提示，仅保留浏览按钮 */
    .stFileUploader {
        width: 100% !important;
        margin-top: 10px !important;  /* 按钮与图片框的距离 */
    }
    
    /* 隐藏"Drag and drop file here"提示文字 */
    .stFileUploader label div:nth-child(2) {
        display: none !important;
    }
    
    /* 隐藏上传图标 */
    .stFileUploader label div:nth-child(1) {
        display: none !important;
    }
    
    /* 仅保留"Browse files"按钮，并调整样式 */
    .stFileUploader label {
        display: flex !important;
        justify-content: center !important;
        padding: 0 !important;
    }
    
    .stFileUploader button {
        background-color: #4CAF50 !important;  /* 按钮颜色 */
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
        padding: 6px 12px !important;  /* 小按钮尺寸 */
        font-size: 0.9vw !important;
        cursor: pointer !important;
    }
    
    /* 按钮hover效果 */
    .stFileUploader button:hover {
        background-color: #388E3C !important;
    }
    
    /* 结果框按钮样式 */
    .generate-button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.8% 2%;
        font-size: 1.1vw;
        font-weight: 600;
    }
    
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.8vw;
        margin-top: 1%;
        padding-top: 1%;
    }
    
    img {
        max-width: 90% !important;
        max-height: 70% !important;
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
with st.container():
    col1, col2, col3, col4, col5 = st.columns([1, 0.01, 1, 0.01, 1])

    # 内容图片框
    with col1:
        st.markdown('<div class="image-box">', unsafe_allow_html=True)
        # 显示"内容图片"文字提示
        st.markdown('<div class="box-text">内容图片</div>', unsafe_allow_html=True)
        # 文件上传组件（仅显示Browse按钮）
        content_image = st.file_uploader(
            "内容图片",
            type=['png', 'jpg', 'jpeg'],
            key="content",
            label_visibility="collapsed"
        )
        # 上传后显示图片
        if content_image:
            st.image(Image.open(content_image))
        st.markdown('</div>', unsafe_allow_html=True)

    # 加号
    with col2:
        st.markdown('<div class="operator">+</div>', unsafe_allow_html=True)

    # 风格图片框
    with col3:
        st.markdown('<div class="image-box">', unsafe_allow_html=True)
        st.markdown('<div class="box-text">风格图片</div>', unsafe_allow_html=True)
        style_image = st.file_uploader(
            "风格图片",
            type=['png', 'jpg', 'jpeg'],
            key="style",
            label_visibility="collapsed"
        )
        if style_image:
            st.image(Image.open(style_image))
        st.markdown('</div>', unsafe_allow_html=True)

    # 等号
    with col4:
        st.markdown('<div class="operator">=</div>', unsafe_allow_html=True)

    # 结果图片框
    with col5:
        st.markdown('<div class="image-box">', unsafe_allow_html=True)
        st.markdown('<div class="box-text">融合结果</div>', unsafe_allow_html=True)
        if 'result_image' in st.session_state and st.session_state.result_image:
            st.image(st.session_state.result_image, caption="融合结果")
        st.markdown('</div>', unsafe_allow_html=True)

        # 一键生成按钮
        st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
        if st.button("一键生成", key="generate_btn", use_container_width=True):
            if content_image and style_image:
                with st.spinner("正在生成融合图片..."):
                    st.session_state.result_image = "https://via.placeholder.com/400x300/4CAF50/FFFFFF?text=融合结果"
                    st.success("风格融合完成！")
                    st.rerun()
            else:
                st.warning("请先上传内容图片和风格图片")

# 底部说明
st.markdown('''
<div class="footer">
    使用说明：上传内容图片和风格图片，点击生成按钮即可获得风格融合后的图片
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

if 'result_image' not in st.session_state:
    st.session_state.result_image = None