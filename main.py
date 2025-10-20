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

# 自定义CSS - 重新规划组件大小和位置
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
    
    /* 第2层级：白色工作区 */
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
    }
    
    /* 第3层级：透明组件容器 */
    .layer-2 {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 70%;
        height: 70%;
        z-index: 3;
        padding: 3%; /* 增加内边距给组件更多空间 */
        display: flex;
        flex-direction: column;
        background-color: transparent;
        pointer-events: auto;
        box-sizing: border-box;
    }
    
    /* 标题区域 - 调整大小 */
    .title-section {
        text-align: center;
        margin-bottom: 3%; /* 增加间距 */
        padding-bottom: 2%;
        border-bottom: 1px solid #f0f0f0;
        width: 100%;
        height: 8%; /* 固定标题区域高度 */
    }
    
    .main-title {
        font-size: 2.2vw; /* 增大标题字体 */
        font-weight: bold;
        color: #ff69b4;
        margin: 0;
    }
    
    /* 图片框容器 - 重新规划大小和位置 */
    .image-container {
        flex: 1;
        display: flex;
        justify-content: space-between; /* 均匀分布三个框 */
        align-items: center;
        gap: 3%; /* 增加间距 */
        padding: 0 2%;
        width: 100%;
        box-sizing: border-box;
        height: 60%; /* 固定图片区域高度 */
    }
    
    /* 单个图片框样式 - 重新调整大小 */
    .image-box {
        width: 26%; /* 调整宽度，保持3:2比例 */
        height: 80%; /* 相对于容器的高度 */
        border: 2px dashed #4CAF50;
        border-radius: 12px; /* 稍微增大圆角 */
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #f1f8e9;
        transition: all 0.3s ease;
        padding: 3%; /* 增加内边距 */
        position: relative;
        box-sizing: border-box;
    }
    
    .image-box:hover {
        border-color: #388E3C;
        background-color: #dcedc8;
        transform: translateY(-3px); /* 增强悬停效果 */
    }
    
    .box-text {
        color: #2E7D32;
        font-size: 1.2vw; /* 增大文字 */
        text-align: center;
        margin-top: 10px;
    }
    
    /* 加号样式 - 调整大小和位置 */
    .operator {
        font-size: 2.5vw; /* 增大运算符 */
        color: #6b7280;
        font-weight: 300;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }
    
    /* 按钮容器 - 重新调整 */
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 2%;
        padding-top: 2%;
        border-top: 1px solid #f0f0f0;
        width: 100%;
        box-sizing: border-box;
        height: 15%; /* 固定按钮区域高度 */
    }
    
    .generate-button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 10px; /* 增大圆角 */
        padding: 12px 30px;
        font-size: 1.3vw; /* 增大按钮文字 */
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 35%; /* 调整按钮宽度 */
        max-width: 220px;
        height: 60%; /* 相对于容器高度 */
        box-sizing: border-box;
    }
    
    .generate-button:hover {
        background-color: #2563eb;
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(37, 99, 235, 0.3);
    }
    
    /* 底部信息 - 调整大小 */
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.9vw; /* 稍微增大底部文字 */
        margin-top: 1%;
        width: 100%;
        box-sizing: border-box;
        height: 5%; /* 固定底部区域高度 */
    }
    
    /* 强制所有Streamlit组件在第3层级显示 */
    .stFileUploader, .stButton, .stImage, .stSpinner, .stSuccess, .stWarning {
        position: relative !important;
        z-index: 3 !important;
        box-sizing: border-box !important;
    }
    
    .stFileUploader label {
        display: none !important;
    }
    
    .stFileUploader div {
        border: none !important;
        background-color: transparent !important;
        padding: 0 !important;
        width: 100%;
        height: 100%;
        box-sizing: border-box !important;
    }
    
    /* 确保所有列和块都在第3层级 */
    .stColumn, [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
        position: relative !important;
        z-index: 3 !important;
        box-sizing: border-box !important;
    }
    
    /* 图片样式 */
    img {
        max-width: 90%;
        max-height: 90%;
        object-fit: contain;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 第1层级：灰色背景
st.markdown('<div class="layer-0"></div>', unsafe_allow_html=True)

# 第2层级：白色工作区
st.markdown('<div class="layer-1"></div>', unsafe_allow_html=True)

# 第3层级：透明组件容器
st.markdown('<div class="layer-2">', unsafe_allow_html=True)

# 标题区域
st.markdown('''
<div class="title-section">
    <div class="main-title">🎨 AI图片风格融合工具</div>
</div>
''', unsafe_allow_html=True)

# 图片框容器
st.markdown('<div class="image-container">', unsafe_allow_html=True)

# 使用Streamlit的columns创建横向布局 - 调整比例
col1, col2, col3, col4, col5 = st.columns([26, 3, 26, 3, 26])  # 调整列比例

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
            <div style="font-size: 3.5vw; color: #4CAF50;"></div>
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
            <div style="font-size: 3.5vw; color: #4CAF50;"></div>
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
            <div style="font-size: 3.5vw; color: #4CAF50;"></div>
            <div class="box-text">融合结果</div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 关闭图片框容器

# 生成按钮
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button("🚀 一键生成风格融合", key="generate_btn", use_container_width=False):
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

# 关闭第3层级
st.markdown('</div>', unsafe_allow_html=True)  # 关闭layer-2（第3层级）

# 初始化session state
if 'result_image' not in st.session_state:
    st.session_state.result_image = None




