import streamlit as st
from PIL import Image
import time

# 页面配置
st.set_page_config(
    page_title="AI 图片风格融合工具",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 全局样式
st.markdown(
    """
    <style>
    html, body, #root, .stApp {
        height: 100vh;
        width: 100vw;
        overflow: hidden;
        position: fixed;
        top: 0;
        left: 0;
        margin: 0;
        padding: 0;
    }
    #MainMenu, footer, header {
        visibility: hidden;
    }
    .gray-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: #808080;
        z-index: 1;
    }
    .white-panel {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 90vw;
        max-width: 1200px;
        height: 90vh;
        max-height: 800px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        z-index: 2;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        overflow: hidden;
    }
    .title-section {
        text-align: center;
        margin-bottom: 20px;
    }
    .main-title {
        font-size: 24px;
        font-weight: bold;
        color: #ff69b4;
        margin: 0;
    }
    .image-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        width: 100%;
        margin-bottom: 20px;
    }
    .image-box {
        width: 30%;
        height: 300px;
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #f1f8e9;
        transition: all 0.3s ease;
        padding: 20px;
        position: relative;
        overflow: hidden;
    }
    .image-box:hover {
        border-color: #388E3C;
        background-color: #dcedc8;
    }
    .box-text {
        color: #2E7D32;
        font-size: 16px;
        text-align: center;
        margin-top: 8px;
        z-index: 10;
        position: relative;
    }
    .operator {
        font-size: 24px;
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
        width: 100%;
        margin-top: 20px;
    }
    .generate-button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 200px;
    }
    .generate-button:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
    }
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 14px;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 灰色背景
st.markdown('<div class="gray-bg"></div>', unsafe_allow_html=True)

# 白色工作区
st.markdown('<div class="white-panel">', unsafe_allow_html=True)

# 标题区域
st.markdown('''
<div class="title-section">
    <div class="main-title">AI 图片风格融合工具</div>
</div>
''', unsafe_allow_html=True)

# 图片框容器
st.markdown('<div class="image-container">', unsafe_allow_html=True)

# 使用Streamlit的columns创建横向布局
col1, col2, col3 = st.columns([1, 1, 1])

# 内容图片框
with col1:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    content_image = st.file_uploader(
        "内容图片",
        type=['png', 'jpg', 'jpeg'],
        key="content"
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

# 风格图片框
with col2:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    style_image = st.file_uploader(
        "风格图片", 
        type=['png', 'jpg', 'jpeg'],
        key="style"
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

# 结果图片框
with col3:
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
            import time
            time.sleep(2)
            st.session_state.result_image = "https://via.placeholder.com/400x300/4CAF50/FFFFFF?text= 融合结果"
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

# 初始化session state
if 'result_image' not in st.session_state:
    st.session_state.result_image = None