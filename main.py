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

# 自定义CSS - 重点解决图片显示问题
st.markdown(
    """
    <style>
    /* 基础布局设置 */
    html, body {
        overflow: hidden !important;
    }
    
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
    }
    
    .layer-2 {
        position: relative;
        z-index: 3;
        height: 100%;
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
    
    /* 图片容器 */
    .image-container {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2%;
        padding: 1%;
    }
    
    /* 图片框样式 - 关键修改 */
    .image-box {
        width: 30%;
        aspect-ratio: 2/3;
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        background-color: #f1f8e9;
        position: relative; /* 相对定位作为容器 */
        overflow: hidden;
    }
    
    .image-box:hover {
        border-color: #388E3C;
        background-color: #dcedc8;
    }
    
    /* 上传组件样式 - 关键修改 */
    .upload-container {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 4;
    }
    
    /* 提示文字 */
    .box-text {
        color: #2E7D32;
        font-size: 1vw;
        text-align: center;
        margin: 0;
    }
    
    /* 运算符样式 */
    .operator {
        font-size: 3vw;
        color: #6b7280;
        font-weight: 400;
        margin: 0;
    }
    
    /* 生成按钮区域 */
    .generate-btn {
        margin-top: 1%;
        text-align: center;
    }
    
    /* 底部说明 */
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.8vw;
        margin-top: 1%;
        padding-top: 1%;
        border-top: 1px solid #f0f0f0;
    }
    
    /* 确保图片可见的关键样式 */
    .uploaded-image {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        object-fit: contain !important;
        z-index: 5 !important; /* 图片层级最高 */
    }
    
    /* 隐藏Streamlit上传组件的默认样式 */
    [data-testid="stFileUploader"] {
        width: 80% !important;
    }
    
    [data-testid="stFileUploader"] > div {
        border: none !important;
        background-color: transparent !important;
        padding: 0 !important;
    }
    
    [data-testid="stFileUploader"] label {
        display: none !important;
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
col1, col2, col3, col4, col5 = st.columns([3, 0.5, 3, 0.5, 3])

# 内容图片框 - 关键修改
with col1:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    # 上传容器
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    content_image = st.file_uploader(
        "内容图片",
        type=['png', 'jpg', 'jpeg'],
        key="content",
        label_visibility="collapsed"
    )
    # 显示提示文字（未上传时）
    if not content_image:
        st.markdown('<p class="box-text">点击上传内容图片</p>', unsafe_allow_html=True)
    # 显示上传的图片
    if content_image:
        image = Image.open(content_image)
        # 为图片添加特定类名确保样式生效
        st.image(image, use_column_width=True, output_format='PNG', 
                 caption="", clamp=True)
    st.markdown('</div>', unsafe_allow_html=True)  # 关闭upload-container
    st.markdown('</div>', unsafe_allow_html=True)  # 关闭image-box

# 加号
with col2:
    st.markdown('<p class="operator">+</p>', unsafe_allow_html=True)

# 风格图片框 - 关键修改
with col3:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    style_image = st.file_uploader(
        "风格图片",
        type=['png', 'jpg', 'jpeg'],
        key="style",
        label_visibility="collapsed"
    )
    if not style_image:
        st.markdown('<p class="box-text">点击上传风格图片</p>', unsafe_allow_html=True)
    if style_image:
        image = Image.open(style_image)
        st.image(image, use_column_width=True, output_format='PNG',
                 caption="", clamp=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 等号
with col4:
    st.markdown('<p class="operator">=</p>', unsafe_allow_html=True)

# 结果图片框
with col5:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    if 'result_image' in st.session_state and st.session_state.result_image:
        st.image(st.session_state.result_image, use_column_width=True,
                 caption="融合结果", clamp=True)
    else:
        st.markdown('<p class="box-text">融合结果将显示在这里</p>', unsafe_allow_html=True)
    
    # 生成按钮
    st.markdown('<div class="generate-btn">', unsafe_allow_html=True)
    if st.button("一键生成", key="generate_btn", use_container_width=True):
        if content_image and style_image:
            with st.spinner("正在生成融合图片..."):
                # 使用符合比例的占位图
                st.session_state.result_image = "https://via.placeholder.com/400x600/4CAF50/FFFFFF?text=融合结果"
                st.success("风格融合完成！")
                st.rerun()
        else:
            st.warning("请先上传内容图片和风格图片")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 关闭image-container

# 底部说明
st.markdown('''
<div class="footer">
    使用说明：上传内容图片和风格图片，点击生成按钮即可获得风格融合后的图片
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 关闭layer-2

# 初始化session state
if 'result_image' not in st.session_state:
    st.session_state.result_image = None