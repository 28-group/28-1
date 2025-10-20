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

# 自定义CSS - 修复布局问题
st.markdown(
    """
    <style>
    /* 隐藏所有Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {display: none;}
    
    /* 重置主容器样式 */
    .stApp {
        background-color: #808080 !important; /* 层面0：灰色背景 */
        min-height: 100vh;
        margin: 0;
        padding: 0;
    }
    
    /* 隐藏所有默认的块容器 */
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* 层面1：白色工作区容器 */
    .white-container {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        width: 66.666vw;
        height: 66.666vh;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        display: flex;
        flex-direction: column;
        padding: 2%;
        z-index: 2;
    }
    
    /* 标题区域 */
    .title-section {
        text-align: center;
        margin-bottom: 2%;
        padding-bottom: 2%;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .main-title {
        font-size: 2vw;
        font-weight: bold;
        color: #ff69b4;
        margin: 0;
    }
    
    /* 三个图片框的主容器 */
    .boxes-container {
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
    }
    
    .image-box:hover {
        border-color: #3b82f6;
        background-color: rgba(59, 130, 246, 0.05);
    }
    
    .box-text {
        color: #6b7280;
        font-size: 1.2vw;
        text-align: center;
        margin-top: 10px;
    }
    
    /* 加号样式 */
    .operator {
        font-size: 2.5vw;
        color: #6b7280;
        font-weight: 300;
    }
    
    /* 按钮容器 */
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 2%;
    }
    
    .generate-btn {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 40px;
        font-size: 1.2vw;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 30%;
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
        margin-top: 2%;
        padding-top: 2%;
        border-top: 1px solid #f0f0f0;
    }
    
    /* 文件上传器样式调整 */
    .stFileUploader > label {
        display: none;
    }
    
    .stFileUploader > div {
        border: none !important;
        background: transparent !important;
    }
    
    /* 确保没有滚动条 */
    html, body, [data-testid="stAppViewContainer"] {
        height: 100%;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 使用Streamlit的列布局来创建白色层面1
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # 白色层面1容器
    st.markdown('<div class="white-container">', unsafe_allow_html=True)
    
    # 标题区域
    st.markdown('''
    <div class="title-section">
        <div class="main-title">🎨 AI图片风格融合工具</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # 三个图片框容器
    st.markdown('<div class="boxes-container">', unsafe_allow_html=True)
    
    # 使用Streamlit列来创建三个框
    box_col1, op1, box_col2, op2, box_col3 = st.columns([1, 0.1, 1, 0.1, 1])
    
    with box_col1:
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
            <div style="text-align: center; padding: 20px;">
                <div style="font-size: 3vw; color: #6b7280;">📷</div>
                <div class="box-text">内容图片</div>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with op1:
        st.markdown('<div class="operator">+</div>', unsafe_allow_html=True)
    
    with box_col2:
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
            <div style="text-align: center; padding: 20px;">
                <div style="font-size: 3vw; color: #6b7280;">🎨</div>
                <div class="box-text">风格图片</div>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with op2:
        st.markdown('<div class="operator">=</div>', unsafe_allow_html=True)
    
    with box_col3:
        st.markdown('<div class="image-box">', unsafe_allow_html=True)
        if 'result_image' in st.session_state and st.session_state.result_image:
            st.image(st.session_state.result_image, use_column_width=True)
        else:
            st.markdown('''
            <div style="text-align: center; padding: 20px;">
                <div style="font-size: 3vw; color: #6b7280;">✨</div>
                <div class="box-text">融合结果</div>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # 关闭boxes-container
    
    # 生成按钮
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("🚀 一键生成", key="generate_btn", use_container_width=True):
        if content_image and style_image:
            with st.spinner("正在生成融合图片..."):
                # 这里添加实际的风格融合代码
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

# 初始化session state
if 'result_image' not in st.session_state:
    st.session_state.result_image = None