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

# 自定义CSS - 彻底解决横向布局和滑动问题
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
        background-color: transparent;
    }
    
    /* 修复Streamlit默认容器样式 */
    .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        overflow: hidden !important;
    }
    
    .main {
        padding: 0 !important;
        background-color: transparent !important;
        overflow: hidden !important;
    }
    
    /* 层面0：灰色背景层，完全覆盖屏幕 */
    .layer-0 {
        background-color: #808080;
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1;
    }
    
    /* 层面1：白色工作区，居中放置，大小为层面0的2/3 */
    .layer-1 {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 66.666vw;
        height: 66.666vh;
        z-index: 2;
        padding: 2%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        overflow: hidden !important;
    }
    
    /* 标题区域 */
    .title-section {
        text-align: center;
        margin: 0 0 2% 0;
        padding-bottom: 1%;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .main-title {
        font-size: 1.8vw;
        font-weight: bold;
        color: #ff69b4; /* 粉红色 */
        margin: 0;
    }
    
    /* 三个图片框的主容器 - 使用Flexbox布局 */
    .boxes-main-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex: 1;
        padding: 0 5%;
        margin: 2% 0;
        position: relative;
        z-index: 3;
        width: 100%;
        height: auto;
        overflow: hidden !important;
    }
    
    /* 单个图片框样式 - 绿色主题 */
    .image-box {
        width: 28%; /* 每个框占容器宽度的28% */
        max-width: 180px; /* 最大宽度限制 */
        aspect-ratio: 3/2; /* 保持3:2的长宽比 */
        border: 2px dashed #4CAF50; /* 绿色边框 */
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #f1f8e9; /* 浅绿色背景 */
        transition: all 0.3s ease;
        position: relative;
        z-index: 4;
    }
    
    .image-box:hover {
        border-color: #388E3C; /* 深绿色边框（悬停时） */
        background-color: #dcedc8; /* 深一点的绿色背景（悬停时） */
    }
    
    .box-text {
        color: #2E7D32; /* 绿色文字 */
        font-size: 1vw;
        text-align: center;
        margin-top: 8px;
    }
    
    /* 加号样式 */
    .operator {
        font-size: 2vw;
        color: #6b7280;
        font-weight: 300;
        text-align: center;
        position: relative;
        z-index: 3;
        width: 5%; /* 加号区域宽度 */
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
        background-color: #3b82f6; /* 蓝色，按钮颜色 */
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
        background-color: #2563eb; /* 深蓝色，鼠标悬停时的按钮颜色 */
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
    .stFileUploader {
        width: 100%;
        height: 100%;
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
    }
    
    /* 图片样式 */
    img {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }
    
    /* 确保所有元素都在可视区域内 */
    * {
        max-height: 100vh !important;
        max-width: 100vw !important;
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

# 三个图片框的主容器 - 使用HTML和CSS创建横向布局
st.markdown('''
<div class="boxes-main-container">
    <!-- 内容图片框 -->
    <div class="image-box">
        <div style="text-align: center; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 3vw; color: #4CAF50;">📷</div>
            <div class="box-text">内容图片</div>
        </div>
    </div>
    
    <!-- 加号1 -->
    <div class="operator">+</div>
    
    <!-- 风格图片框 -->
    <div class="image-box">
        <div style="text-align: center; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 3vw; color: #4CAF50;">🎨</div>
            <div class="box-text">风格图片</div>
        </div>
    </div>
    
    <!-- 加号2 -->
    <div class="operator">=</div>
    
    <!-- 结果图片框 -->
    <div class="image-box">
        <div style="text-align: center; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 3vw; color: #4CAF50;">✨</div>
            <div class="box-text">融合结果</div>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# 使用Streamlit的columns创建文件上传组件，放置在绝对位置
col1, col2, col3 = st.columns([1, 0.05, 1, 0.05, 1])

with col1:
    content_image = st.file_uploader(
        "内容图片",
        type=['png', 'jpg', 'jpeg'],
        key="content",
        label_visibility="collapsed"
    )

with col3:
    style_image = st.file_uploader(
        "风格图片", 
        type=['png', 'jpg', 'jpeg'],
        key="style",
        label_visibility="collapsed"
    )

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
        st.warning("请先上传内容图和风格图")
st.markdown('</div>', unsafe_allow_html=True)

# 底部信息
st.markdown('''
<div class="footer">
    使用说明：上传内容图和风格图，点击一键生成按钮即可获得融合风格图
</div>
''', unsafe_allow_html=True)

# 关闭层面1
st.markdown('</div>', unsafe_allow_html=True)  # 关闭layer-1

# 关闭主容器
st.markdown('</div>', unsafe_allow_html=True)  # 关闭main-container

# 初始化session state
if 'result_image' not in st.session_state:
    st.session_state.result_image = None


