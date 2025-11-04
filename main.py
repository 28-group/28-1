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

# 自定义CSS - 修复按钮和覆盖图显示
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
        line-height: 1.5;  /* 确保文字垂直居中 */
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
        z-index: 4;  /* 提高层级确保可见 */
        border-top: 1px solid #f0f0f0;
    }
    
    /* 确保组件可见 */
    .stFileUploader, .stButton, .stImage, .stSpinner, .stSuccess, .stWarning {
        position: relative !important;
        z-index: 3 !important;
    }
    
    /* 隐藏长条上传提示 */
    .stFileUploader > div > div:first-child {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
    }
    
    .stFileUploader > div > button {
        display: block !important;
        visibility: visible !important;
        background-color: #4CAF50 !important;
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
        padding: 6px 12px !important;
        font-size: 0.9vw !important;
        cursor: pointer !important;
        margin: 10px auto 0 !important;
    }
    
    .stFileUploader > div,
    .stFileUploader {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        height: auto !important;
    }
    
    .stColumn, [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
        position: relative !important;
        z-index: 3 !important;
    }
    
    img {
        max-width: 30%;  /* 调整图片大小确保可见 */
        max-height: 30%;
        object-fit: contain;
    }

    /* 右上角按钮样式 */
    .top-right-button {
        position: fixed !important;
        top: 20px !important;
        right: 20px !important;
        z-index: 4 !important;  /* 确保覆盖layer-1 */
        background-color: #4CAF50 !important;
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
        padding: 8px 16px !important;
        font-size: 1vw !important;
        cursor: pointer !important;
    }

    .top-right-button:hover {
        background-color: #388E3C !important;
    }

    /* 覆盖层样式 */
    .overlay-image {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        z-index: 2.5 !important;  /* 介于layer-1和layer-2之间 */
        object-fit: cover !important;
        opacity: 0.8 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 初始化覆盖层图片状态
if 'overlay_image' not in st.session_state:
    st.session_state.overlay_image = None

# 层级结构
st.markdown('<div class="layer-0"></div>', unsafe_allow_html=True)
st.markdown('<div class="layer-1"></div>', unsafe_allow_html=True)
st.markdown('<div class="layer-2">', unsafe_allow_html=True)

# 右上角上传按钮
st.markdown(
    f"""
    <button class="top-right-button" onclick="document.getElementById('overlay-upload').click()">
        上传覆盖图
    </button>
    """,
    unsafe_allow_html=True
)

# 隐藏的文件上传组件（用于右上角按钮触发）
overlay_upload = st.file_uploader(
    "上传覆盖图",
    type=['png', 'jpg', 'jpeg'],
    key="overlay",
    label_visibility="hidden",
    on_change=lambda: st.session_state.update({"overlay_image": overlay_upload})
)

# 显示覆盖层图片
if st.session_state.overlay_image:
    image_bytes = st.session_state.overlay_image.read()
    st.markdown(
        f"""
        <img src="data:image/jpeg;base64,{image_bytes}" class="overlay-image" id="overlay-img">
        """,
        unsafe_allow_html=True
    )
    # 重置文件读取指针
    st.session_state.overlay_image.seek(0)

# 标题区域 - 确保正确显示
st.markdown('''
<div class="title-section">
    <div class="main-title">🎨 AI图片风格融合</div>
</div>
''', unsafe_allow_html=True)

# 图片框容器
st.markdown('<div class="image-container">', unsafe_allow_html=True)

# 横向布局
col1, col2, col3, col4, col5 = st.columns([1, 0.04, 1, 0.04, 1])

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

# 底部使用说明 - 确保正确显示
st.markdown('''
<div class="footer">
    使用说明：上传内容图片和风格图片，点击生成按钮即可获得风格融合后的图片
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 关闭layer-2

# 初始化session state
if 'result_image' not in st.session_state:
    st.session_state.result_image = None